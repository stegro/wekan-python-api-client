import requests
from .models import Board


class WekanApi:
    def api_call(self, url, data=None, authed=True, params=None):
        if data is None and params is None:
            api_response = self.session.get(
                "{}{}".format(self.api_url, url),
                headers={"Authorization": "Bearer {}".format(self.token)},
                proxies=self.proxies
            )
        else:
            # modify
            if params:
                if data:
                    print 1
                    api_response = self.session.put(
                        "{}{}".format(self.api_url, url),
                        data=data,
                        headers={"Authorization": "Bearer {}".format(self.token)},
                        proxies=self.proxies
                    )
                else:
                    headers = {
                      'Content-Type': 'multipart/form-data',
                      'Accept': 'application/json',
                      'Authorization': "Bearer {}".format(self.token),
                    }
                    print 2, headers, "{}{}".format(self.api_url, url)
                    api_response = self.session.put(
                        "{}{}".format(self.api_url, url),
                        params=params,
                        headers=headers if authed else {},
                        proxies=self.proxies
                    )
            # add
            else:
                print 3
                api_response = self.session.post(
                    "{}{}".format(self.api_url, url),
                    data=data,
                    headers={"Authorization": "Bearer {}".format(self.token)} if authed else {},
                    proxies=self.proxies
                )
        return api_response.json()

    def __init__(self, api_url, credentials, proxies=None):
        if proxies is None:
            proxies = {}
        self.session = requests.Session()
        self.proxies = proxies
        self.api_url = api_url
        api_login = self.api_call("/users/login", data=credentials, authed=False)
        self.token = api_login["token"]
        self.user_id = api_login["id"]

    def get_user_boards(self, filter=''):
        boards_data = self.api_call("/api/users/{}/boards".format(self.user_id))
        return [Board(self, board_data) for board_data in boards_data if filter in board_data["title"]]
