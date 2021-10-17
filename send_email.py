#!/usr/bin/python
import configparser
import boto3
from botocore.exceptions import ClientError
import time

creds = configparser.ConfigParser()
creds.read('credentials.ini')

AWS_ACCESS_KEY_ID = creds['default']['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = creds['default']['aws_secret_access_key']
AWS_REGION = "us-east-1"
CONFIGURATION_SET = "ConfigSet"

class Email:

    def __init__(self, sender, recipients=[]):
        self.client = boto3.client('ses',
                                   region_name=AWS_REGION,
                                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                                   )
        self.sender = sender
        self.recipients = recipients

    def __body(self, body, is_html):
        content = ""
        if is_html:
            content = {
                'Html': {
                    'Charset': "UTF-8",
                    'Data': body,
                }
            }
        else:
            content = {'Text': {
                'Charset': "UTF-8",
                'Data': body,
            }}
        return content

    def send_mail(self, subject, body, is_html=False):
        body_json_content = self.__body(body, is_html)
        try:
            response = self.client.send_email(
                Source=self.sender,
                Destination={
                    'ToAddresses': self.recipients,
                },
                Message={
                    'Body': body_json_content,
                    'Subject': {
                        'Charset': "UTF-8",
                        'Data': subject,
                    }
                },
                ConfigurationSetName=CONFIGURATION_SET
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email successfully sent! Message ID:"),
            print(response['MessageId'])

recipient_list = ["recipient@pauvar.com", "bounce@pauvar.com", "complaint@simulator.amazonses.com"]

for recipient in recipient_list:
    email = Email("sender@pauvar.com", [recipient])
    email.send_mail(subject="pauvar.com test email incoming", body="Hi again!", is_html=True)
    print("Email sent to: " + recipient)
    time.sleep(1)
