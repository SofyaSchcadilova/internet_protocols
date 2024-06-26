from urllib.request import Request, urlopen
import json


class VK_App:
    def __init__(self, id, token):
        self.id = id
        self.token = token
        self.api_version = "5.131"

    @staticmethod
    def make_request(req_message):
        req_obj = Request(req_message,
                          headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req_obj)
        return json.loads(page.read())

    def id_by_screen_name(self, screen_name):
        id_by_screenname_req = f"https://api.vk.com/method/users.get?user_ids={screen_name}" \
            f"&access_token={self.token}&v={self.api_version}"
        response = VK_App.make_request(id_by_screenname_req)
        try:
            return response["response"][0]["id"]
        except IndexError:
            raise ValueError("user does not exist")

    def get_friends_list(self, user_id):
        if not user_id.isdigit():
            try:
                user_id = self.id_by_screen_name(user_id)
            except KeyError:
                raise ValueError("user does not exist")
        friends_list_req = f"https://api.vk.com/method/friends.get?user_id={user_id}" \
            f"&order=hints&fields=nickname,domain&access_token={self.token}&v={self.api_version}"
        try:
            return self.make_request(friends_list_req)['response']
        except KeyError:
            raise KeyError(f"{self.make_request(friends_list_req)['error']['error_msg']}")
