#!/usr/bin/python3
''' Script that request to API Holberton checkers
'''
import requests
import sys
import time
import json


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


def read_json():
    """Function to read the config.json file"""
    try:
        with open('config.json', 'r') as json_file:
                data = json.load(json_file)
        return (data)
    except Exception:
        print("Please run the option 2 of the setup script to create the config.json file")
        sys.exit(0)

def get_token():
    try:
        data = read_json()
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
        print("")
        print("*"*30)
        print("\n{}\n".format(project['name']))
        print("*"*30)
        corrects_l = []
        for task in tasks_asked:
            corrects_d = {}
            correction = ask_correction(token, task["id"])
            result = {"status": "Send"}
            print("\nWe are generating correction for task - {}\n".format(task["title"]))
            while (result["status"] != "Done"):
                result = get_correction(token, correction)
                print("wait for 6 seconds more.....")
                time.sleep(6)
            """  Call function to display the checker result"""
            corrects_d['title'] = task['title']
            corrects_d['result'] =result
            corrects_l.append(corrects_d)
        print_result(corrects_l)

def print_result(corrects_l):
    for correct in corrects_l:
        passed = 0
        checkers = correct['result'].get('result_display')['checks']
        num_checks = len(checkers)
        for check in checkers:
            if check['passed'] == True:
                passed += 1
        print("\n")
        print("\t* Task: {} - {}/{} checkers validated\n".format(correct['title'], passed, num_checks))
        if passed == num_checks:
            print("\t \U0001f600 \U0001f600 Congratulations, You earn a candy!!! \U0001f600 \U0001f600 \n")


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
