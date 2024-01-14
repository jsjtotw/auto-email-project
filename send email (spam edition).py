import requests
import smtplib
from email.message import EmailMessage
from tqdm import tqdm

def tandas(subject, paragraphs, to, limit=None):
    email = "anonymous.tandas@gmail.com"
    key = "noct xpmm tdjw jrna"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, key)
    with tqdm(total=len(paragraphs), desc="Sending Emails", unit="email") as pbar:
        for body in paragraphs[:limit]:
            message = EmailMessage()
            message.set_content(body.strip())
            message["subject"] = subject
            message["to"] = to
            message["from"] = email
            server.send_message(message)
            pbar.update(1)
    server.quit()

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
    response = requests.get(url)
    content = response.text
    paragraphs = [para.strip() for para in content.split('\n\n') if para.strip()]
    #recipient_email = "joshua_tan_shao_jie@students.edu.sg" 
    recipient_email = "lucas_thiam_chuan_quan@students.edu.sg" 
    email_subject = "Shakespearean Text"  
    limit_input = input("Enter the number of lines to limit the content (leave blank for no limit): ")
    try:
        limit = int(limit_input) if limit_input.strip() else None
    except ValueError:
        print("Invalid input. Using the entire content.")
        limit = None

    tandas(email_subject, paragraphs, recipient_email, limit)
