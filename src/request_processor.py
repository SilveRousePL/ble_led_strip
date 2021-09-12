import json
from message_composer import MessageComposer

f = open('config.json',)
config = json.load(f)

def json_to_action(json_str):
    data = json.loads(json_str)

    device = data['device']
    address = config['devices'][device]

    command = data['command']
    value = data['value']
    mc = MessageComposer()
    mc_command_method = getattr(mc, command)
    result = mc_command_method(value)

    return (address, result)
