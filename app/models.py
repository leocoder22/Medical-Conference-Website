from datetime import datetime

from .extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    conference_registration = db.relationship(
        "ConferenceRegistration",
        backref="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    abstracts = db.relationship(
        "AbstractSubmission",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ConferenceRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    institution_name = db.Column(db.String(200), nullable=False)
    designation = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(150), nullable=False)
    medical_council_registration_number = db.Column(db.String(150), nullable=True)
    council_name = db.Column(db.String(150), nullable=True)

    registration_type = db.Column(db.String(100), nullable=False)
    registration_fee = db.Column(db.Integer, nullable=False)

    transaction_id = db.Column(db.String(150), nullable=False, unique=True)

    payment_verified = db.Column(db.Boolean, default=False, nullable=False)
    payment_verified_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)


class AbstractSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    authors = db.Column(db.Text, nullable=False)
    presenting_author = db.Column(db.String(150), nullable=False)
    abstract_text = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String(250), nullable=True)
    presentation_preference = db.Column(db.String(50), nullable=False, default="Oral/Poster")

    status = db.Column(db.String(30), nullable=False, default="submitted")
    accepted_as = db.Column(db.String(20), nullable=True)
    abstract_code = db.Column(db.String(20), unique=True, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Speaker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    designation = db.Column(db.String(200), nullable=True)
    institution = db.Column(db.String(200), nullable=True)
    specialization = db.Column(db.String(150), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    initials = db.Column(db.String(10), nullable=True)
    gradient_class = db.Column(db.String(100), nullable=True, default="from-blue-100 to-cyan-100")
    text_color_class = db.Column(db.String(100), nullable=True, default="text-blue-700")
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ScheduleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_label = db.Column(db.String(50), nullable=False)
    section_title = db.Column(db.String(200), nullable=True)

    from_time = db.Column(db.String(50), nullable=True)
    to_time = db.Column(db.String(50), nullable=True)
    title = db.Column(db.String(200), nullable=True)
    speaker = db.Column(db.String(200), nullable=True)
    venue = db.Column(db.String(200), nullable=True)

    display_order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)