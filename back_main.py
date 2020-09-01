from smtplib import SMTP 
 
from jinja2 import Environment, FileSystemLoader
import os

env = Environment(
    loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)))

def get_data():
    data = []
    data.append(
        {
         "movies": [
             {         
                 "title": 'Terminator',
                 "description": 'One soldier is sent back to protect her from the killing machine. He must find Sarah before the Terminator can carry out its mission.'
             },
             {                 
                 "title": 'Seven Years in Tibet',
                 "description": 'Seven Years in Tibet is a 1997 American biographical war drama film based on the 1952 book of the same name written by Austrian mountaineer Heinrich Harrer on his experiences in Tibet.'
             },
             {               
                 "title": 'The Lion King',
                 "description": 'A young lion prince is born in Africa, thus making his uncle Scar the second in line to the throne. Scar plots with the hyenas to kill King Mufasa and Prince Simba, thus making himself King. The King is killed and Simba is led to believe by Scar that it was his fault, and so flees the kingdom in shame.'
             }
         ]
         })
    return data

def send_mail(bodyContent):
    to_email = 'to@gmail.com'
    from_email = 'from@gmail.com'
    subject = 'This is a email from Python with a movies list!'
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email

    message.attach(MIMEText(bodyContent, "html"))
    msgBody = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, 'your password')
    server.sendmail(from_email, to_email, msgBody)

    server.quit()

def send_movie_list(event, context):
    json_data = get_data()
    template = env.get_template('child.html')
    output = template.render(data=jsonData[0])
    send_mail(output)    
    return "Mail sent successfully."
    # import smtplib

# gmail_user = 'deepak@alhatimi.com'
# gmail_password = 'Mahanadi@5'

# sender = 'source@supplyvan.com'
# receivers = ['ajit@alhatimi.com', 'ajit77shinde@gmail.com']

# message = """From: From Person <from@fromdomain.com>
# To: To Person <to@todomain.com>
# Subject: SMTP e-mail test

# This is a test e-mail message.
# """

# try:
#     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     server.ehlo()
#     server.login(gmail_user, gmail_password)
#     server.sendmail(sender, receivers, message)  
#     print('Mail sent sucessfully....')       

# except Exception as ex:
#     print ('ex = ', ex)
#     print ('Something went wrong...')


# return "hii"

# Create some test data for our catalog in the form of a list of dictionaries.

# @app.route('/', methods=['GET'])
# def home():
#     return '''<h1>Distant Reading Archive</h1>
# <p>A prototype API for distant reading of science fiction novels.</p>'''


# # A route to return all of the available entries in our catalog.
# @app.route('/api/v1/resources/books/all', methods=['GET'])
# def api_all():
#     return jsonify(books)

# gmail_user = 'source@supplyvan.com'
# gmail_password = 'Mahanadi@4'

# sender = 'source@supplyvan.com'
# receivers = ['ajit@alhatimi.com', 'ajit77shinde@gmail.com']
# receivers = ['ajit@alhatimi.com', 'ajit77shinde@gmail.com', 'ajshinde77@gmail.com']

# message = """From: From Person <from@fromdomain.com>
# To: To Person <to@todomain.com>
# Subject: SMTP e-mail test

# This is a test e-mail message.
# """