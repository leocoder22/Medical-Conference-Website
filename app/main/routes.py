from collections import OrderedDict

from flask import render_template
from . import main_bp
from app.models import Speaker, ScheduleItem


@main_bp.route("/")
def home():
    return render_template("main/index.html")


@main_bp.route("/about")
def about():
    return render_template("main/about.html")


@main_bp.route("/speakers")
def speakers():
    speakers = Speaker.query.order_by(Speaker.id.asc()).all()
    return render_template("main/speakers.html", speakers=speakers)


@main_bp.route("/schedule")
def schedule():
    schedule_items = ScheduleItem.query.order_by(
        ScheduleItem.day_label.asc(),
        ScheduleItem.display_order.asc(),
        ScheduleItem.id.asc()
    ).all()

    schedule_days = OrderedDict()

    for item in schedule_items:
        if item.day_label not in schedule_days:
            schedule_days[item.day_label] = {
                "day_title": item.section_title or item.day_label,
                "rows": []
            }

        schedule_days[item.day_label]["rows"].append(item)

    return render_template("main/schedule.html", schedule_days=schedule_days)


@main_bp.route("/contact")
def contact():
    return render_template("main/contact.html")