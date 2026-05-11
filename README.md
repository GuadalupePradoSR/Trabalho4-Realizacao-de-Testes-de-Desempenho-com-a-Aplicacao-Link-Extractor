# Trabalho 4: Testes de Desempenho - Link Extractor

**Disciplina:** Computação Distribuída  
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
* Abaixo está o trecho principal do script de configuração [**`locustfile.py`**](./codigo%20locust/locustfile.py) que define a rotina de cada usuário:

```python
from locust import HttpUser, task, between

class ExtratorLinksVUser(HttpUser):
    # Simula o tempo de "pensamento" do usuário entre ações
    wait_time = between(1, 3)

    @task
    def sequencia_dez_invocacoes(self):
        urls_alvo = [
            "[https://www.bbc.com/](https://www.bbc.com/)",
            "[https://g1.globo.com/](https://g1.globo.com/)", 
            "[https://edition.cnn.com/](https://edition.cnn.com/)", 
            "[https://books.toscrape.com/](https://books.toscrape.com/)",
            "[https://crawler-test.com/](https://crawler-test.com/)", 
            "[https://quotes.toscrape.com/](https://quotes.toscrape.com/)", 
            "[https://www.php.net/manual/pt_BR/](https://www.php.net/manual/pt_BR/)",
            "[https://github.com/explore](https://github.com/explore)", 
            "[https://www.w3schools.com/tags/default.asp](https://www.w3schools.com/tags/default.asp)", 
            "[https://developer.mozilla.org/en-US/](https://developer.mozilla.org/en-US/)" 
        ]

        # Itera sobre as URLs enviando-as para a nossa API
        for url in urls_alvo:
            self.client.get(f"/api/{url}", name="/api/[url_alvo]")
```

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

Os testes foram estruturados em 4 cenários principais para isolar as variáveis de "Linguagem de Programação" e "Uso de Memória Cache". Abaixo, descrevemos cada cenário com seus respectivos gráficos de **Desempenho** (Tempo em ms do percentil P95) e **Confiabilidade** (Taxa de Erro %):

### 1. API em Python (Flask) SEM Cache
Cenário onde a API em Python extrai os links "ao vivo" a cada requisição, sofrendo impacto direto da latência da rede e bloqueios.
* Comportamento das Barras: Apresenta um crescimento acentuado conforme a carga de usuários aumenta.
* Impacto da Carga Máxima: Aos 210 usuários simultâneos, o tempo de resposta (P95) atinge picos críticos de aproximadamente 13.000 milissegundos (13 segundos).
![Desempenho Python Sem Cache](graficos%20gerados/grafico%20cenarios/py%20sem%20cache/grafico_desempenho_python_sem_cache.png)

* Revela o ponto de ruptura da aplicação. À medida que a carga sobe para 210 usuários, a taxa de erros cresce devido a bloqueios de anti-bot dos sites alvo e estouro de buffers de conexão.
![Erro Python Sem Cache](graficos%20gerados/grafico%20cenarios/py%20sem%20cache/grafico_erro_python_sem_cache.png)

### 2. API em Python (Flask) COM Cache (Redis)
Cenário onde o Redis foi ativado. As requisições são servidas em milissegundos direto da memória, sem depender do acesso externo contínuo.
* Impacto da Carga Máxima: O tempo de resposta despenca para a faixa de 5 a 8 milissegundos, mantendo-se estável mesmo com 210 usuários ativos.
![Desempenho Python Com Cache](graficos%20gerados/grafico%20cenarios/py%20com%20cache/grafico_desempenho_python_com_cache.png)

* Mantém uma taxa de 0% de erro em todos os níveis de carga, provando que o cache protege a aplicação contra instabilidades externas.
![Erro Python Com Cache](graficos%20gerados/grafico%20cenarios/py%20com%20cache/grafico_erro_python_com_cache.png)

### 3. API em Ruby (Sinatra) SEM Cache
Cenário base para avaliar a resiliência do servidor WEBrick/Sinatra sob altas conexões para extração "ao vivo", sem auxílio de cache.
![Desempenho Ruby Sem Cache](graficos%20gerados/grafico%20cenarios/ruby%20sem%20cache/grafico_desempenho_ruby_sem_cache.png)
![Erro Ruby Sem Cache](graficos%20gerados/grafico%20cenarios/ruby%20sem%20cache/grafico_erro_ruby_sem_cache.png)

### 4. API em Ruby (Sinatra) COM Cache (Redis)
Cenário otimizado em Ruby. Servindo o conteúdo diretamente do Redis para verificar nivelamento de performance em relação ao Python.
![Desempenho Ruby Com Cache](graficos%20gerados/grafico%20cenarios/ruby%20com%20cache/grafico_desempenho_ruby_com_cache.png)

Mantém uma taxa de 0% de erro em todos os níveis de carga, provando que o cache protege a aplicação contra instabilidades externas.
![Erro Ruby Com Cache](graficos%20gerados/grafico%20cenarios/ruby%20com%20cache/grafico_erro_ruby_com_cache.png)

## Modificação do Código Original (Cenário: Ruby SEM Cache)
Para garantir a rigorosidade e a veracidade arquitetural do cenário **API em Ruby (Sinatra) SEM Cache**, foi necessário realizar modificações diretas no código-fonte do repositório base fornecido em [ibnesayeed/linkextractor](https://github.com/ibnesayeed/linkextractor) (especificamente os arquivos da pasta `step6`).

Por padrão, a versão Ruby do Link Extractor implementa a conexão obrigatória com o Redis. Para desativar o cache de forma efetiva e forçar a API a realizar a raspagem (scraping) na internet em 100% das requisições, as seguintes alterações foram aplicadas:

### 1. Desativação da Lógica de Cache (`api/linkextractor.rb`)
As funções de busca (`redis.get`) e gravação (`redis.set`) foram inibidas no código, forçando a variável `jsonlinks` a receber o processamento direto da função `extract_links`.

```ruby
get "/api/*" do
  url = [params['splat'].first, request.query_string].reject(&:empty?).join("?")
  cache_status = "MISS" # Forçado para MISS para o log
  
  # A extração ocorre em tempo real, ignorando o banco
  jsonlinks = JSON.pretty_generate(extract_links(url))
  
  # AS LINHAS ABAIXO FORAM COMENTADAS/REMOVIDAS:
  # jsonlinks = redis.get(url)
  # if jsonlinks.nil?
  #   cache_status = "MISS"
  #   jsonlinks = JSON.pretty_generate(extract_links(url))
  #   redis.set(url, jsonlinks)
  # end

  cache_log.puts "#{Time.now.to_i}\t#{cache_status}\t#{url}"
  status 200
  headers "content-type" => "application/json"
  body jsonlinks
end
```
### 2. Remoção do Contêiner (`docker-compose.yml`)
Para evitar que o serviço do banco de dados continuasse rodando "fantasma" consumindo memória RAM do ambiente de testes, o contêiner do Redis e a variável de ambiente REDIS_URL foram comentados na orquestração do Docker.
``` ruby
version: '3'

services:
  api:
    image: linkextractor-api:step6-ruby
    build: ./api
    ports:
      - "4567:4567"
    # Variável removida para isolar a API:
    # environment:
    #  - REDIS_URL=redis://redis:6379
    volumes:
      - ./logs:/app/logs
  web:
    # ... configurações da web ...
    
# Serviço do banco de dados inativado:
#  redis:
#    image: redis
```

---

### Comparativo Geral
Além das visualizações por cenário, compilamos as informações gerais nos gráficos abaixo. Note que devido à alta discrepância entre as linguagens sem cache vs com cache, o gráfico de tempo de resposta possui **escala logarítmica**.

**Tempo de Resposta P95 (Escala Logarítmica)**
![Comparativo P95](graficos%20gerados/grafico%20geral/desempenho_geral.png)  

**Taxa de Erros**
![Taxa de Erros](graficos%20gerados/grafico%20geral/falha_geral.png)

---

## Conclusões e Descobertas

1. **A Arquitetura Supera a Linguagem:**
   A inserção do Redis igualou o desempenho de ambas as linguagens. No cenário COM cache, a diferença de velocidade entre usar Python ou Ruby tornou-se praticamente nula (estabilizando entre 5 e 8 milissegundos). Isso prova que otimizações de arquitetura de software costumam trazer ganhos superiores à simples troca da linguagem de programação.

2. **O Verdadeiro Gargalo é a Rede (I/O Bound):**
   Nos cenários SEM Cache, ficou claro que a aplicação não estava limitada pelo poder de processamento interno, mas sim pela latência da internet e pelas restrições de terceiros (firewalls e bloqueios dos sites alvo). Para 210 usuários, o Python sem cache demorou cerca de **13.000 ms (13 segundos)** para responder e o Ruby sem cache demorou cerca de **7.900 ms (7 segundos)** para responder.

3. **O Cache como "Escudo de Confiabilidade":**
   Mais do que apenas velocidade, o Redis funcionou como um escudo protetor. Ele isolou os microsserviços da instabilidade da internet, evitou a fadiga de conexões e garantiu uma **taxa de 0% de erros** em todos os cenários, independentemente da carga de usuários.

---

## Observações e Problemas Registrados
Durante a fase de bateria de testes de estresse para definir as URLs alvos, registramos os seguintes fenômenos reais do comportamento de redes:
* **Bloqueio por Firewalls (Anti-Bot):** Sites como `www.debian.org` e `nytimes.com` bloquearam as requisições (Erro 500 / SSLEOFError) quando a carga passou de dezenas de usuários, provando a eficácia de sistemas Cloudflare/Anti-DDoS comerciais.
* **Erro OOM (Out Of Memory - Erro 137):** Durante testes com a URL `https://html.spec.whatwg.org/` (que continha absurdos 64.913 links), o container Docker da API Python excedeu o limite de Memória RAM alocado no sistema operacional e foi encerrado de forma abrupta ("Killed") pelo sistema. As URLs finais do teste foram ajustadas para páginas com volumes suportáveis pelo hardware local.

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
