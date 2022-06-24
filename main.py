import requests

client_id = "23685"

# SECRET
client_secret = "7DI9bW2I4WM3YoMhaTSW9A(("

# use for requests
api_key = "F2wA5L2NXwhEWWlTomEt)Q(("


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
        print(res['title'], '\n')
        print(res['body'])

        answer_id = res['accepted_answer_id']

        answer = self._make_request(f"/answers/{answer_id}", params={"site": site,
                                                                     "filter": "withbody"})

        print("***ANSWER*** \n")
        print(answer['items'][0]['body'])


client = StackExchange()
resp = client.search("Reverse linked list")
