"""
Stack exchange client interface used for searching!
"""


class StackExchange:
    """
    Wrapper class for the stack exchange API
    Facade only caring about search
    """

    SEARCH_ENDPOINT = "/search/advanced"

    def __init__(self, version="2.3"):
        self.version = version
        self.url = f"https://api.stackexchange.com/{version}"

    def _make_request(self, endpoint, params):
        url = self.url + endpoint
        response = requests.get(url, params).json()

        if response.get('error_message') is not None:
            raise StackRequestError(response.get('error_message'))
        return response

    def search(self, query, params, site="stackoverflow"):
        default_params = {"accepted": True, "filter": "withbody"}
        params = {**params, **default_params}

        resp = self._make_request(endpoint=self.SEARCH_ENDPOINT, params=params)

        res = resp['items'][0]
        print(res['title'])
        question = res['body']
        console.print(strip_tags(question))

        answer_id = res['accepted_answer_id']

        answer = self._make_request(f"/answers/{answer_id}", params={"site": site,
                                                                     "filter": "withbody"})

        print("***ANSWER*** \n")
        a = answer['items'][0]['body']
        # console.print(strip_tags(a))
