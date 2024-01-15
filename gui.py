import requests
import smtplib
from email.message import EmailMessage
from tqdm import tqdm
import PySimpleGUI as sg

def tandas(subject, paragraphs, to, email, key, url, limit=None, repeat_text=None):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, key)

    if url.startswith("http"):
        response = requests.get(url)
        content = response.text
        paragraphs = [para.strip() for para in content.split('\n\n') if para.strip()]

    with tqdm(total=len(paragraphs) * repeat_text if repeat_text else len(paragraphs), desc="Sending Emails", unit="email") as pbar:
        for _ in range(repeat_text) if repeat_text else [0]:
            for body in paragraphs[:limit]:
                message = EmailMessage()
                message.set_content(body.strip())
                message["subject"] = subject
                message["to"] = to
                message["from"] = email
                server.send_message(message)
                pbar.update(1)

    server.quit()

    sg.popup('Emails Sent Successfully!', title='Success')

def main_window():
    layout = [
        [sg.Text("Enter the sender email:"), sg.InputText(key='sender_email', default_text="anonymous.tandas@gmail.com")],
        [sg.Text("Enter the application password:"), sg.InputText(key='sender_key', password_char='*', default_text="noct xpmm tdjw jrna")],
        [sg.Text("Enter the recipient email:"), sg.InputText(key='recipient_email', default_text="joshua_tan_shao_jie@students.edu.sg")],
        [sg.Text("Enter the email subject:"), sg.InputText(key='email_subject', default_text="Subject")],
        [sg.Text("Choose 'text' or 'url':"), sg.Radio('Text', 'RADIO1', key='text_radio', default=True), sg.Radio('URL', 'RADIO1', key='url_radio')],
        [sg.Button('Send', key='send_button')],
    ]

    window = sg.Window('Tandas Email Sender', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'send_button':
            if values['text_radio']:
                text_content, repeat_text = text_window(values, window)
                tandas(values['email_subject'], [text_content], values['recipient_email'],
                       values['sender_email'], values['sender_key'], "", repeat_text=repeat_text)
                print("Emails Sent Successfully!")
            elif values['url_radio']:
                url_input, limit = url_window(values, window)
                tandas(values['email_subject'], [], values['recipient_email'], values['sender_email'],
                       values['sender_key'], url_input, limit)
                print("Emails Sent Successfully!")

    window.close()

def text_window(values, window):
    layout = [
        [sg.Text("Enter the text content:"), sg.InputText(key='text_content')],
        [sg.Text("Enter how many times you want to send the text:"), sg.InputText(key='repeat_text')],
        [sg.Button('Send')],
    ]

    window.Hide()

    text_window = sg.Window('Text Content', layout)

    while True:
        event, values_text = text_window.read()

        if event == sg.WINDOW_CLOSED:
            text_window.close()
            window.UnHide()
            return None, None 

        if event == 'Send' and values_text['text_content']:
            text_window.close()
            window.UnHide()
            return values_text['text_content'], int(values_text['repeat_text'])

    text_window.close()

def url_window(values, window):
    layout = [
        [sg.Text("Enter the URL:"), sg.InputText(key='url_input', default_text="https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt")],
        [sg.Text("Enter the number of lines to limit the content:"), sg.InputText(key='limit_input')],
        [sg.Button('Send')],
    ]

    window.Hide()

    url_window = sg.Window('URL Content', layout)

    while True:
        event, values_url = url_window.read()

        if event == sg.WINDOW_CLOSED:
            url_window.close()
            window.UnHide()
            break

        if event == 'Send':
            url_window.close()
            window.UnHide()
            try:
                limit = int(values_url['limit_input']) if values_url['limit_input'].strip() else None
            except ValueError:
                print("Invalid input. Using the entire content.")
                limit = None

            return values_url['url_input'], limit

    url_window.close()

if __name__ == "__main__":
    main_window()
