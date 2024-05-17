from mailjet_rest import Client
import os
import dotenv

dotenv.load_dotenv()

api_key = os.getenv('MAILJET_API_KEY')
api_secret = os.getenv('MAILJET_SECRET_KEY')
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
  'Messages': [
    {
      "From": {
        "Email": "idimnovdie1602@protonmail.com",
        "Name": "Iván Dima"
      },
      "To": [
        {
          "Email": "idimnovdie1602@protonmail.com",
          "Name": "Iván Dima"
        }
      ],
      "Subject": "Greetings from Mailjet.",
      "TextPart": "My first Mailjet email",
      "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
      "CustomID": "AppGettingStartedTest"
    }
  ]
}
result = mailjet.send.create(data=data)
print(result.status_code)
print(result.json())
