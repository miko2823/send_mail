import datetime
import smtplib
import sys
from email.mime.text import MIMEText
from email.utils import formatdate

if len(sys.argv) < 2:
    print('Please input mode "start" or "end"')
    sys.exit()
mode = sys.argv[1]

FROM_ADDRESS = '@gmail.com'
MY_PASSWORD = ''
TO_ADDRESS = '@ae.auone-net.jp'
BCC = ''

now = datetime.datetime.now()
date = now.strftime('%Y/%m/%d')

if mode == "start":
    job_time = now.strftime('%H:%M ~ call_hour:%M')
    call_hour = int(now.strftime('%H'))+9
    job_time = job_time.replace('call_hour', str(call_hour))
    with open("job_time.txt", "w") as f:
        f.write(job_time)
elif mode == "end":
    with open("job_time.txt", "r") as f:
        job_time = f.read()

mode_subject = "作業開始" if mode == "start" else "作業完了"
mode_time = "作業予定" if mode == "start" else "作業時間"
mode_time2 = "作業スケジュール" if mode == "start" else "作業実績"


SUBJECT = f'【{mode_subject}】{date} 中嶋かおり'
with open('mail_body.txt', 'r') as f:
    job = f.read()
    job = job.replace('{job_time}', job_time)

BODY = f"""{mode_time}：{job_time}
休憩：14:00 ~ 15:00

<{mode_time2}>
{job}


<申し送り事項>
なし"""


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
    print('***Remote Working Format***')
    print(BODY)
    val = input()
    if val == "y":
        send(FROM_ADDRESS, to_addr, msg)
    else:
        sys.exit()

