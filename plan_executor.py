import eel

from mq.Producer import Producer
import json

from utils import load_plan, plan_to_list


class Executor:
    def __init__(self):
        self.function = 'execute'
        self.id = 'executioner_0'
        self.typ = 'executioner'

        self.producer = Producer()

        self.producer.channel.exchange_declare(exchange=self.producer.exchange, exchange_type="topic", durable=True,
                                               auto_delete=False)

    def getRoutingKey(self):
        return "*.*.executioner.*.*.*"

    def getResponse(self):
        msg = {'function': self.function, 'id': self.id, 'type': self.typ, 'value': None}
        return msg

    def send(self, value):
        resp = self.getResponse()
        resp['value'] = value
        message = json.dumps(resp)

        self.producer.channel.basic_publish(exchange=self.producer.exchange, routing_key=self.getRoutingKey(),
                                            body=message)

    def execute_plan(self, plan_name):
        """
         Goes through the new plan and sends the actions for the affected actuators to the gateway
        :param plan_name:
        :return:
        """
        actions = plan_to_list(load_plan(plan_name))
        print(str(actions))
        for action in actions:
            command = action.split()
            method = command[0]

            room = ''
            status = False
            if method == 'climate-on':
                room = command[2]
                status = True
            elif method == 'climate-off':
                room = command[2]
                status = False
            elif method == 'keep-climate-on':
                continue
            elif method == 'window-open':
                room = command[2]
                status = True
            elif method == 'window-close':
                room = command[2]
                status = False
            elif method == 'keep-window-open':
                continue
            elif method == 'light-on':
                room = command[1]
                status = True
            elif method == 'light-off-low':
                room = command[1]
                status = False
            elif method == 'light-off-high':
                room = command[1]
                status = False
            elif method == 'reduce-sound-level':
                table = command[1].replace("t", "")
                status = True
            elif method == 'set-weathersafe':
                continue
            elif method == 'keep-light-off':
                continue
            elif method == 'keep-light-on':
                continue

            if method == 'even-distributed-reset':
                continue
            elif method == 'place-person-on-chair':
                person = command[1]
                room = command[2]
                chair = command[3]
                status = chair.replace("c", "")
            elif method == 'reject-new-person-because-full':
                continue

            actuator = ""
            if 'window' in method:
                actuator = 'window'
            elif 'light' in method:
                actuator = 'light'
            elif 'climate' in method:
                actuator = 'climate'
            elif 'sound' in method:
                actuator = 'sound_level'
            elif 'person' in method:
                actuator = 'place_person'

            if 'sound' in method:
                actuator += "_" + str(int(table) - 1)
            elif room == "":
                actuator = None
            elif 'person' in method:
                actuator += "_" + str(int(status) - 1)
            else:
                room = str(int(room.replace("r", "")) - 1)
                actuator += "_" + room

            if (hasattr(eel, "setText")):
                data = {'actuator': actuator, 'status': status}
                msg = {'sender': 'plan_executioner', 'data': data}
                eel.setText("plan", json.dumps(msg))

            self.send({'actuator': actuator, 'status': status})
