import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
import mimetypes
import globalVars


def send_mail(mailTo, subject, filesToAttach, Text):
    SMTP_USER = 'sergutpalrpi@gmail.com'
    SMTP_PWD = 'SGP24121976'
    SMTP_HOST = 'smtp.gmail.com:587'
    SMTP_FROM = 'Casa'
    # SMTP_TO = mailTo; # ['sergutpal@hotmail.com', 'sergutpal@gmail.com',
    # 'sgutierrez@aoc.cat', 'isharkova@gmail.com'];
    SMTP_TO = ['sergutpal@hotmail.com', 'sergutpal@gmail.com',
               'sgutierrez@aoc.cat', 'isharkova@gmail.com']

    COMMASPACE = ', '
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['From'] = SMTP_FROM
    # outer['To'] = SMTP_TO;  # COMMASPACE.join(SMTP_TO);
    outer['To'] = COMMASPACE.join(SMTP_TO)

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

    smtp = smtplib.SMTP(SMTP_HOST)
    smtp.starttls()
    smtp.login(SMTP_USER, SMTP_PWD)
    smtp.sendmail(SMTP_FROM, SMTP_TO, outer.as_string())
    smtp.quit()
