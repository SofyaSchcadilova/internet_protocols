from vk_app import VK_App
import argparse


def print_friends(string):
    len_s = 25
    print("-" * len_s)
    for human in string:
        first_name = human[0]
        last_name = human[1]
        print(f"First Name: {first_name}\n"
              f" Last Name: {last_name}")
        print("-" * len_s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-userid", required=True)
    parser.add_argument("-appid", required=True, help="id of vk application")
    parser.add_argument("-token", required=True,
                        help="access_token of vk_app")
    cnsl_args = parser.parse_args().__dict__
    protocols_app = VK_App(cnsl_args["appid"], cnsl_args["token"])
    user_id = cnsl_args["userid"]
    humans_dict = protocols_app.get_friends_list(user_id)['items']
    res = []
    for human in humans_dict:
        res.append([human['first_name'], human['last_name']])
    print_friends(res)
