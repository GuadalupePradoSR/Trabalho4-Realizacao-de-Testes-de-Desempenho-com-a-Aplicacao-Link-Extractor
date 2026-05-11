# Trabalho 4: Testes de Desempenho - Link Extractor

**Disciplina:** Computação Distribuida  
**Professor:** Nabor Mendonça  
**Equipe:**
* Fernanda Ortega - 2310305
* Guadalupe Prado - 2310300
* Letícia Cunha - 2315055

---

## Objetivo do Projeto
Este projeto tem como objetivo avaliar o comportamento e o desempenho de uma arquitetura de microsserviços (aplicação **Link Extractor**). Realizamos testes de carga variando a linguagem da API (Python e Ruby) e a utilização de uma camada de cache em memória (Redis), submetendo a aplicação a diferentes volumes de usuários virtuais simultâneos para identificar gargalos, limites físicos e ganhos de performance.

## Ferramentas Utilizadas
* **Docker e Docker Compose:** Orquestração dos microsserviços (Web App em PHP, API em Python/Ruby e Cache em Redis).
* **Locust:** Ferramenta de teste de carga (Load Testing) para simular dezenas a milhares de usuários (Virtual Users - VUs).
* **Python (Pandas & Matplotlib):** Utilizados para extração e plotagem dos dados comparativos a partir dos relatórios CSV gerados pelo Locust.

---

## Metodologia e Configuração dos Testes

### Ferramenta de Teste de Carga e Comportamento do Usuário
Foi utilizado o **Locust**, uma ferramenta de teste de carga baseada em Python, para simular o comportamento de usuários reais. O script de configuração (`locustfile.py`) define exatamente como cada usuário virtual (VU) age no sistema:
* Cada usuário aguarda um tempo aleatório entre 1 e 3 segundos (`wait_time = between(1, 3)`) antes de fazer uma nova requisição, simulando o tempo de leitura de um humano.
* Durante o teste, cada usuário executa a tarefa principal iterando sobre uma lista pré-definida de 10 URLs. Para cada uma, é feita uma requisição `GET` para o endpoint da aplicação `/api/{url_alvo}` a fim de extrair seus links.

### Justificativa e URLs Utilizadas
As URLs foram escolhidas propositalmente com base na quantidade de links contidos em cada página, variando de conteúdos muito leves até páginas extremamente densas em hiperlinks. O uso dessa lista justifica-se para garantir variabilidade e estressar o processamento da aplicação com diferentes densidades de payload durante a mesma sessão de navegação de um usuário.

As URLs alvos configuradas e seus respectivos tamanhos de links foram:
* `https://quotes.toscrape.com/` -> 55 links
* `https://books.toscrape.com/` -> 94 links
* `https://developer.mozilla.org/en-US/` -> 171 links
* `https://www.php.net/manual/pt_BR/` -> 229 links
* `https://www.bbc.com/` -> 302 links
* `https://github.com/explore` -> 325 links
* `https://crawler-test.com/` -> 415 links
* `https://edition.cnn.com/` -> 493 links
* `https://g1.globo.com/` -> 672 links
* `https://www.w3schools.com/tags/default.asp` -> 1008 links

Os testes foram executados em cargas progressivas de 110, 170 e 210 usuários concorrentes.

---

## Cenários de Teste Avaliados e Gráficos

Os testes foram estruturados em 4 cenários principais para isolar as variáveis de "Linguagem de Programação" e "Uso de Memória Cache". Abaixo, descrevemos cada cenário com links para seus respectivos gráficos de **Desempenho** (Tempo em ms do percentil P95) e **Confiabilidade** (Taxa de Erro %):

### 1. API em Python (Flask) SEM Cache
Cenário onde a API em Python extrai os links "ao vivo" a cada requisição, sofrendo impacto direto da latência da rede e bloqueios.
* 📈 **[Gráfico de Desempenho P95](graficos%20gerados/grafico%20cenarios/py%20sem%20cache/grafico_desempenho_python_sem_cache.png)**
* 📉 **[Gráfico de Taxa de Erro](graficos%20gerados/grafico%20cenarios/py%20sem%20cache/grafico_erro_python_sem_cache.png)**

### 2. API em Python (Flask) COM Cache (Redis)
Cenário onde o Redis foi ativado. As requisições são servidas em milissegundos direto da memória, sem depender do acesso externo contínuo.
* 📈 **[Gráfico de Desempenho P95](graficos%20gerados/grafico%20cenarios/py%20com%20cache/grafico_desempenho_python_com_cache.png)**
* 📉 **[Gráfico de Taxa de Erro](graficos%20gerados/grafico%20cenarios/py%20com%20cache/grafico_erro_python_com_cache.png)**

### 3. API em Ruby (Sinatra) SEM Cache
Cenário base para avaliar a resiliência do servidor WEBrick/Sinatra sob altas conexões para extração "ao vivo", sem auxílio de cache.
* 📈 **[Gráfico de Desempenho P95](graficos%20gerados/grafico%20cenarios/ruby%20sem%20cache/grafico_desempenho_ruby_sem_cache.png)**
* 📉 **[Gráfico de Taxa de Erro](graficos%20gerados/grafico%20cenarios/ruby%20sem%20cache/grafico_erro_ruby_sem_cache.png)**

### 4. API em Ruby (Sinatra) COM Cache (Redis)
Cenário otimizado em Ruby. Servindo o conteúdo diretamente do Redis para verificar nivelamento de performance em relação ao Python.
* 📈 **[Gráfico de Desempenho P95](graficos%20gerados/grafico%20cenarios/ruby%20com%20cache/grafico_desempenho_ruby_com_cache.png)**
* 📉 **[Gráfico de Taxa de Erro](graficos%20gerados/grafico%20cenarios/ruby%20com%20cache/grafico_erro_ruby_com_cache.png)**

### Comparativo Geral
Além das visualizações por cenário, compilamos as informações gerais nos gráficos abaixo. Note que devido à alta discrepância entre as linguagens sem cache vs com cache, o gráfico de tempo de resposta possui **escala logarítmica**.

![Comparativo P95](graficos%20gerados/grafico%20geral/grafico_p95_comparativo.png)  
![Taxa de Erros](graficos%20gerados/grafico%20geral/grafico_taxa_erros.png)

---

## Conclusões e Descobertas

1. **A Internet vs. O Cache:**
   No cenário SEM Cache, a aplicação é refém da latência da rede externa e de firewalls de terceiros. Para 210 usuários, o Python sem cache demorou cerca de **13.000 ms (13 segundos)** para responder, registrando falhas por bloqueio de servidores externos. 
   Ao introduzir o **Redis (COM Cache)**, a resposta caiu para assombrosos **5 a 8 milissegundos**, com **0% de falha**. O cache atuou como um escudo, eliminando a dependência da rede externa e servindo os dados diretamente da memória RAM.

2. **Python vs. Ruby sob Estresse de Rede (Sem Cache):**
   Ao comparar os cenários sem cache, o servidor Ruby (WEBrick/Sinatra) demonstrou maior resiliência no gerenciamento de conexões abertas do que o Python (Flask). Sob a carga de 210 usuários, o Ruby entregou os dados em **4.600 ms com 0% de erro**, enquanto o Python já apresentava fadiga de conexões (13.000 ms e taxa de erro em crescimento).

3. **Nivelamento pela Arquitetura:**
   A inserção do Redis igualou o desempenho de ambas as linguagens. No cenário COM cache, a diferença entre usar Python ou Ruby tornou-se estatisticamente insignificante. Isso prova que otimizações de arquitetura de software (inserção de cache) costumam trazer ganhos de performance muito superiores à simples troca da linguagem de programação do microsserviço.

---

## Observações e Problemas Registrados
Durante a fase de bateria de testes de estresse para definir as URLs alvos, registramos os seguintes fenômenos reais do comportamento de redes:
* **Bloqueio por Firewalls (Anti-Bot):** Sites como `g1.globo.com`, `www.debian.org` e `nytimes.com` bloquearam as requisições (Erro 500 / SSLEOFError) quando a carga passou de dezenas de usuários, provando a eficácia de sistemas Cloudflare/Anti-DDoS comerciais.
* **Erro OOM (Out Of Memory - Erro 137):** Durante testes com a URL `https://html.spec.whatwg.org/` (que continha absurdos 64.913 links), o container Docker da API Python excedeu o limite de Memória RAM alocado no sistema operacional e foi encerrado de forma abrupta ("Killed") pelo Mac. As URLs finais do teste foram ajustadas para páginas com volumes suportáveis pelo hardware local.

---

## Acesso aos Dados Brutos (CSVs)
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
*  [Script Locust (`locustfile.py`)](./codigo%20locust/locustfile.py)
*  [Scripts Python de Geração de Gráficos](./codigo%20gerar%20graficos/)
