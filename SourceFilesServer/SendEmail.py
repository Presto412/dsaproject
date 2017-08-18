import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
def SendEmail(regno,day,toaddr,time,now,ven): 
    fromaddr = "dsa16bcemohank@gmail.com"
    toaddr = toaddr 
    msg = MIMEMultipart() 
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "DESK DUTIES FOR "+str(day)+" as assigned on "+str(now)
    bodystr=''
    headstr="Time \tVenue\n"
    body = headstr+time
    msg.attach(MIMEText(body,'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "DSAPROJECT")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

