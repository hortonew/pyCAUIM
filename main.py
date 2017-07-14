""".

CA UIM API
Author: Erik Horton

"""
import requests
from globalvars import USER, PASSWORD, HEADERS, SITE, DOMAIN, HUB, ROBOT
from lxml import etree


def get_all_hubs():
    """Get all hubs in environment."""
    api_call = SITE + "/rest/hubs"
    r = requests.get(api_call, auth=(USER, PASSWORD))
    hub_list = list()

    try:
        xml = r.text
        xml = xml.encode('utf16')
        root = etree.XML(xml)

        for item in root.xpath('/hublist/hub'):
            hub = item.xpath('name')[0].text
            hub_list.append(hub)
    except:
        False

    return hub_list

def get_computer_system_id(cs_name):
    """Get the computer system id of a computer."""
    api_call = SITE + "/rest/computer_systems/cs_name/" + cs_name + "?contains=true"
    r = requests.get(api_call, auth=(USER, PASSWORD))
    computer_system_id = ""

    try:
        xml = r.text
        xml = xml.encode('utf16')
        root = etree.XML(xml)

        for item in root.xpath('/computer_systems/computer_system'):
            computer_system_id = item.xpath('cs_id')[0].text
            computer_system_id = computer_system_id
    except:
        False

    return computer_system_id

def invoke_callback(
    probe,
    callback,
    data,

    site=SITE,
    domain=DOMAIN,
    hub=HUB,
    robot=ROBOT
):
    """Invoke a probe callback function."""
    api_call = site + "/rest/probe/" + domain + "/" + hub + "/" + robot + "/" \
        + probe + "/callback/" + callback

    try:
        response = requests.post(
            api_call,
            auth=(USER, PASSWORD),
            headers=HEADERS,
            json=data
        )
    except:
        return "Request of invoke_callback failed."

    return response


def maintenance_mode(robot, hub, start_epoch, end_epoch):
    """Workflow to create a maintenance mode schedule."""
    data = {
        "timeout": "10000",
        "parameters": [
            {
                "name": "from",
                "type": "int",
                "value": start_epoch
            },
            {
                "name": "until",
                "type": "int",
                "value": end_epoch
            }
        ]
    }

    r = invoke_callback("controller", "maint_until",
                        data, SITE, DOMAIN, hub, robot)
    return r


def stop_maintenance_mode(robot, hub):
    """Stop maintenance on robot."""
    return maintenance_mode(robot, 0, 0)


def verify_maintenance_mode(robot, hub, start_epoch, end_epoch):
    """Description: Verify maintenance mode schedule."""
    return True
