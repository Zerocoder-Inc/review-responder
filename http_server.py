from fastapi import FastAPI
from schemas.schemas import Message, Request_model
import os
from dotenv import load_dotenv
from utils.request import get_requests_handler, post_requests_handler

load_dotenv()

# account_sid = os.getenv("TWILIO_ACCOUNT_SID")
# auth_token = os.getenv('TWILIO_AUTH_TOKEN')
xano_add_sms = os.getenv("XANO_ADD_SMS")
xano_post_edit_sms = os.getenv("XANO_POST_EDIT_SMS")
xano_access_token = os.getenv("XANO_ACCESS_TOKEN")

params_for_xano = {
    'access_token': xano_access_token,
}

app = FastAPI()


#webhook for updating status in db by sid
@app.post("/MessageStatus")
def incoming_sms(request):
    message_sid = request.get('MessageSid', None)
    message_status = request.get('MessageStatus', None)
    if message_sid is not None and message_status is not None:
        json_data = {
          "sid": message_sid,
          "status": message_status
        }
        json_data.update(params_for_xano)
        response = post_requests_handler(url=xano_post_edit_sms, json=json_data)
        if response["status"] == "success":
            pass

    return ('', 204)

# webhook for getting answer sms from users

# webhook

