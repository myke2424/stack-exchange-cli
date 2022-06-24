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
        params={"q": query, "accepted": True, "site": site}
        print(f"Params: {params}")
        resp = self._make_request(endpoint="/search/advanced", params=params)
        answer_ids = [item["accepted_answer_id"] for item in resp["items"]]
        answers = self._make_request("/answers", params={"answers_ids": answer_ids, "site": site})
        print()



client = StackExchange()
resp = client.search("How to traverse file directory rust")
print("DONE!")