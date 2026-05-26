from unicodedata import category

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from . import user_bp
from app.extensions import db
from app.models import AbstractSubmission


@user_bp.route("/abstract-portal")
@login_required
def abstract_portal():
    abstracts = AbstractSubmission.query.filter_by(
        user_id=current_user.id
    ).order_by(AbstractSubmission.created_at.desc()).all()

    registration = current_user.conference_registration

    return render_template(
        "user/abstract_portal.html",
        user=current_user,
        registration=registration,
        abstracts=abstracts
    )


@user_bp.route("/submit-abstract", methods=["GET", "POST"])
@login_required
def submit_abstract():
    registration = current_user.conference_registration

    if not registration:
        flash("Please register for the conference first.", "warning")
        return redirect(url_for("auth.conference_registration"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        allowed_categories = [
            "Under Graduate (UG)",
            "Post Graduate (PG)",
            "Post PG",
            "Other"
            ]

        if category not in allowed_categories:
            flash("Please select a valid abstract category.", "danger")
            return redirect(url_for("user.submit_abstract"))
        authors = request.form.get("authors", "").strip()
        presenting_author = request.form.get("presenting_author", "").strip()
        abstract_text = request.form.get("abstract_text", "").strip()
        keywords = request.form.get("keywords", "").strip()
        presentation_preference = request.form.get("presentation_preference", "").strip()

        if not title or not category or not authors or not presenting_author or not abstract_text:
            flash("Please fill all required abstract fields.", "danger")
            return redirect(url_for("user.submit_abstract"))

        existing = AbstractSubmission.query.filter_by(
            user_id=current_user.id,
            title=title
        ).first()

        if existing:
            flash("You have already submitted an abstract with this title.", "warning")
            return redirect(url_for("user.abstract_portal"))

        abstract = AbstractSubmission(
            title=title,
            category=category,
            authors=authors,
            presenting_author=presenting_author,
            abstract_text=abstract_text,
            keywords=keywords,
            presentation_preference=presentation_preference if presentation_preference else "Oral/Poster",
            user_id=current_user.id
        )

        db.session.add(abstract)
        db.session.commit()

        flash("Abstract submitted successfully.", "success")
        return redirect(url_for("user.abstract_portal"))

    return render_template("user/submit_abstract.html", registration=registration)