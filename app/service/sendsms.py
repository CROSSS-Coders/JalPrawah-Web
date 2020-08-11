import http.client
from app.setting import MSG91_KEY
import requests

def send_sms(message,user):
    # print(users)
    # payload = {
    #     "flow_id": "5f23dd91d6fc054ee346a349",
    #     "sender": "msgind",
    #     "recipients": users
    # }
    # headers = {
    #     "authkey": str(MSG91_KEY),
    #     "content-type": "application/json"
    # }
    # print(payload,MSG91_KEY)
    url='https://api.msg91.com/api/sendhttp.php?Group_id=group_id&authkey=auth_key&mobiles='+str(user.mobile)+'&country=91&message='+message+'&sender=TESTIN&route=4'
    print(url)
    r = requests.get(url)
    print(r.text,r.status_code)
    return 'Done'

