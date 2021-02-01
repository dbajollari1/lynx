from mailjet_rest import Client
from flask import current_app as app


#send email using MailJet API (mailjet-rest==1.3.3)
def send_email(subject, recipientsString, text_body, html_body):
    try:
        fromName = "LynX"
        fromEmail = app.config['MJ_EMAIL'] # has to vailid email registered with mailject
        api_key = app.config['MJ_APIKEY_PUBLIC']
        api_secret = app.config['MJ_APIKEY_PRIVATE']
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')

        #create list of recipients in JSON format
        # "To": [
        #     {
        #         "Email": 'abc@xyz.com',
        #         "Name": ""
        #     }
        # ],

        recipientsArray = []
        if (recipientsString.find(';') == -1): #single recipient
            recipientsArray.append({"Email": recipientsString})
        else: #multipe receipents with ';' as delimiter
            recipientsList = recipientsString.split(';')
            for recipient in recipientsList:
                recipientsArray.append({"Email": recipient})

        data = {
            'Messages': [
                {
                    "From": {
                        "Email": fromEmail,
                        "Name": fromName
                    },
                    "To": recipientsArray,
                    "Subject": subject,
                    "TextPart": text_body,
                    "HTMLPart": html_body
                }
            ]
        }
        result = mailjet.send.create(data=data)
        print(result.status_code)
        # vprint(result.json())
    except Exception as e:
        app.logger.error('***SEND EMAIL FAILED***' + str(e), extra={'user': ''})