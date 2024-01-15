import requests
import smtplib
from email.message import EmailMessage
from tqdm import tqdm

def tandas(subject, paragraphs, to, email, key, url, limit=None, repeat_text=None):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, key)

    if url.startswith("http"):
        response = requests.get(url)
        content = response.text
        paragraphs = [para.strip() for para in content.split('\n\n') if para.strip()]

    with tqdm(total=len(paragraphs) * repeat_text if repeat_text else len(paragraphs), desc="Sending Emails", unit="email") as pbar:
        for _ in range(repeat_text) if repeat_text else [0]:  # Repeat for the specified times if repeat_text is provided
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
    while True:
        sender_email = input("Enter the sender email (default: anonymous.tandas@gmail.com): ") or "anonymous.tandas@gmail.com"
        sender_key = input("Enter the sender key (default: noct xpmm tdjw jrna): ") or "noct xpmm tdjw jrna"
        recipient_email = input("Enter the recipient email (default: joshua_tan_shao_jie@students.edu.sg): ") or "joshua_tan_shao_jie@students.edu.sg"
        email_subject = input("Enter the email subject: ")

        # Choose between text or URL
        choice = input("Choose 'text' or 'url': ").lower()
        
        if choice == 'text':
            text_content = input("Enter the text content: ")
            repeat_text = int(input("Enter how many times you want to send the text: "))
            tandas(email_subject, [text_content], recipient_email, sender_email, sender_key, "", repeat_text=repeat_text)
        
        elif choice == 'url':
            url_input = input("Enter the URL (default: https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt): ") or "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
            limit_input = input("Enter the number of lines to limit the content: ")
            try:
                limit = int(limit_input) if limit_input.strip() else None
            except ValueError:
                print("Invalid input. Using the entire content.")
                limit = None
            tandas(email_subject, [], recipient_email, sender_email, sender_key, url_input, limit)
        
        else:
            print("Invalid choice. Please choose 'text' or 'url'.")
            continue  # Restart the loop for another attempt
        
        try_again = input("Do you want to try again? (yes/no): ").lower()
        if try_again != 'no':
            continue  # Exit the loop if the user doesn't want to try again
