# Smart Cities Project

## Setup
After cloning the repo you have to create your own ``config.py`` file by copying ``config.sample.py`` and renaming it to ``config.py``.
In ``config.py`` enter the information for your local RabbitMQ server, user and vhost.


## RabbitMQ Setup
Create the virtual host sc:
1. Go to ``http://localhost:15672/#/vhosts``
2. Add new virtual host Name: ``sc``
3. Click on the newly created vhost ``sc`` and grant your user permissions ``.*`` for configure/write/read.

Naming conventions:
- vhost is named ``sc``
- the topic exchange is name ``sc.topic``
- sensor producer P publishes with routing key ``building.floor.room.type.subtype.id`` where type could be ``sensor`` and subtype ``temperature``.
- queue Q is named e.g. ``sc.type.subtype`` 
- queue Q is bound to a routing key, here a few examples: 
```bash
*.*.*.sensor.*.* (Listen to sensors in all buildings)
*.*.*.sensor.temperature.* (Listen to all temperature sensors in all buildings)
U38.*.*.sensor.temperature.* (Listen to all temperature sensors in building U38)
```