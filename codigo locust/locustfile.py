from locust import HttpUser, task, between

class ExtratorLinksVUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def sequencia_dez_invocacoes(self):
        urls_alvo = [
            "https://www.bbc.com/",
            "https://g1.globo.com/", 
            "https://edition.cnn.com/", 
            "https://books.toscrape.com/",
            "https://crawler-test.com/", 
            "https://quotes.toscrape.com/", 
            "https://www.php.net/manual/pt_BR/",
            "https://github.com/explore", 
            "https://www.w3schools.com/tags/default.asp", 
            "https://developer.mozilla.org/en-US/" 
        ]

        for url in urls_alvo:
            self.client.get(f"/api/{url}", name="/api/[url_alvo]")
