import time
from enum import Enum
from threading import Thread

from utils.planner_utils import *
import requests
import json


class Mode(Enum):
    solve = 'solve'
    validate = 'validate'
    solve_and_validate = 'solve_and_validate'


solve_url = 'http://solver.planning.domains/solve'
validate_url = 'http://solver.planning.domains/validate'
solve_and_validate = 'http://solver.planning.domains/solve-and-validate'

old_status = None

def update_problem_file_objects(name, objects=None):
    """
    Updates the problem pddl file and changes the objects
    :param name: name of the pddl file
    :param objects: objects block to insert
    :return:
    """
    with open('./pddl_data/' + name + '.pddl', 'r') as f:
        problem = f.read()
        start = problem.find('(:objects')
        end = problem.find('(:init')
        if not objects:
            objects = problem[start:end]
        new_pddl = problem[:start] + objects + problem[end:]

    with open('./pddl_data/' + name + '.pddl', 'w+') as f:
        f.write(new_pddl)


def update_problem_file_init(name, init=None):
    """
    Updates the problem pddl file and changes the init
    :param name: name of the pddl file
    :param init: init block to insert
    :return:
    """
    with open('./pddl_data/' + name + '.pddl', 'r') as f:
        problem = f.read()
        start = problem.find('(:init')
        end = problem.find('(:goal')
        if not init:
            init = problem[start:end]
        new_pddl = problem[:start] + init + problem[end:]

    with open('./pddl_data/' + name + '.pddl', 'w+') as f:
        f.write(new_pddl)


def update_problem_file_goal(name, goal=None):
    """
    Updates the problem pddl file and changes the init
    :param name: name of the pddl file
    :param init: init block to insert
    :return:
    """
    with open('./pddl_data/' + name + '.pddl', 'r') as f:
        problem = f.read()
        start = problem.find('(:goal')
        end = -1
        if not goal:
            goal = problem[start:end]
        new_pddl = problem[:start] + goal + problem[end:]

    with open('./pddl_data/' + name + '.pddl', 'w+') as f:
        f.write(new_pddl)


def get_solver_api_response(domain, problem, mode=None):
    """

    API Call to the Solver API to solve the problem given the problem and domain pddl-files

    :param domain:
    :param problem:
    :param mode:
    :return:
    """
    data = load_pddl_data(domain, problem)

    if not mode or mode == Mode.solve:
        resp = json.loads(requests.post(solve_url, verify=False, json=data).text)
    elif mode == Mode.solve_and_validate:
        resp = json.loads(requests.post(solve_and_validate, verify=False, json=data).text)

    return resp


def get_plan(domain, problem):
    """
    Makes an api post request for the defined domain and problem and saves the plan in the response of the solver
    :param domain: domain file name
    :param problem: domain problem name
    :return:
    """
    resp = get_solver_api_response(domain=domain, problem=problem)

    if (resp['status'] == 'ok'):
        plan = '\n'.join([act['name'] for act in resp['result']['plan']])
        plan_name = get_problem_name(resp)
        save_plan(plan_name, plan)
    else:
        plan = ""
        if isinstance(resp['result'], str):
            print(resp['result'])
            print("AI Planner Server busy")
            plan_name = "server_busy"
        else:
            if 'FALSE' in str(resp['result']['output']):
                print("No plan found")
            elif 'TRUE' in str(resp['result']['output']):
                print("No plan needed")
            else:
                print(str(resp['result']['output']))
            plan_name = resp['status']
    return plan_name, plan


def start_planning(domain, problem):
    successful = False
    time_out = 1
    while not successful:
        plan_name, plan = get_plan(domain=domain, problem=problem)
        if plan_name == 'server_busy':
            time.sleep(time_out)
            time_out *= 2
        elif plan_name == 'error':
            plan_name = 'default'
            break
        else:
            break
    return plan_name, plan



def start():
    Thread(target=start_planning, args=[]).start()


if __name__ == '__main__':
    start()
