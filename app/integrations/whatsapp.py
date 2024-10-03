from flask_restful import Resource
import requests


TOKEN = "EAAKmnPQb1esBO6dGIifnJpjoAt8Cok63K88Mj2NSwGwB8O4AAHnNeQkOZBgQqAkaEEs7FVTZBZB5t7gHuxliGZBK2HVlMj7WyuHgY5SdE3QMBWXgim9dASVYD43mOjW2p8oAEaUHdHrKxEUmoyMbZA44iNZCDycexjmH8FuQ40dIX4B62mNqrkV7tweMYWwUYf"

class Whatsapp(Resource):
    def __init__(self):
        pass
    def sendSMS(self):
        # data = flask_request.get_json(silent=True)
        phone_number = "+919361458719"
        message = "Hello This Is Testing Message"
        
        if phone_number and message:
            url = f"https://graph.facebook.com/v18.0/269592469567922/messages"
            headers = {
                'Authorization': f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": "919361458719",
                "type": "template",
                "template": { "name": "hello_world", "language": { "code": "en_US" } }
            }
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                return "Message sent successfully"
            else:
                return f"Failed to send message. Status code: {response.status_code}"
        else:
            return "Missing phone number or message in request"
