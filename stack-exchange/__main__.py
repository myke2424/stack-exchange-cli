import requests
import toml

with open('config.toml') as f:
    config = toml.load(f)
# use for requests

from rich.console import Console
from rich.markdown import Markdown

console = Console()


# Proxy design pattern, potential!
class CachedStackExchangeProxy:
    def __init__(self, stack_exchange_service):
        self.service = stack_exchange_service

    def search(self, query, site="stackoverflow"):
        # Check if request is in the DB!?. Since using redis, maybe hash the query and site?
        self.service.search(query, site)


class StackExchange:
    def __init__(self, version="2.3"):
        self.version = version
        self.base_url = f"https://api.stackexchange.com/{version}"

    def _make_request(self, endpoint, params):
        url = self.base_url + endpoint
        print(f"Making request to: {url}")
        resp = requests.get(url, params)
        return resp.json()

    def search(self, query, site="stackoverflow"):
        params = {"q": query, "accepted": True, "site": site, "filter": "withbody"}
        resp = self._make_request(endpoint="/search/advanced", params=params)

        res = resp['items'][0]
        print(f"****** {res['title']} ******")
        question = res['body']
        console.print(question)

        answer_id = res['accepted_answer_id']

        answer = self._make_request(f"/answers/{answer_id}", params={"site": site,
                                                                     "filter": "withbody"})

        print("***ANSWER*** \n")
        a = answer['items'][0]['body']
        console.print(a)


client = StackExchange()
resp = client.search("Reverse linked list")
