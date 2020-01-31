import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
import mimetypes
import globalVars


def send_mail(subject, filesToAttach, Text, mailTo = ''):
    # SMTP_HOST = '127.0.0.1'
    SMTP_HOST = 'smtp.gmail.com: 587'
    SMTP_FROM = 'sergutpalrpi@gmail.com'
    SMTP_PWD = 'VGs08022007'
    if not mailTo:
        mailTo = globalVars.getConfigField('mail')
    SMTP_TO = mailTo

    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['From'] = SMTP_FROM
    outer['To'] = SMTP_TO

    msg = MIMEText(Text)
    outer.attach(msg)

    if filesToAttach is not None:
        for filename in filesToAttach:
            if (globalVars.fileIsAvailable):
                continue
            ctype, encoding = mimetypes.guess_type(filename)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                if maintype == 'text':
                    fp = open(filename)
                    # Note: we should handle calculating the charset
                    msg = MIMEText(fp.read(), _subtype=subtype)
                    fp.close()
                elif maintype == 'image':
                    fp = open(filename, 'rb')
                    msg = MIMEImage(fp.read(), _subtype=subtype)
                    fp.close()
                elif maintype == 'audio':
                    fp = open(filename, 'rb')
                    msg = MIMEAudio(fp.read(), _subtype=subtype)
                    fp.close()
                else:
                    fp = open(filename, 'rb')
                    msg = MIMEBase(maintype, subtype)
                    msg.set_payload(fp.read())
                    fp.close()
                    encoders.encode_base64(msg)
                # Set the filename parameter
                msg.add_header('Content-Disposition',
                               'attachment', filename=filename)
                outer.attach(msg)

    #smtp = smtplib.SMTP(SMTP_HOST)
    smtp = smtplib.SMTP(SMTP_HOST)
    smtp.starttls()
    smtp.login(SMTP_FROM, SMTP_PWD)
    globalVars.toLogFile(outer.as_string())
    smtp.sendmail(SMTP_FROM, SMTP_TO.split(','), outer.as_string())
    smtp.quit()
