#!/usr/bin/python3
''' Script that request to API Holberton checkers
'''
import requests
import sys
import time


def print_help():
    print('help options')
    sys.exit(0)


def filter_task(all_tasks, task_required=[]):
    """ """
    aux = []
    if task_required == []:
        return all_tasks
    for i in range(len(all_tasks)):
        if i in task_required:
            aux.append(all_tasks[i])
    return aux


def get_token():
    try:
        data = {
            'api_key': '68005742a84467416325ec2636a47b5c',
            'email': '@holbertonschool.com',
            'password': '',
            'scope': 'checker'}
        url_aut = 'https://intranet.hbtn.io/users/auth_token.json'
        aut = requests.post(url_aut, data)
        aut = aut.json()
        if aut and aut.get('auth_token'):
            token = aut.get('auth_token')
        else:
            raise Exception
    except Exception:
        print('Are you sure you setup correctly your credentials in config.json?')
        sys.exit(0)
    return token


def get_project(token, project):
    try:
        if not token:
            token = get_token()
        url_project = 'https://intranet.hbtn.io/projects/' + project + '.json'
        data = {'auth_token': token}
        req = requests.get(url_project, data)
        req = req.json()
        if req:
            proj_dict = {
                "id": req.get('id'),
                "name": req.get('name'),
                'tasks': req.get('tasks')}
    except Exception:
        print('Are you sure you are checking a correct project?')
        sys.exit(0)
    return proj_dict


def ask_correction(token, task):
    url_correction = "https://intranet.hbtn.io/tasks/{}/start_correction.json".format(task)
    data = {'auth_token': token}
    res = requests.post(url_correction, params=data, data="")
    res = res.json()
    if res:
        return res["id"]
    else:
        print("Something is wrong asking for task {}".format(task["title"]))
        system.exit(0)


def get_correction(token, id):
    url_project = "https://intranet.hbtn.io/correction_requests/{}.json".format(id)
    data = {'auth_token': token}
    res = requests.get(url_project, data)
    res = res.json()
    return(res)


def get_checkers(token, project, tasks=[]):
    if project is None:
        print("You can't check an empty project")
    else:
        tasks_asked = filter_task(project["tasks"], tasks)
        for task in tasks_asked:
            correction = ask_correction(token, task["id"])
            result = {"status": "Send"}
            print("We are generating correction for task {}".format(task["title"]))
            while (result["status"] != "Done"):
                result = get_correction(token, correction)
                print("wait for 6 seconds more.....")
                time.sleep(6)
            """  create function to display the checker result"""
            print(result)

if len(sys.argv) == 1:
    print_help()
if sys.argv[1] == "help":
    print_help()
project = sys.argv[1]
tasks = []
if len(sys.argv) >= 3:
    if sys.argv[2] == '-t':
        tasks = sys.argv[3:] or []
    else:
        tasks = [sys.argv[2]]
    tasks = list(map(lambda x: int(x) if x.isnumeric() else x, tasks))
''' Get token for requests '''
tok = get_token()
''' Get project id and name '''
proj = get_project(tok, project)
checkers = get_checkers(tok, proj, tasks)
