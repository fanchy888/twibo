
from twibo_server import mail, Message


def send_email(subject, content, receiver):
    msg = Message(subject=subject, recipients=[receiver])
    msg.html = content
    mail.send(msg)
    return
