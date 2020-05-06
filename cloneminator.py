import requests
import json

github_username = str()
github_token = str()
gitlab_url = str()
gitlab_token = str()


def get_stars(page=0):
    token_header = {"Authorization": "Bearer " + github_token}
    response = requests.get("https://api.github.com/users/" + github_username + "/starred?page=" + str(page), headers=token_header).text
    return json.loads(response)


def get_repos(page=0):
    token_header = {"Authorization": "Bearer " + github_token}
    response = requests.get("https://api.github.com/users/" + github_username + "/repos?page=" + str(page), headers=token_header).text
    return json.loads(response)


def delete_github_repo(name):
    token_header = {"Authorization": "Bearer " + github_token}
    response = requests.delete("https://api.github.com/repos/" + github_username + "/" + name, headers=token_header).text


def push_gitlab(name, import_url):
    token_header = {"PRIVATE-TOKEN": gitlab_token}
    params = {"name": name, "import_url": import_url}
    return requests.post(gitlab_url + "/api/v4/projects", headers=token_header, params=params, verify=False).text


def push_starred():
    page_num = 0
    while True:
        stars = get_stars(page_num)
        if len(stars) == 0:
            break
        for repo in stars:
            name = repo["name"]
            url = repo["html_url"]
            push_gitlab(name, url)
        page_num += 1


def push_forked(delete=False):
    page_num = 0
    while True:
        repos = get_repos(page_num)
        if len(repos) == 0:
            break
        for repo in repos:
            name = repo["name"]
            url = repo["html_url"]
            forked = repo["fork"]
            if forked == True:
                push_gitlab(name, url)
                if delete == True:
                    delete_github_repo(name)
        page_num += 1


push_forked(True)
push_starred()
