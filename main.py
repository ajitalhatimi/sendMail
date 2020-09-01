import flask
from flask import request, jsonify
import requests
from flask import Flask
import json
import smtplib
import boto3
from botocore.exceptions import ClientError
import pyjade
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from flask import render_template
import os

env = Environment(
    loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)))

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "Sender Name <source@supplyvan.com>"

# Replace recipient@example.com with a "To" address. If your account 
# is still in the sandbox, this address must be verified.
RECIPIENT = "ajit@alhatimi.com"

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the 
# ConfigurationSetName=CONFIGURATION_SET argument below.
# CONFIGURATION_SET = "ConfigSet"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-east-1"


app = Flask(__name__)
app.config["DEBUG"] = True
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

attributesList = {
    "brands": ["brand1", "brand2", "brand3", "brand4", "brand5"],
    "category": ["category1", "category2", "category3", "category4", "category5"]
}
URL = 'https://user-service-dot-turing-terminus-224612.el.r.appspot.com/app/signup'    
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# The subject line for the email.
SUBJECT = "Amazon SES Test (SDK for Python)"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )
            
# The HTML body of the email.
# BODY_HTML = """<html>
# <head></head>
# <body>
#   <h1>Amazon SES Test (SDK for Python)</h1>
#   <p>This email was sent with
#     <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
#     <a href='https://aws.amazon.com/sdk-for-python/'>
#       AWS SDK for Python (Boto)</a>.</p>
# </body>
# </html>
#     """            

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)

@pyjade.register_filter('capitalize')
def capitalize(text,ast):
  return text.capitalize()
  
def sendMail(BODY_HTML):
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

@app.route('/sendMail', methods=['POST'])
def prepareForSendMail():
    request_json = request.json
    print('request_json = ', request_json)
    # f = open("reciveRFX.html", "r")
    # BODY_HTML = f.read()
    # print('file content  = ',f.read())
    user_name = "Ajit Shinde"
    rfx_name = "sending the mail for RFX send"
    totalLineItems = "100"
    titalQuantity = "100"
    BODY_HTML = render_template('reciveRFX.html', user_name=user_name, rfx_name=rfx_name, totalLineItems=totalLineItems, titalQuantity=titalQuantity)

    print('==============================')
    print(render_template('reciveRFX.html', user_name=user_name, rfx_name=rfx_name, totalLineItems=totalLineItems, titalQuantity=titalQuantity) )
    print('==============================')
    
    # print('converting the file = ',capitalize(f.read(), "ast") )
    # try:
    #     # getting mailids from related users having same brand and category
    #     response = requests.post(URL, data = json.dumps(attributesList), headers = headers)

    #     //email should send to the this data
    #     response.raise_for_status()
    # except requests.exceptions.HTTPError as errh:
    #     print ("Http Error:",errh)
    # except requests.exceptions.ConnectionError as errc:
    #     print ("Error Connecting:",errc)
    # except requests.exceptions.Timeout as errt:
    #     print ("Timeout Error:",errt)
    # except requests.exceptions.RequestException as err:
    #     print ("OOps: Something Else",err) 

    # print("api Responce response.status_code : ", response.status_code)
    # print("api Responce response.status_code : ", response.text)
    # print("api Responce : ", response.json())
    # Try to send the email.
    sendMail(BODY_HTML)
    
    
    return json.dumps(request_json)


app.run()

