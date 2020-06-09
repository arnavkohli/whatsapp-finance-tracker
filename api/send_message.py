# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC406df9a892b77b8c5e65a7973897c2e1'
auth_token = '2ee685d732631960bb8158ebf558c7ff'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='whatsapp:+14155238886',
                     to='whatsapp:+919820417721'
                 )

print(message.sid)



