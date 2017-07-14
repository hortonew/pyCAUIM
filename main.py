""".

CA UIM API
Author: Erik Horton

"""
import requests
from globalvars import USER, PASSWORD, HEADERS, SITE, DOMAIN, HUB, ROBOT, PRIMARYHUB_PATH
from lxml import etree

def get_xml_item(text, path):
    """Convert xml string to entry"""
    try:
        xml = text
        xml = xml.encode('utf16')
        root = etree.XML(xml)
        item = root.xpath(path)[0].text
        return True, item
    except:
        return False, ""

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

    status, computer_system_id = get_xml_item(r.text, '/computer_systems/computer_system/cs_id')
    return status, computer_system_id

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
        return response.text
    except:
        return "Request of invoke_callback failed."



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

def epoch_to_time_fields(epoch):
    """Convert epoch to mon/day/year/hour/min/sec"""
    import time
    t = time.localtime(epoch)
    month = t.tm_mon
    day = t.tm_mday
    year = t.tm_year
    hours = t.tm_hour
    minutes = t.tm_min
    seconds = t.tm_sec
    return month, day, year, hours, minutes, seconds

def maintenance_mode_create_schedule(name, desc, start_epoch, end_epoch):
    """Define a mainteannce_mode schedule"""
    api_call = SITE + "/rest/maintenance_mode" + PRIMARYHUB_PATH + "/add_schedule"
    s_month, s_day, s_year, s_hours, s_min, s_sec = epoch_to_time_fields(start_epoch)
    e_month, e_day, e_year, e_hours, e_min, e_sec = epoch_to_time_fields(end_epoch)
    data = {
        "name": name,
        "description": desc,
        "start_date_time": {
            "month": s_month,
            "day": s_day,
            "year": s_year,
            "timestamp": {
                "hours": s_hours,
                "minutes": s_min,
                "seconds": s_sec
            }
        },
        "end_time": {
            "type": "end_date_time", 
            "end_date_time": {
                "month": e_month,
                "day": e_day,
                "year": e_year,
                "timestamp": {
                    "hours": e_hours,
                    "minutes": e_min,
                    "seconds": e_sec
                }
            }
        }
    }
    try:
        response = requests.post(
            api_call,
            auth=(USER, PASSWORD),
            headers=HEADERS,
            json=data
        )

        status, schedule_id = get_xml_item(response.text, '/schedule/schedule_id')
        return status, schedule_id
    except:
        return False, "Request of maintenance_mode_create_schedule failed."

def maintenance_mode_add_to_schedule(schedule_id, cs_id):
    """Adds cs_id (list) to schedule_id"""
    api_call = SITE + "/rest/maintenance_mode" + PRIMARYHUB_PATH + "/add_computer_systems_to_schedule/" \
        + schedule_id
    data = {
        "cs": cs_id
    }
    try:
        response = requests.post(
            api_call,
            auth=(USER, PASSWORD),
            headers=HEADERS,
            json=data
        )
        return True, response.text
    except:
        return False, "Failed to add computers to schedule"

def maintenance_mode_task(
    change,
    computers,
    start_epoch,
    end_epoch
):
    """Build a maintenance period and add hosts"""
    cs_id_list = list()
    name = "Change control: " + change
    description = "Built by script"
    for computer in computers:
        gcsi_status, c_id = get_computer_system_id(computer)
        if gcsi_status:
            cs_id_list.append(c_id)
            print("Added " + computer + " - " + c_id + " to computer list")

    mmcs_status, s_id = maintenance_mode_create_schedule(name, description, start_epoch, end_epoch)
    if mmcs_status:
        print("Created maintenance schedule")
        mmats_status, response = maintenance_mode_add_to_schedule(s_id, cs_id_list)
        print("Successfully completed change control disable")

def stop_maintenance_mode(robot, hub):
    """Stop maintenance on robot."""
    return maintenance_mode(robot, 0, 0)

def verify_maintenance_mode(robot, hub, start_epoch, end_epoch):
    """Description: Verify maintenance mode schedule."""
    return True
