# Trabalho 4: Testes de Desempenho - Link Extractor 🚀

**Disciplina:** Computação Distribuida  
**Professor:** Nabor Mendonça  
**Equipe:**
* Fernanda Ortega - 2310305
* Guadalupe Prado - 2310300
* Letícia Cunha - 2315055

---

## 📌 Objetivo do Projeto
Este projeto tem como objetivo avaliar o comportamento e o desempenho de uma arquitetura de microsserviços (aplicação **Link Extractor**). Realizamos testes de carga variando a linguagem da API (Python e Ruby) e a utilização de uma camada de cache em memória (Redis), submetendo a aplicação a diferentes volumes de usuários virtuais simultâneos para identificar gargalos, limites físicos e ganhos de performance.

## 🛠 Ferramentas Utilizadas
* **Docker e Docker Compose:** Orquestração dos microsserviços (Web App em PHP, API em Python/Ruby e Cache em Redis).
* **Locust:** Ferramenta de teste de carga (Load Testing) para simular dezenas a milhares de usuários (Virtual Users - VUs).
* **Python (Pandas & Matplotlib):** Utilizados para extração e plotagem dos dados comparativos a partir dos relatórios CSV gerados pelo Locust.

---

## ⚙️ Metodologia e Configuração dos Testes
O script de teste (`locustfile.py`) foi configurado para simular o comportamento de usuários reais. Cada usuário virtual aguarda um tempo aleatório entre 1 e 3 segundos (`wait_time = between(1, 3)`) antes de solicitar à API a extração de links de uma lista pré-definida de 10 URLs variadas (com densidades de links indo de 55 até mais de 1000 links por página).

Os testes foram executados em cargas progressivas (110, 170 e 210 usuários) divididos em 4 cenários principais:
1. API em Python (Flask) **SEM** Cache
2. API em Python (Flask) **COM** Cache (Redis)
3. API em Ruby (Sinatra) **SEM** Cache
4. API em Ruby (Sinatra) **COM** Cache (Redis)

---

## 📊 Análise de Resultados e Gráficos

### 1. Tempo de Resposta (Percentil 95)
O gráfico abaixo ilustra o tempo máximo que 95% das requisições levaram para serem concluídas em cada cenário. Devido à imensa discrepância de desempenho, o gráfico utiliza uma **escala logarítmica** no eixo Y.

![Comparativo P95](graficos%20gerados/grafico_p95_comparativo.png)

### 2. Confiabilidade (Taxa de Erro)
O gráfico a seguir demonstra o percentual de falhas (Erros 500, Timeouts, Connection Refused) conforme a carga de usuários aumentava.

![Taxa de Erros](graficos%20gerados/grafico_taxa_erros.png)

---

## 🧠 Conclusões e Descobertas

1. **O Gargalo da Internet vs. O Triunfo do Cache:**
   No cenário SEM Cache, a aplicação é refém da latência da rede externa e de firewalls de terceiros. Para 210 usuários, o Python sem cache demorou cerca de **13.000 ms (13 segundos)** para responder, registrando falhas por bloqueio de servidores externos. 
   Ao introduzir o **Redis (COM Cache)**, a resposta caiu para assombrosos **5 a 8 milissegundos**, com **0% de falha**. O cache atuou como um escudo, eliminando a dependência da rede externa e servindo os dados diretamente da memória RAM.

2. **Python vs. Ruby sob Estresse de Rede (Sem Cache):**
   Ao comparar os cenários sem cache, o servidor Ruby (WEBrick/Sinatra) demonstrou maior resiliência no gerenciamento de conexões abertas do que o Python (Flask). Sob a carga de 210 usuários, o Ruby entregou os dados em **4.600 ms com 0% de erro**, enquanto o Python já apresentava fadiga de conexões (13.000 ms e taxa de erro em crescimento).

3. **Nivelamento pela Arquitetura:**
   A inserção do Redis igualou o desempenho de ambas as linguagens. No cenário COM cache, a diferença entre usar Python ou Ruby tornou-se estatisticamente insignificante. Isso prova que otimizações de arquitetura de software (inserção de cache) costumam trazer ganhos de performance muito superiores à simples troca da linguagem de programação do microsserviço.

---

## ⚠️ Observações e Problemas Registrados
Durante a fase de bateria de testes de estresse para definir as URLs alvos, registramos os seguintes fenômenos reais do comportamento de redes:
* **Bloqueio por Firewalls (Anti-Bot):** Sites como `g1.globo.com`, `www.debian.org` e `nytimes.com` bloquearam as requisições (Erro 500 / SSLEOFError) quando a carga passou de dezenas de usuários, provando a eficácia de sistemas Cloudflare/Anti-DDoS comerciais.
* **Erro OOM (Out Of Memory - Erro 137):** Durante testes com a URL `https://html.spec.whatwg.org/` (que continha absurdos 64.913 links), o container Docker da API Python excedeu o limite de Memória RAM alocado no sistema operacional e foi encerrado de forma abrupta ("Killed") pelo Mac. As URLs finais do teste foram ajustadas para páginas com volumes suportáveis pelo hardware local.

---

## 📁 Acesso aos Dados Brutos (CSVs)
Abaixo estão os links diretos para as pastas contendo os relatórios brutos gerados pelo Locust (Requisições e Falhas), organizados por cenário e carga:

### Python (Flask)
* 📂 **[Python SEM Cache](./csv%20cenarios/py%20sem%20cache/)**
  * [Carga 110](./csv%20cenarios/py%20sem%20cache/110/) | [Carga 170](./csv%20cenarios/py%20sem%20cache/170/) | [Carga 210](./csv%20cenarios/py%20sem%20cache/210/)
* 📂 **[Python COM Cache](./csv%20cenarios/py%20com%20cache/)**
  * [Carga 110](./csv%20cenarios/py%20com%20cache/110/) | [Carga 170](./csv%20cenarios/py%20com%20cache/170/) | [Carga 210](./csv%20cenarios/py%20com%20cache/210/)

### Ruby (Sinatra)
* 📂 **[Ruby SEM Cache](./csv%20cenarios/ruby%20sem%20cache/)**
  * [Carga 110](./csv%20cenarios/ruby%20sem%20cache/110/) | [Carga 170](./csv%20cenarios/ruby%20sem%20cache/170/) | [Carga 210](./csv%20cenarios/ruby%20sem%20cache/210/)
* 📂 **[Ruby COM Cache](./csv%20cenarios/ruby%20com%20cache/)**
  * [Carga 110](./csv%20cenarios/ruby%20com%20cache/110/) | [Carga 170](./csv%20cenarios/ruby%20com%20cache/170/) | [Carga 210](./csv%20cenarios/ruby%20com%20cache/210/)

*Scripts Adicionais:*
* 🐍 [Script Locust (`locustfile.py`)](./codigo%20locust/locustfile.py)
* 📈 [Scripts Python de Geração de Gráficos](./codigo%20gerar%20graficos/)
