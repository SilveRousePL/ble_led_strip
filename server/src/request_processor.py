import json
import config
from message_composer import MessageComposer

def data_validator(json_str):
    return True

def get_action(json_str):
    data = json.loads(json_str)

    device = data['device']
    address = config.get_config()['devices'][device]

    command = data['command']
    value = data['value']
    mc = MessageComposer()
    mc_command_method = getattr(mc, command)
    result = mc_command_method(value)

    return (address, result)
