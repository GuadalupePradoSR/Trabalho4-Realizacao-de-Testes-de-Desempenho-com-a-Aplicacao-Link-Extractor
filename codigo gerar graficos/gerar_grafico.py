import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

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
        110: "/Users/guadaprado/trabalho4/csv cenarios/ruby sem cache/110/Locust_2026-05-10-15h48_locustfile.py_http___localhost_4567_requests.csv",
        170: "/Users/guadaprado/trabalho4/csv cenarios/ruby sem cache/170/Locust_2026-05-10-15h36_locustfile.py_http___localhost_4567_requests.csv",
        210: "/Users/guadaprado/trabalho4/csv cenarios/ruby sem cache/210/Locust_2026-05-10-15h43_locustfile.py_http___localhost_4567_requests.csv"
    },
    "Ruby COM Cache": {
        110: "/Users/guadaprado/trabalho4/csv cenarios/ruby com cache/110/Locust_2026-05-10-16h07_locustfile.py_http___localhost_4567_requests.csv",
        170: "/Users/guadaprado/trabalho4/csv cenarios/ruby com cache/170/Locust_2026-05-10-16h04_locustfile.py_http___localhost_4567_requests.csv",
        210: "/Users/guadaprado/trabalho4/csv cenarios/ruby com cache/210/Locust_2026-05-10-16h00_locustfile.py_http___localhost_4567_requests.csv"
    }
}

def extrair_p95(caminho_csv):
    if not os.path.exists(caminho_csv):
        return None # Retorna None se não achar
    try:
        df = pd.read_csv(caminho_csv)
        linha_total = df[df['Name'] == 'Aggregated']
        return float(linha_total['95%'].values[0])
    except Exception as e:
        return None

# Extração com Avisos no Terminal
cargas = [110, 170, 210]
cenarios = list(dados_arquivos.keys())
valores_p95 = {cenario: [] for cenario in cenarios}

print("\n--- INICIANDO LEITURA DOS ARQUIVOS ---")
for cenario in cenarios:
    for carga in cargas:
        caminho = dados_arquivos[cenario][carga]
        p95 = extrair_p95(caminho)
        
        if p95 is None:
            print(f"❌ ERRO: Ficheiro não encontrado para {cenario} - {carga} users.")
            print(f"   Caminho tentado: {caminho}")
            valores_p95[cenario].append(0.0)
        else:
            print(f"✅ SUCESSO: {cenario} ({carga} users) -> P95 = {p95} ms")
            valores_p95[cenario].append(p95)
print("--------------------------------------\n")

# Configuração e Geração do Gráfico
plt.figure(figsize=(14, 8))
largura_barra = 0.2
posicoes_base = np.arange(len(cargas))
cores = ['#1f77b4', '#ff7f0e', '#d62728', '#2ca02c']

for i, cenario in enumerate(cenarios):
    posicoes_cenario = [p + i * largura_barra for p in posicoes_base]
    barras = plt.bar(posicoes_cenario, valores_p95[cenario], largura_barra, label=cenario, color=cores[i])
    
    for barra in barras:
        altura = barra.get_height()
        if altura > 0:
            plt.text(barra.get_x() + barra.get_width()/2., altura,
                     f'{int(altura)}', ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

plt.xlabel('Número de Usuários Virtuais', fontweight='bold', fontsize=12)
plt.ylabel('Tempo de Resposta P95 (ms) - Escala Logarítmica', fontweight='bold', fontsize=12)
plt.title('Comparativo de Desempenho (P95)', fontweight='bold', fontsize=14, pad=20)
plt.xticks([p + largura_barra * 1.5 for p in posicoes_base], cargas)

plt.yscale('log') 

plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.legend(title='Cenários', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('grafico_p95_comparativo.png', dpi=300, bbox_inches='tight')
plt.show()