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

# 2. FUNÇÃO PARA CALCULAR A PORCENTAGEM DE ERRO
def extrair_taxa_erro(caminho_csv):
    if not os.path.exists(caminho_csv):
        return None 
    try:
        df = pd.read_csv(caminho_csv)
        linha_total = df[df['Name'] == 'Aggregated']
        
        # Pega o total de requisições e o total de falhas
        total_req = float(linha_total['Request Count'].values[0])
        total_fail = float(linha_total['Failure Count'].values[0])
        
        if total_req > 0:
            porcentagem = (total_fail / total_req) * 100
            return round(porcentagem, 2) # Arredonda para 2 casas decimais
        return 0.0
    except Exception as e:
        return None

# 3. EXTRAÇÃO DOS DADOS
cargas = [110, 170, 210]
cenarios = list(dados_arquivos.keys())
valores_erro = {cenario: [] for cenario in cenarios}

print("\n--- CALCULANDO TAXAS DE ERRO ---")
for cenario in cenarios:
    for carga in cargas:
        caminho = dados_arquivos[cenario][carga]
        taxa = extrair_taxa_erro(caminho)
        
        if taxa is None:
            valores_erro[cenario].append(0.0)
        else:
            print(f"✅ {cenario} ({carga} users) -> Falha: {taxa}%")
            valores_erro[cenario].append(taxa)
print("--------------------------------\n")

# 4. CONFIGURAÇÃO E GERAÇÃO DO GRÁFICO
plt.figure(figsize=(12, 7))

largura_barra = 0.2
posicoes_base = np.arange(len(cargas))
cores = ['#1f77b4', '#ff7f0e', '#d62728', '#2ca02c']

for i, cenario in enumerate(cenarios):
    posicoes_cenario = [p + i * largura_barra for p in posicoes_base]
    barras = plt.bar(posicoes_cenario, valores_erro[cenario], largura_barra, label=cenario, color=cores[i])
    
    # Adicionando a porcentagem exata no topo de cada barra
    for barra in barras:
        altura = barra.get_height()
        if altura > 0:
            plt.text(barra.get_x() + barra.get_width()/2., altura + (max(valores_erro[cenario]) * 0.02),
                     f'{altura}%', ha='center', va='bottom', fontsize=9, fontweight='bold', color='black')
        elif altura == 0:
            plt.text(barra.get_x() + barra.get_width()/2., 0.1,
                     '0%', ha='center', va='bottom', fontsize=9, color='gray')

# Estilização
plt.xlabel('Número de Usuários Virtuais', fontweight='bold', fontsize=12)
plt.ylabel('Taxa de Erro / Falhas (%)', fontweight='bold', fontsize=12)
plt.title('Comparativo de Confiabilidade: Taxa de Erro por Carga', fontweight='bold', fontsize=14, pad=20)
plt.xticks([p + largura_barra * 1.5 for p in posicoes_base], cargas)

# Define o limite do eixo Y para ter um respiro no visual
max_erro_geral = max([max(lista) for lista in valores_erro.values()])
plt.ylim(0, max(10, max_erro_geral + 2)) # Vai até 10% no mínimo, ou um pouco acima do erro máximo

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(title='Cenários', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Salva a imagem
nome_arquivo = 'grafico_taxa_erros.png'
plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
print(f"Gráfico gerado com sucesso! Salvo como '{nome_arquivo}'.")
plt.show()