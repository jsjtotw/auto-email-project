from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import requests
import smtplib
from email.message import EmailMessage

class TandasApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.build_main_screen()
        return self.layout

    def build_main_screen(self):
        self.sender_email_input = TextInput(text="anonymous.tandas@gmail.com", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(Label(text="Enter the sender email:", size_hint=(1, 0.1)))
        self.layout.add_widget(self.sender_email_input)

        self.sender_key_input = TextInput(password=True, text="noct xpmm tdjw jrna", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(Label(text="Enter the application password:", size_hint=(1, 0.1)))
        self.layout.add_widget(self.sender_key_input)

        self.recipient_email_input = TextInput(text="joshua_tan_shao_jie@students.edu.sg", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(Label(text="Enter the recipient email:", size_hint=(1, 0.1)))
        self.layout.add_widget(self.recipient_email_input)

        self.email_subject_input = TextInput(text="Subject", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(Label(text="Enter the email subject:", size_hint=(1, 0.1)))
        self.layout.add_widget(self.email_subject_input)

        self.text_radio = True  # Default to text
        self.text_radio_button = Button(text="Text", on_press=self.select_text_radio, size_hint=(0.3, 1))
        self.url_radio_button = Button(text="URL", on_press=self.select_url_radio, size_hint=(0.3, 1))
        self.layout.add_widget(Label(text="Choose 'text' or 'url':", size_hint=(1, 0.1)))
        radio_layout = BoxLayout(size_hint=(1, 0.1))
        radio_layout.add_widget(self.text_radio_button)
        radio_layout.add_widget(self.url_radio_button)
        self.layout.add_widget(radio_layout)

        self.next_button = Button(text="Next", on_press=self.next_button_press, size_hint=(1, 0.1))
        self.layout.add_widget(self.next_button)

    def select_text_radio(self, instance):
        self.text_radio = True
        self.text_radio_button.state = 'down'
        self.url_radio_button.state = 'normal'

    def select_url_radio(self, instance):
        self.text_radio = False
        self.url_radio_button.state = 'down'
        self.text_radio_button.state = 'normal'

    def next_button_press(self, instance):
        if self.text_radio:
            self.text_window()
        else:
            self.url_window()

    def text_window(self):
        text_content_input = TextInput()
        repeat_text_input = TextInput()

        text_layout = BoxLayout(orientation='vertical')
        text_layout.add_widget(Label(text="Enter the text content:"))
        text_layout.add_widget(text_content_input)
        text_layout.add_widget(Label(text="Enter how many times you want to send the text:"))
        text_layout.add_widget(repeat_text_input)
        text_layout.add_widget(Button(text="Send", on_press=lambda x: self.text_window_send(text_content_input.text, repeat_text_input.text)))

        self.layout.clear_widgets()
        self.layout.add_widget(text_layout)
        self.layout.add_widget(BoxLayout(size_hint=(1, 1.5)))  # Black space

    def text_window_send(self, text_content, repeat_text):
        self.tandas(self.email_subject_input.text, [text_content], self.recipient_email_input.text,
                    self.sender_email_input.text, self.sender_key_input.text, "", repeat_text=int(repeat_text))

    def url_window(self):
        url_input = TextInput(text="https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt")
        limit_input = TextInput()

        url_layout = BoxLayout(orientation='vertical')
        url_layout.add_widget(Label(text="Enter the URL:"))
        url_layout.add_widget(url_input)
        url_layout.add_widget(Label(text="Enter the number of lines to limit the content:"))
        url_layout.add_widget(limit_input)
        url_layout.add_widget(Button(text="Send", on_press=lambda x: self.url_window_send(url_input.text, limit_input.text)))

        self.layout.clear_widgets()
        self.layout.add_widget(url_layout)
        self.layout.add_widget(BoxLayout(size_hint=(1, 1.5)))  # Black space

    def url_window_send(self, url_input, limit_input):
        limit = int(limit_input) if limit_input.strip() else None
        self.tandas(self.email_subject_input.text, [], self.recipient_email_input.text, self.sender_email_input.text,
                    self.sender_key_input.text, url_input, limit)

    def tandas(self, subject, paragraphs, to, email, key, url, limit=None, repeat_text=None):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, key)

        if url.startswith("http"):
            response = requests.get(url)
            content = response.text
            paragraphs = [para.strip() for para in content.split('\n\n') if para.strip()]

        for _ in range(repeat_text) if repeat_text else [0]:
            for body in paragraphs[:limit]:
                message = EmailMessage()
                message.set_content(body.strip())
                message["subject"] = subject
                message["to"] = to
                message["from"] = email
                server.send_message(message)

        server.quit()

        self.layout.clear_widgets()
        self.layout.add_widget(Label(text='Emails Sent Successfully!', halign='center'))
        self.layout.add_widget(Button(text='Exit', on_press=self.stop))

if __name__ == "__main__":
    TandasApp().run()
