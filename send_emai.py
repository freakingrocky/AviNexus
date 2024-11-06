import requests

API_TEXT = "mlsn.bccf9684431c35435c5a841a419f8a67be4bdb0a706d12e3279acb0ba60a02a1"
url = "https://api.mailersend.com/v1/email"
headers = {
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Authorization": f"Bearer {API_TEXT}"
}
data = {
    "from": {
        "email": "rakshan793@gmail.com"
    },
    "to": [
        {
            "email": "rakshan793@gmail.com"
        }
    ],
    "subject": "Hello from MailerSend!",
    "text": "Greetings from the team, you got this message through MailerSend.",
    "html": "Greetings from the team, you got this message through MailerSend."
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json())
