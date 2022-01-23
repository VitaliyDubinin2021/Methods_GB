import requests
import json

LIST_REPOS = 'repos'

URL_GIT = 'https://api.github.com/users'

def get_list_users_repositories(username: str) -> list:

    result = requests.get(f'{URL_GIT}/{username}/{LIST_REPOS}')
    dict_result = result.json()

    return [{'name': reposit['full_name'], 'url': reposit['html_url']} for reposit in dict_result]


def main():
    repos = get_list_users_repositories('VitaliyDubinin2021')
    with open('task_one_h_v_1.json', 'w') as file:
        json.dump(repos, file, indent=2)


if __name__ == '__main__':
    main()