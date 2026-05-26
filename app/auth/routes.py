import re

from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, current_user

from . import auth_bp
from app.extensions import db
from app.models import User, ConferenceRegistration
from app.utils.email_utils import send_registration_credentials_email


def is_valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10


def is_admin_user(user):
    admin_email = current_app.config.get("ADMIN_EMAIL")
    return user.email == admin_email


REGISTRATION_FEES = {
    "Conference + Workshop": 4000,
    "Only Conference": 3000,
    "Associate Delegate": 2000,
}


@auth_bp.route("/conference-registration", methods=["GET", "POST"])
def conference_registration():
    if current_user.is_authenticated:
        if is_admin_user(current_user):
            return redirect(url_for("admin.dashboard"))
        if current_user.conference_registration:
            return redirect(url_for("user.abstract_portal"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        institution_name = request.form.get("institution_name", "").strip()
        designation = request.form.get("designation", "").strip()
        department = request.form.get("department", "").strip()
        medical_council_registration_number = request.form.get(
            "medical_council_registration_number", ""
        ).strip()
        council_name = request.form.get("council_name", "").strip()
        registration_type = request.form.get("registration_type", "").strip()
        transaction_id = request.form.get("transaction_id", "").strip()

        if not all([
            full_name, age, gender, email, phone, institution_name,
            designation, department, registration_type, transaction_id
        ]):
            flash("All required fields must be filled.", "danger")
            return redirect(url_for("auth.conference_registration"))

        if not is_valid_email(email):
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("auth.conference_registration"))

        if not is_valid_phone(phone):
            flash("Please enter a valid 10-digit mobile number.", "danger")
            return redirect(url_for("auth.conference_registration"))

        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except ValueError:
            flash("Please enter a valid age.", "danger")
            return redirect(url_for("auth.conference_registration"))

        if registration_type not in REGISTRATION_FEES:
            flash("Please select a valid registration type.", "danger")
            return redirect(url_for("auth.conference_registration"))

        if User.query.filter_by(email=email).first():
            flash("This email is already registered. Please log in.", "warning")
            return redirect(url_for("auth.login"))

        if User.query.filter_by(phone=phone).first():
            flash("This mobile number is already registered. Please log in.", "warning")
            return redirect(url_for("auth.login"))

        if ConferenceRegistration.query.filter_by(transaction_id=transaction_id).first():
            flash("This transaction ID/UPI ID is already used.", "warning")
            return redirect(url_for("auth.conference_registration"))

        registration_fee = REGISTRATION_FEES[registration_type]

        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
        )
        user.set_password(phone)

        db.session.add(user)
        db.session.flush()

        conference_registration = ConferenceRegistration(
            full_name=full_name,
            age=age,
            gender=gender,
            email=email,
            phone=phone,
            institution_name=institution_name,
            designation=designation,
            department=department,
            medical_council_registration_number=medical_council_registration_number,
            council_name=council_name,
            registration_type=registration_type,
            registration_fee=registration_fee,
            transaction_id=transaction_id,
            payment_verified=False,
            user_id=user.id
        )

        db.session.add(conference_registration)
        db.session.commit()

        email_sent = send_registration_credentials_email(
            recipient_email=email,
            participant_name=full_name,
            username=email,
            password=phone
        )

        if email_sent:
            flash(
                "Conference registration submitted successfully. Login credentials have been sent to your email.",
                "success"
            )
        else:
            flash(
                "Conference registration submitted successfully, but the email could not be sent. "
                "Your username is your email and password is your phone number.",
                "warning"
            )

        return redirect(url_for("auth.login"))

    return render_template(
        "auth/conference_registration.html",
        registration_fees=REGISTRATION_FEES
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if is_admin_user(current_user):
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("user.abstract_portal"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not identifier or not password:
            flash("Please enter email and password.", "danger")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(email=identifier).first()

        if not user:
            flash("No registration found with this email. Please register for the conference first.", "warning")
            return redirect(url_for("auth.conference_registration"))

        if not user.check_password(password):
            flash("Invalid login credentials.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)
        flash("Login successful.", "success")

        if is_admin_user(user):
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("user.abstract_portal"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))