import flask
from flask import request, jsonify
import requests
from flask import Flask
import json
import smtplib
import boto3
from botocore.exceptions import ClientError
import pyjade
from jinja2 import Environment, FileSystemLoader
from flask import render_template
import os

SENDER = "Source.SupplyVan.com (AL HATIMI Trading LLC)<source@supplyvan.com>"
AWS_REGION = "us-east-1"

URL = 'https://user-service-dot-turing-terminus-224612.el.r.appspot.com/api/find-user-by-brand-category'    
# URL = 'http://localhost:2000/api/find-user-by-brand-category'    
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# The subject line for the email.
SUBJECT = "Receive RFX"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Receive RFX")

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)

def sendMail(BODY_HTML, recipient):
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': recipient,
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

def prepareForSendMail():
    request_json = request.json 
    # print('request_json = ', request_json)
    # print('request_json.total_lineItems = ', request_json["total_lineItems"])
    user_name = ""
    rfx_name = request_json["rfx_name"]
    totalLineItems = request_json["total_lineItems"]
    titalQuantity = request_json["total_quantity"]
    BODY_HTML = render_template('reciveRFX.html', user_name=user_name, rfx_name=rfx_name, totalLineItems=totalLineItems, titalQuantity=titalQuantity)
    
    try:
        # getting mailids from related users having same brand and category
        response = requests.post(URL, data = json.dumps(request_json), headers = headers)

    # email should send to the this data
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err) 

    json_res = json.loads( response.text )
    # Try to send the email.
    recipient = []
    for x in json_res:
        recipient.append(x["email"])  
    sendMail(BODY_HTML, recipient)
    
    return "emails sent successfully to all related vendors!!"