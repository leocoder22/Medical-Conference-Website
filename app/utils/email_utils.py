from flask import current_app
from flask_mail import Message

from app.extensions import mail


def send_registration_credentials_email(recipient_email, participant_name, username, password):
    subject = "MAHATROPACON 2026 Registration Received"

    body = f"""Dear Participant,

Greetings from the Organizing Committee of MAHATROPACON 2026.

We are pleased to inform you that your conference registration has been successfully received. Your registration will be confirmed once your payment has been verified by our team. A confirmation email will be sent to you upon successful verification.

For accessing the conference portal and submitting your abstract, kindly note the following login credentials:

* Username: {username}
* Password: {password}

You are requested to log in and proceed with abstract submission before 30 May.

For any queries or assistance, please feel free to contact the organizing team.

We look forward to your active participation in MAHATROPACON 2026.

Warm regards,
Organizing Committee
MAHATROPACON 2026
Datta Meghe Medical College, Nagpur
"""

    try:
        msg = Message(
            subject=subject,
            recipients=[recipient_email],
            body=body,
            sender=current_app.config.get("MAIL_DEFAULT_SENDER")
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False


def send_payment_verified_email(recipient_email, participant_name):
    subject = "MAHATROPACON 2026 Registration Confirmed"

    body = f"""Dear {participant_name},

Greetings from the Organizing Committee of MAHATROPACON 2026.

We are pleased to inform you that your payment has been successfully verified and your conference registration is now confirmed.

You may now log in to the conference portal and proceed with your abstract submission using your previously shared credentials:

* Username: Your registered email ID
* Password: Your registered phone number

For any queries or assistance, please feel free to contact the organizing team.

We look forward to your active participation in MAHATROPACON 2026.

Warm regards,
Organizing Committee
MAHATROPACON 2026
Datta Meghe Medical College, Nagpur
"""

    try:
        msg = Message(
            subject=subject,
            recipients=[recipient_email],
            body=body,
            sender=current_app.config.get("MAIL_DEFAULT_SENDER")
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Payment verification email error: {e}")
        return False
    
def send_abstract_accepted_email(recipient_email, participant_name, abstract_title, accepted_as, abstract_code):
    subject = "MAHATROPACON 2026 Abstract Accepted"

    body = f"""Dear {participant_name},

Greetings from the Organizing Committee of MAHATROPACON 2026.

We are pleased to inform you that your abstract has been accepted.

Abstract Title:
{abstract_title}

Accepted Category:
{accepted_as}

Abstract ID:
{abstract_code}

Kindly quote this Abstract ID for all future correspondence related to your abstract presentation.

Further instructions regarding presentation schedule and guidelines will be communicated in due course.

Warm regards,
Organizing Committee
MAHATROPACON 2026
Datta Meghe Medical College, Nagpur
"""

    try:
        msg = Message(
            subject=subject,
            recipients=[recipient_email],
            body=body,
            sender=current_app.config.get("MAIL_DEFAULT_SENDER")
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Abstract acceptance email error: {e}")
        return False


def send_abstract_rejected_email(recipient_email, participant_name, abstract_title):
    subject = "MAHATROPACON 2026 Abstract Review Update"

    body = f"""Dear {participant_name},

Greetings from the Organizing Committee of MAHATROPACON 2026.

Thank you for submitting your abstract for MAHATROPACON 2026.

After review, we regret to inform you that the following abstract has not been accepted for presentation.

Abstract Title:
{abstract_title}

We appreciate your interest and contribution to the conference.

Warm regards,
Organizing Committee
MAHATROPACON 2026
Datta Meghe Medical College, Nagpur
"""

    try:
        msg = Message(
            subject=subject,
            recipients=[recipient_email],
            body=body,
            sender=current_app.config.get("MAIL_DEFAULT_SENDER")
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Abstract rejection email error: {e}")
        return False