"""General page routes."""


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import request
import json

from .. import db
from .. import app_ref


def record_save(ip):
    from datetime import datetime
    from urllib.request import urlopen
    from .model_ip import IP

    # agent = request.user_agent()
    request_url = 'https://ipapi.co/{}/json'.format(
        ip)+'/?key=QCM5ry3Xw1kC1xrNrXZKzaZRXhhxywi67F8eSTgVDnnSMn64Lu'

    # store the response of URL
    response = urlopen(request_url)

    # storing the JSON response
    # from url in data
    data_json = json.loads(response.read())

    ip = IP(
        page=request.endpoint,

        ip=data_json['ip'],
        city=data_json['city'],
        region=data_json['region'],
        country_name=data_json['country_name'],
        country_capital=data_json['country_capital'],
        timezone=data_json['timezone'],
        latitude=data_json['latitude'],
        longitude=data_json['longitude'],
        org=data_json['org'],

        browser=request.user_agent.string
    )

    db.session.add(ip)
    db.session.commit()

    time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    ip = data_json['ip']
    ip_url = "https://ipapi.co/{}/json".format(data_json['ip'])
    address = data_json['city'] + '/' +\
        data_json['region'] + '/' + data_json['country_name']
    map = "https://www.google.com/maps/search/?api=1&query={0},{1}".format(
        str(data_json['latitude']), str(data_json['longitude']))

    browser = request.user_agent.string

    # email_notice(time, ip, ip_url, address, map, browser)


def email_notice(time, ip, ip_url, address, map, browser):
    import smtplib
    import ssl

    subject = "全栈IT Development访问！"

    html_1 = """<html>
    <head>
      <title>{subject}</title>
      <style>table {font-family: Garamond;background-color: white;border-collapse: collapse;text-align: left;width: 100%;}table caption {font-size: 24px;font-weight: bold;color: #5f0000;margin-bottom: 20px;}table thead th {background-color: #005f5f;color: white;white-space: nowrap;padding: 9px 5px;font-size: 18px;text-shadow: 1px 1px 2px #aaa;border: 1px solid black;}table tbody td {font-family: Garamond;border: 1px solid #afaf00;padding: 5px;font-size: 16px;}table tbody tr:nth-child(even) {background-color: #aaa;}table tbody tr:hover {background-color: #afaf00;}</style>
    </head>"""
    html_2 = f"""<body><main><table class="table table-dark table-striped"><caption>{subject}</caption> <thead><tr><th>Time<th>IP<th>Address<th>ISP<th>Browser</thead><tbody><tr><td>{time}</td><td><a href="{ip_url}" target='_blank'>{ip}</a></td><td style="color: red; font-weight: bold;">{address}</td><td><a href="{map}" target='_blank'>🌎</a></td><td>{browser}</td></tr></tbody></table></main></body></html>"""

    # 111, GMAIL SEND
    # sender_email = "nemo.xun.jin.wang@gmail.com"
    # receiver_email = "cocowang2014@protonmail.com"
    # global app_ref
    # password = app_ref.config["MY_GMAIL"]

    # 222, PROTONMAIL SEND
    global app_ref
    sender_email = app_ref.config["SENDER_EMAIL"]
    receiver_email = app_ref.config["RECEIVER_EMAIL"]
    password = app_ref.config["MY_OUTLOOK"]

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    # message.attach(MIMEText(text, "text"))
    message.attach(MIMEText(html_1+html_2, "html"))

    #
    text = message.as_string()

    # Log in to server using secure context and send email
    # 111, GMAIL SEND
    context = ssl.create_default_context()
    # with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_email, text)

    # 222, PROTONMAIL SEND
    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
