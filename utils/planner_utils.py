import re

sed = 'slios_environment_domain'
sep = 'slios_environment_problem'
sdd = 'slios_distribution_domain'
sdp = 'slios_distribution_problem'

def load_plan(name):
    """
    Loads the plan and returns a list of actions
    :param name: name of the plan
    :return: list of actions
    """
    with open('./pddl_data/' + name + '.plan', 'r') as f:
        actions = f.read()
    return actions


def save_plan(name, plan):
    """
    Saves the plan
    :param name: name of the plan file
    :param plan: plan from the solver
    :return:
    """
    with open('./pddl_data/' + name + '.plan', 'w+') as f:
        f.write(plan)


def get_problem_name(response):
    """
    Returns a name for the plan file by extracting the problem name out of the response
    :param response:
    :return:
    """
    name = [line.split()[1] for line in response['result']['output'].split('\n') if 'Problem' in line][0].lower()
    return name


def load_pddl_data(domain, problem):
    """
    Returns the data dictionary required for the api call. It includes the domain and problem definition
    :param domain: domain file name
    :param problem: problem file name
    :return: data dictionary object for api call
    """
    data = {'domain': open('./pddl_data/'+domain+'.pddl', 'r').read(),
            'problem': open('./pddl_data/'+problem+'.pddl', 'r').read()}
    return data


def plan_to_list(plan):
    """
    Transforms the plan into an iterable list of actions
    :param plan:
    :return:
    """
    return re.sub('[()]', '', plan).split('\n')