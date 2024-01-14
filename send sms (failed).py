import smtplib
from email.message import EmailMessage

def tandas(subject, body, to, sms_gateway_domain):
    try:
        message = EmailMessage()
        message.set_content(body)
        message["subject"] = subject
        message["to"] = to

        email = "anonymous.tandas@gmail.com"
        key = "noct xpmm tdjw jrna"
        message["from"] = email

        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email, key)
        sms_gateway_address = to + "@" + sms_gateway_domain
        server.sendmail(email, sms_gateway_address, message.as_string())
        print(f"SMS sent successfully via {sms_gateway_domain}")

    except Exception as e:
        print(f"Failed to send SMS via {sms_gateway_domain}: {e}")

    finally:
        server.quit()

if __name__ == "__main__":
    recipient_phone_number = "+6586965532"
    sms_gateway_domain = "singtel-sms.com"
    tandas("Tandas Terbaik", "Saya suka makan tandas", recipient_phone_number, sms_gateway_domain)
