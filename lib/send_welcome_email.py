

import os
import resend
from dotenv import load_dotenv

load_dotenv()
resend.api_key = os.environ["RESEND_API_KEY"]


def send_welcome_email(email, first_name):
    params = {
    "from": "dentestai@classez.net",
    "to": [email],
    "subject": "Welcome to Dentist AI",
    "html": """
        <table style="border-collapse: collapse; width: 100%; height: 17px; background: #463aa2;" border="1">
    <tbody>
        <tr style="height: 92px;">
        <td style="width: 100%; height: 17px; text-align: center; padding: 0;">
            <img src="https://share1.cloudhq-mkt3.net/3abf266ed6a5c7.png" alt="" width="64" height="64">
        </td>
        </tr>
    </tbody>
    </table>
    <br>Dear {{first_name}},
    <br>
    <br>Welcome to our project! We're thrilled to have you join us. You've just taken the first step towards a journey filled with innovation and collaboration. Your account has been successfully set up, and you're now part of a community that values progress and creativity.
    <br>
    <br>To get started, we encourage you to visit our welcome page where you'll find all the resources you need to hit the ground running. Should you have any questions or need assistance, our support team is always here to help.
    <br>
    <br>Thank you for choosing us. Let's create something amazing together!
    <br>
    <br>Best regards,
    <br>The Dentist AI Team
    <br>
    """.replace("{{first_name}}", first_name),
    }

    email = resend.Emails.send(params)
    return email
