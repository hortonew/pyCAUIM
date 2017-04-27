Docs
http://docs.nimsoft.com/prodhelp/en_US/Monitor/SDK/REST/Nimsoft%20RESTful%20Webservices%20Manual%20and%20Reference%20Guide_v2_13.pdf

""".

Example globalvars.py

"""

USER = "test.username"
PASSWORD = "password123"
SITE = "http://myumpserver:8080"
DOMAIN = "myUIMDomain"
HUB = "examplehub"
ROBOT = "examplerobot"

# Used in post requests
HEADERS = {
    'X-Requested-With': 'Python requests',
    'Content-type': 'application/json'
}
