#!/usr/bin/python3
''' Script that request to API Holberton checkers
'''
import requests
from flask import jsonify
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


def get_user(token):
    try:
        data = {'auth_token': token}
        url_usr = 'https://intranet.hbtn.io/users/me.json'
        usr = requests.get(url_usr, data)
        usr = usr.json()
        if usr:
            data_user = {}
            data_user['name'] = usr.get('full_name')
            data_user['id'] = usr.get('id')
        else:
            raise Exception
    except Exception:
        print('Are you sure you setup correctly your credentials in config.json?')
        sys.exit(0)
    return data_user


def save_user(data_user):
    try:
        with open('config.json', 'r') as json_file:
                data = json.load(json_file)
    except Exception:
        print('Are you sure you setup correctly your credentials in config.json?')
        sys.exit(0)
    api_user = {"id": data_user["id"], "name": data_user["name"], "email": data["email"], "password": data["password"]}
    url_api = 'http://0.0.0.0:5000/api/v1/users/'
    save = requests.post(url_api, json=api_user)
    print(save.status_code)
      

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


def save_project(project):
    api_project = {"id": project["id"], "name": project["name"]}
    url_api = 'http://0.0.0.0:5000/api/v1/projects/'
    save = requests.post(url_api, json=api_project)
    print(save.status_code)
    


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


def get_correction(token, id, project_id):
    url_project = "https://intranet.hbtn.io/correction_requests/{}.json".format(id)
    data = {'auth_token': token}
    res = requests.get(url_project, data)
    res = res.json()
    url_correction = 'http://0.0.0.0:5000/api/v1/corrections/'
    correction_exist = requests.get(url_correction)
    for corrections in correction_exist.json():
        if corrections['task_id'] == res['task_id']:
            requests.delete(url_correction + str(corrections["id"]))
    data_corrections = {"id": res['id'], "status": res['status'], "project_id": project_id, "task_id": res['task_id'], "user_id": res['user_id']}
    req = requests.post(url_correction, json=data_corrections)
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
                result = get_correction(token, correction, project["id"])
                print("wait for 6 seconds more.....")
                time.sleep(6)
            """  Call function to display the checker result"""
            corrects_d['title'] = task['title']
            corrects_d['result'] =result
            corrects_l.append(corrects_d)
        print_result(corrects_l, result['id'])

def print_result(corrects_l, correction_id):
    for correct in corrects_l:
        passed = 0
        checkers = correct['result'].get('result_display')['checks']
        num_checks = len(checkers)
        url_check = 'http://0.0.0.0:5000/api/v1/checks/'
        for check in checkers:
            check_exist = requests.get(url_check + str(check["id"]))
            if not check_exist: 
                data_checks = {"id": check['id'], "title": check['title'], "passed": check["passed"], "correction_id": correction_id}
                req = requests.post(url_check, json=data_checks)
            if check['passed'] == True:
                passed += 1
        print("\n")
        print("\t* Task: {} - {}/{} checkers validated\n".format(correct['title'], passed, num_checks))
        if passed == num_checks:
            print("\t \U0001f600 \U0001f600 Congratulations, You earn a candy!!! \U0001f600 \U0001f600 \n")
            url = 'http://192.168.8.215:5000/candy'
            rq = requests.get(url)
            rq = rq.json()
            print(rq)


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

''' Validate and Get id and user name '''
with open('config.json', 'r') as json_file:
    data = json.load(json_file)
id = data["email"][0:3]
usr_exist = 'http://0.0.0.0:5000/api/v1/users/'+str(id)
get_usr = requests.get(usr_exist)
if get_usr:
   pass
else:
    data_user = get_user(tok)
    ''' Save data User '''
    save_user(data_user)




''' Get project id and name '''
url_proj = 'http://0.0.0.0:5000/api/v1/projects/'+sys.argv[1]
proj = requests.get(url_proj)
if not proj:
   proj = get_project(tok, project)
   save_project(proj)


''' Get tasks '''
if tasks:
    proj = get_project(tok, project)
    tasks = filter_task(proj['tasks'], tasks)
    proj_id = proj['id']
    url_task = 'http://0.0.0.0:5000/api/v1/tasks/'
    for pr_task in tasks:
        if not requests.get(url_task + str(pr_task["id"])):
            data_task = {"id": pr_task['id'], "title": pr_task['title'], "project_id": proj_id}
            req = requests.post(url_task, json=data_task)
                

''' ********** Get Candy Checkers ******** '''
project = sys.argv[1] 
proj = get_project(tok, project)
checkers = get_checkers(tok, proj, tasks)
