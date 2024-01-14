import smtplib
from email.message import EmailMessage

def tandas(messages, to):
    email = "anonymous.tandas@gmail.com"
    key = "noct xpmm tdjw jrna"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, key)

    for subject, body in messages:
        message = EmailMessage()
        message.set_content(body)
        message["subject"] = subject
        message["to"] = to
        message["from"] = email

        server.send_message(message)

    server.quit()

if __name__ == "__main__":
    messages_to_send = [
        ("Subject 1", "Body of message 1"),
        ("Subject 2", "Body of message 2"),
    ]
    recipient_email = "joshua_tan_shao_jie@students.edu.sg"

    tandas(messages_to_send, recipient_email)
