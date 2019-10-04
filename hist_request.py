#!/usr/bin/python3
''' Script that request to API Holberton checkers
'''
import requests
import sys


project = sys.argv[1]
if len(sys.argv) == 3:
    task = sys.argv[2]
else:
    task = ""


def getToken():
    try:
        data = {
            'api_key': '3e70739a1d341fb95b66fddc5650b1f6',
            'email': '@holbertonschool.com',
            'password': '',
            'scope': 'checker'}
        url_aut = 'https://intranet.hbtn.io/users/auth_token.json'
        aut = requests.post(url_aut, data)
        aut = aut.json()
        if aut:
            token = aut.get('auth_token')
        print(aut)
        print(token)
    except Exception:
        print('Not a valid JSON')
    return token


def getProject(project, token):
    try:
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
        print('Not a valid JSON')
    return proj_dict


def getTask(task, token):
    try:
        if task == "":
            print("estoy vacio")
        else:
            print(task)
            url_task = 'https://intranet.hbtn.io/tasks/' + task + '.json'
            print(url_task)
            data = {'auth_token': token}
            req = requests.get(url_task, data)
            req = req.json()
            if req:
                print(req)
    except Exception:
        print('Not a valid JSON')


''' Get token for requests '''
tok = getToken()
''' Get project id and name '''
proj = getProject(project, tok)
print(proj)

''' Get task for project  iterate over proj.tasks
this attribute have a position of a task '''
print(task)
tasks = getTask(task, tok)
