import datetime
import pyperclip
import smtplib
import sys
from email.mime.text import MIMEText
from email.utils import formatdate

FROM_ADDRESS = '@gmail.com'
MY_PASSWORD = ''
TO_ADDRESS = '@ae.auone-net.jp'
BCC = ''

now = datetime.datetime.now()
date = now.strftime('%Y年%m月%d日')
SUBJECT = f'【日報】{date} 中嶋'
# TODO with remote working mail
# job = pyperclip.paste()
with open('mail_body.txt', 'r') as f:
    job = f.read()
    job = job.replace('：{job_time}', '')

BODY = f"""**************
【日報】中嶋かおり({date})
**************
■ 作業
{job}

■課題/困っていること
なし

■ 連絡事項
なし

"""


def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    return msg


def send(from_addr, to_addrs, msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()


if __name__ == '__main__':

    to_addr = TO_ADDRESS
    subject = SUBJECT
    body = BODY
    msg = create_message(FROM_ADDRESS, to_addr, BCC, subject, body)
    print(BODY)
    val = input()
    if val == "y":
        send(FROM_ADDRESS, to_addr, msg)
    else:
        sys.exit()
