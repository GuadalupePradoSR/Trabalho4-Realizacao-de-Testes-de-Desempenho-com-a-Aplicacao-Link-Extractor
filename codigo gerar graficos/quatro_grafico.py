import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. CAMINHOS REAIS JÁ PREENCHIDOS
dados_arquivos = {
    "Python SEM Cache": {
        110: "/Users/guadaprado/trabalho4/csv cenarios/py sem cache/110/Locust_2026-05-09-18h27_locustfile.py_http___localhost_5000_requests.csv",
        170: "/Users/guadaprado/trabalho4/csv cenarios/py sem cache/170/Locust_2026-05-09-18h31_locustfile.py_http___localhost_5000_requests.csv",
        210: "/Users/guadaprado/trabalho4/csv cenarios/py sem cache/210/Locust_2026-05-09-18h34_locustfile.py_http___localhost_5000_requests.csv"
    },
    "Python COM Cache": {
        110: "/Users/guadaprado/trabalho4/csv cenarios/py com cache/110/Locust_2026-05-10-22h01_locustfile.py_http___localhost_5000_requests.csv",
        170: "/Users/guadaprado/trabalho4/csv cenarios/py com cache/170/Locust_2026-05-10-21h58_locustfile.py_http___localhost_5000_requests.csv",
        210: "/Users/guadaprado/trabalho4/csv cenarios/py com cache/210/Locust_2026-05-10-16h27_locustfile.py_http___localhost_5000_requests.csv"
    },
    "Ruby SEM Cache": {
        110: "/Users/guadaprado/trabalho4/csv cenarios/ruby sem cache/110/Locust_2026-05-11-18h16_locustfile.py_http___localhost_4567_requests.csv",
        170: "/Users/guadaprado/trabalho4/csv cenarios/ruby sem cache/170/Locust_2026-05-11-18h21_locustfile.py_http___localhost_4567_requests.csv",
        210: "/Users/guadaprado/trabalho4/csv cenarios/ruby sem cache/210/Locust_2026-05-11-18h29_locustfile.py_http___localhost_4567_requests.csv"
    },
    "Ruby COM Cache": {
        110: "/Users/guadaprado/trabalho4/csv cenarios/ruby com cache/110/Locust_2026-05-10-16h07_locustfile.py_http___localhost_4567_requests.csv",
        170: "/Users/guadaprado/trabalho4/csv cenarios/ruby com cache/170/Locust_2026-05-10-16h04_locustfile.py_http___localhost_4567_requests.csv",
        210: "/Users/guadaprado/trabalho4/csv cenarios/ruby com cache/210/Locust_2026-05-10-16h00_locustfile.py_http___localhost_4567_requests.csv"
    }
}

def extrair_metricas(caminho_csv):
    if not os.path.exists(caminho_csv):
        print(f"❌ ERRO: Ficheiro não encontrado: {caminho_csv}")
        return 0.0, 0.0
    try:
        df = pd.read_csv(caminho_csv)
        linha_total = df[df['Name'] == 'Aggregated']
        
        p95 = float(linha_total['95%'].values[0])
        total_req = float(linha_total['Request Count'].values[0])
        total_fail = float(linha_total['Failure Count'].values[0])
        
        taxa_erro = round((total_fail / total_req) * 100, 2) if total_req > 0 else 0.0
        print(f"✅ LIDO: P95={p95}ms | Erro={taxa_erro}%")
        return p95, taxa_erro
    except Exception as e:
        print(f"❌ ERRO ao processar {caminho_csv}: {e}")
        return 0.0, 0.0

cargas = [110, 170, 210]
rotulos_cargas = [str(c) for c in cargas]

print("\n--- EXTRAINDO DADOS E GERANDO OS 8 GRÁFICOS ---")

for cenario, arquivos in dados_arquivos.items():
    print(f"\nProcessando cenário: {cenario}")
    p95_lista = []
    erros_lista = []
    
    for carga in cargas:
        # Pega o caminho, convertendo a carga para garantir que acha a chave
        caminho = arquivos.get(carga, "") 
        p95, erro = extrair_metricas(caminho)
        p95_lista.append(p95)
        erros_lista.append(erro)
        
    nome_base = cenario.replace(' ', '_').lower()
    
    # =========================================================
    # GRÁFICO 1: DESEMPENHO (P95)
    # =========================================================
    plt.figure(figsize=(8, 5))
    barras_p95 = plt.bar(rotulos_cargas, p95_lista, color='#1f77b4', width=0.5)
    plt.xlabel('Número de Usuários Virtuais', fontweight='bold', fontsize=11)
    plt.ylabel('Tempo de Resposta P95 (ms)', fontweight='bold', fontsize=11, color='#1f77b4')
    plt.title(f'Desempenho P95 - {cenario}', fontweight='bold', fontsize=13, pad=15)
    
    max_p95 = max(p95_lista) if max(p95_lista) > 0 else 10
    plt.ylim(0, max_p95 * 1.25)
    
    for barra in barras_p95:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2., altura + (max_p95 * 0.02),
                 f'{int(altura)} ms', ha='center', va='bottom', fontweight='bold', color='black')
                 
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    nome_arq_p95 = f"grafico_desempenho_{nome_base}.png"
    plt.savefig(nome_arq_p95, dpi=300, bbox_inches='tight')
    plt.close()

    # =========================================================
    # GRÁFICO 2: TAXA DE ERRO (%)
    # =========================================================
    plt.figure(figsize=(8, 5))
    barras_erro = plt.bar(rotulos_cargas, erros_lista, color='#d62728', width=0.5)
    plt.xlabel('Número de Usuários Virtuais', fontweight='bold', fontsize=11)
    plt.ylabel('Taxa de Erro (%)', fontweight='bold', fontsize=11, color='#d62728')
    plt.title(f'Confiabilidade (Erros) - {cenario}', fontweight='bold', fontsize=13, pad=15)
    
    max_erro = max(erros_lista) if max(erros_lista) > 0 else 1.0
    plt.ylim(0, max_erro * 1.25)
    
    for barra in barras_erro:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2., altura + (max_erro * 0.02),
                 f'{altura}%', ha='center', va='bottom', fontweight='bold', color='black')
                 
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    nome_arq_erro = f"grafico_erro_{nome_base}.png"
    plt.savefig(nome_arq_erro, dpi=300, bbox_inches='tight')
    plt.close()

print("\n✅ Todos os 8 gráficos foram criados com sucesso!")