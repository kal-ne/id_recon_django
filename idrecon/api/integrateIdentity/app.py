import json
from idrecon.models import Contact

def handler(event):
    body = json.loads(event.body)
    contactResp = {
        "primaryContactID": 0,
        "emails": [].append(body["email"]),
        "phoneNumbers": [].append(body["phoneNumber"]),
        "secondaryContactIds": []
    }
    resp = {"contact": contactResp}
    return resp