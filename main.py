""".

CA UIM API
Author: Erik Horton

"""
import requests
from globalvars import USER, PASSWORD, HEADERS, SITE, DOMAIN, HUB, ROBOT
from hubs import get_all_hubs, identify_hub


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

    print api_call

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
    hubs = get_all_hubs()
    print hubs
    hub = identify_hub(robot)
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
