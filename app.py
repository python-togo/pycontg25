import typing
from send_email import send_sponsor_email
from ticket import send_ticket_email
from schedule import get_schedule, get_speaker_images, get_event_info


if not hasattr(typing, "_ClassVar") and hasattr(typing, "ClassVar"):
    typing._ClassVar = typing.ClassVar

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime, timedelta, timezone
from models import (
    Proposal,
    SponsorInquiry,
    VolunteerInquiry,
    WaitlistInquiry,
    RegistrationInquiry,
)
from datas import (
    get_swags,
    get_sponsorteirs,
    get_sponsortirtbytitle,
    get_something_email,
    insert_something,
    # get_everything,
    # get_everything_where,
)
from validator import (
    is_valid_email,
)
from uuid import uuid4, UUID
import requests

load_dotenv()


app = Flask(__name__)

app.static_folder = "static"
app.template_folder = "templates"

application = app
year = datetime.now(timezone.utc).year
event_date = datetime(2025, 8, 23, 7, 0, 0)
event_date_str = event_date.strftime("%d %B %Y at %H:%M")
registration_date = datetime(2025, 7, 23, 16, 45, 0)
registration_closing_date = datetime(2025, 8, 16, 16, 30, 0)
schedule_release_date = datetime(2025, 8, 5, 16, 0, 0)
schedule_release_date = schedule_release_date.replace(tzinfo=timezone.utc)

registration_closing_date = registration_closing_date.replace(tzinfo=timezone.utc)

registration_date = registration_date.replace(tzinfo=timezone.utc)
opening_in = registration_date - datetime.now(timezone.utc)

opening_in_days = opening_in.days
sponsor_tiers = get_sponsorteirs()
proposal_opining_date = datetime(2025, 6, 3, 16).strftime("%d %B %Y at %H:%M UTC")
proposal_closing_date = datetime(2025, 6, 30, 16).strftime("%d %B %Y at %H:%M UTC")

# fake_speakers = [
#     {
#     "first_name": "Afi",
#     "last_name": "Lawson",
#     "photo_url": "static/images/speakers/speakfemale.jpg",
#     "banner_url": "static/images/speakers/speakfemale.jpg",  # grande image (optionnelle)
#     "short_bio": "Data Scientist passionate about AI in education.",
#     "bio": "Afi is a data scientist with 5 years of experience building AI models for education. She leads workshops and mentors women in STEM.",
#     "title": "Using AI to Personalize Learning in African Classrooms",
#     "social_link": "https://linkedin.com/in/afilawson",
#     "social_platform": "LinkedIn"
#     },
#     {
#     "name": "Kossi Adom",
#     "photo_url": "static/images/speakers/speaker_mal.jpg",
#     "banner_url": "static/images/speakers/speaker_mal.jpg",  # grande image (optionnelle)
#     "short_bio": "Software Engineer specializing in web development.",
#     "full_bio": "Kossi is a software engineer with over 7 years of experience in web development. He has worked on various projects across Africa and is passionate about open source.",
#     "talk_theme": "Building Scalable Web Applications with Python",
#     "social_link": "https://linkedin.com/in/afilawson",
#     "social_platform": "LinkedIn"
#     },
#     {
#     "name": "Dada Koffi",
#     "photo_url": "static/images/speakers/speaker_mal.jpg",
#     "banner_url": "static/images/speakers/speaker_mal.jpg",  # grande image (optionnelle)
#     "short_bio": "AI Engineer focused on natural language processing.",
#     "full_bio": "Dada is an AI engineer with a focus on natural language processing. He has developed several applications that help bridge language barriers in Africa.",
#     "talk_theme": "Natural Language Processing for African Languages",
#     "social_link": "https://linkedin.com/in/afilawson",
#     "social_platform": "LinkedIn"
#     },
#     {
#     "name": "Afi Lawson",
#     "photo_url": "static/images/speakers/speakfemale.jpg",
#     "banner_url": "static/images/speakers/speakfemale.jpg",  # grande image (optionnelle)
#     "short_bio": "Data Scientist passionate about AI in education.",
#     "full_bio": "Afi is a data scientist with 5 years of experience building AI models for education. She leads workshops and mentors",
#     "talk_theme": "Using AI to Personalize Learning in African Classrooms",
#     "social_link": "https://linkedin.com/in/afilawson",
#     "social_platform": "LinkedIn"
#     },
#     {
#     "name": "Kossi Adom",
#     "photo_url": "static/images/speakers/speaker2.jpg",
#     "banner_url": "static/images/speakers/speaker_mal.jpg",  # grande image (optionnelle)
#     "short_bio": "Software Engineer specializing in web development.",
#     "full_bio": "Kossi is a software engineer with over 7 years of experience in web development. He has worked on various projects across Africa and is passionate about open source.",
#     "talk_theme": "Building Scalable Web Applications with Python",
#     "social_link": "https://linkedin.com/in/afilawson",
#     "social_platform": "LinkedIn"
#     },

# ]

API_ROOT = os.getenv("API_ROOT", "https://api.pycontg.pytogo.org/api")
speakers_list = requests.get(f"{API_ROOT}/speakers")
if speakers_list.status_code == 200:
    speakers_list = speakers_list.json()
else:
    speakers_list = []


paidsponsors = requests.get(f"{API_ROOT}/sponsors")
if paidsponsors.status_code == 200:
    paidsponsors = paidsponsors.json()
else:
    paidsponsors = []


gold_sponsors = [sponsor for sponsor in paidsponsors if sponsor.get("level") == "gold"]
silver_sponsors = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "silver"
]
bronze_sponsors = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "bronze"
]
headline_sponsors = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "headline"
]
inkind_sponsors = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "inkind"
]
community_sponsors = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "community"
]
media_sponsors = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "media"
]
educational_supporters = [
    sponsor for sponsor in paidsponsors if sponsor.get("level") == "educational"
]


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.route("/")
def home():
    return render_template(
        "home.html",
        year=year,
        event_date=event_date_str,
        sponsor_tiers=sponsor_tiers,
        proposal_opining_date=proposal_opining_date,
        proposal_closing_date=proposal_closing_date,
        paidsponsors=paidsponsors,
    )


@app.route("/shop")
def shop_swag():
    return render_template(
        "shop.html",
        year=year,
        swags=get_swags(),
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":

        if registration_date > datetime.now(timezone.utc):
            return render_template(
                "registration.html",
                year=year,
                event_date=event_date_str,
                registration_open=True,
                opening_in_days=opening_in_days,
            )
        if datetime.now(timezone.utc) > registration_closing_date:
            return render_template(
                "registration_closed.html",
                year=year,
                call_to_action="registration",
                intro_message="Thank you for your interest in attending PyCon Togo 2025. Registration is now closed.",
            )

        return render_template(
            "register.html",
            year=year,
            event_date=event_date_str,
            registration_open=False,
        )
    else:
        if registration_date > datetime.now(timezone.utc):
            return render_template(
                "registration.html",
                year=year,
                event_date=event_date_str,
                registration_open=True,
                opening_in_days=opening_in_days,
            )
        if datetime.now(timezone.utc) > registration_closing_date:
            return render_template(
                "registration_closed.html",
                year=year,
                call_to_action="registration",
                intro_message="Thank you for your interest in attending PyCon Togo 2025. Registration is now closed.",
            )
        _id = str(uuid4())
        form_data = request.form
        data = RegistrationInquiry(
            id=_id,
            fullName=form_data.get("fullName"),
            email=form_data.get("email"),
            phone=form_data.get("phone"),
            organization=form_data.get("organization"),
            country=form_data.get("country"),
            tshirtsize=form_data.get("tshirtsize"),
            dietaryrestrictions=form_data.get("dietaryrestrictions"),
            newsletter=bool(form_data.get("newsletter")),
            codeofconduct=bool(form_data.get("codeofconduct")),
            username=form_data.get("username"),
            favoritefood=form_data.get("favoritefood"),
        )

        if not is_valid_email(data.email):
            abort(
                400,
                description="There was an error submitting your registration. Please try again.",
            )
            return

        existing_entry = get_something_email("registrations", data.email)
        if existing_entry:
            abort(403, description="You are already registered.")
            return
        try:
            send_ticket_email(
                data.fullName, data.email, data.id, data.organization, data.country
            )
            successed = insert_something("registrations", data.dict())
        except Exception as e:
            if e.args and "duplicate key" in str(e.args[0]).lower():
                successed = False
                abort(403, description="You are already registered.")
                return
            else:
                successed = False
                abort(422, description="Unprocessable Entity")
                return

        if not successed:
            abort(
                500,
                description="There was an error submitting your registration. Please try again.",
            )
            return

        success_message = [
            "Thank you for your registration!",
            "We have received your registration and will review it shortly.",
        ]

        return render_template(
            "success.html",
            year=year,
            event_date=event_date_str,
            retry=False,
            message=success_message,
            status="success",
        )


@app.route("/coming-soon")
def coming_soon():
    return render_template(
        "coming-soon.html",
        year=year,
    )


@app.route("/schedule", methods=["GET"])
def schedule():
    if datetime.now(timezone.utc) < schedule_release_date:
         return redirect(url_for("coming_soon"))
    schedule_data = get_schedule()
    speaker_images = get_speaker_images()
    event_info = get_event_info()
    return render_template(
        "schedule.html", 
        schedule=schedule_data, 
        speaker_images=speaker_images,
        event_info=event_info
    )


@app.route("/health-safety")
def health_safety():
    return render_template(
        "health-safety.html",
        year=year,
    )


# @app.route("/schedule")
# def schedule():
#     return redirect(url_for("coming_soon"))


@app.route("/volunteer", methods=["GET", "POST"])
def volunteer():
    close_volunteer_date = datetime(2025, 5, 31, 16, 0, 0)
    close_volunteer_date = close_volunteer_date.replace(tzinfo=timezone.utc)
    if request.method == "GET":
        if datetime.now(timezone.utc) > close_volunteer_date:
            return render_template(
                "call_to_action_close.html",
                year=year,
                call_to_action="volunteers",
                intro_message="Thank you for your interest in volunteering for PyCon Togo 2025. We appreciate your enthusiasm and\
                      support!",
            )
        return render_template(
            "volunteer.html",
            year=year,
        )
    else:
        if datetime.now(timezone.utc) > close_volunteer_date:
            return render_template(
                "call_to_action_close.html",
                year=year,
                call_to_action="volunteers",
                intro_message="Thank you for your interest in volunteering for PyCon Togo 2025. We appreciate your enthusiasm and\
                      support!",
            )

        form_data = request.form
        data = VolunteerInquiry(
            first_name=form_data.get("first_name"),
            last_name=form_data.get("last_name"),
            email=form_data.get("email"),
            phone=form_data.get("phone"),
            country_city=form_data.get("country_city"),
            motivation=form_data.get("motivation"),
            availability_before=bool(form_data.get("availability_before")),
            availability_during=bool(form_data.get("availability_during")),
            availability_after=bool(form_data.get("availability_after")),
            experience=form_data.get("experience"),
            registration=bool(form_data.get("registration")),
            technical=bool(form_data.get("technical")),
            logistic=bool(form_data.get("logistic")),
            social=bool(form_data.get("social")),
            other=form_data.get("other"),
            video_editor=bool(form_data.get("video_editor")),
            graphic_designer=bool(form_data.get("graphic_designer")),
            photography=bool(form_data.get("photography")),
        )

        if not is_valid_email(data.email):
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=True,
                root="/volunteer",
                status="error",
                message=[
                    "Oops! Something went wrong.",
                    "Please enter a valid email address.",
                ],
            )

        existing_entry = get_something_email("volunteerinquiry", data.email)
        if existing_entry:
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=False,
                status="error",
                message=[
                    "You are already registered.",
                    "We are currently in the process of reviewing applications and will be in touch with selected candidates soon.",
                ],
            )

        successed = insert_something("volunteerinquiry", data.dict())
        if not successed:
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=True,
                root="/volunteer",
                status="error",
                message=[
                    "Oops! Something went wrong.",
                    "There was an error submitting your registration. Please try again.",
                ],
            )

        success_message = [
            "Thank you, We appreciate your interest in volunteering!",
            "We have received your registration and will review it shortly.",
        ]
        return render_template(
            "success.html",
            year=year,
            event_date=event_date_str,
            retry=False,
            message=success_message,
            status="success",
        )


@app.route("/waitlist", methods=["GET", "POST"])
def waitlist():
    if request.method == "GET":
        if opening_in > timedelta(days=45):
            return render_template(
                "waitlist.html",
                year=year,
            )
        return redirect(url_for("register"))
    else:
        form_data = request.form
        data = WaitlistInquiry(
            email=form_data.get("email"),
        )

        if not is_valid_email(data.email):
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=True,
                root="/waitlist",
                status="error",
                message=[
                    "Oops! Something went wrong.",
                    "Please enter a valid email address.",
                ],
            )

        existing_entry = get_something_email("waitlist", data.email)
        if existing_entry:
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=False,
                status="error",
                message=[
                    "Oops! Something went wrong.",
                    "You are already on the waitlist.",
                ],
            )

        successed = insert_something("waitlist", data.dict())
        if not successed:
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=True,
                root="/waitlist",
                status="error",
                message=[
                    "Oops! Something went wrong.",
                    "There was an error submitting your registration. Please try again.",
                ],
            )

        success_message = [
            "Thank you for your interest in our event!",
            "We have received your request and will notify you if a spot becomes available.",
        ]
        return render_template(
            "success.html",
            year=year,
            event_date=event_date_str,
            retry=False,
            message=success_message,
            status="success",
        )


@app.route("/speakers", methods=["GET"])
def speakers():
    speaker_release_date = datetime(2025, 7, 10, 16, 0, 0)
    release_speaker_theme_date = datetime(2025, 7, 20, 16, 0, 0)
    speaker_release_date = speaker_release_date.replace(tzinfo=timezone.utc)
    release_speaker_theme_date = release_speaker_theme_date.replace(tzinfo=timezone.utc)
    release_speaker_theme = False

    if speaker_release_date > datetime.now(timezone.utc):

        return render_template(
            "coming-soon.html",
            year=year,
            message="Speakers will be announced soon!",
            event_date=event_date_str,
        )

    if datetime.now(timezone.utc) > release_speaker_theme_date:
        release_speaker_theme = True
        print(release_speaker_theme)
    return render_template(
        "speakers.html",
        year=year,
        event_date=event_date_str,
        speakers=speakers_list,
        is_themes_released=release_speaker_theme,
    )


@app.route("/proposal", methods=["GET", "POST"])
def proposal():
    cfp_opening_in_days = datetime(2025, 6, 2, 16, 0, 0)
    cfp_closing_in_days = datetime(2025, 7, 1, 16, 0, 0)
    cfp_opening_in_days = cfp_opening_in_days.replace(tzinfo=timezone.utc)
    cfp_closing_in_days = cfp_closing_in_days.replace(tzinfo=timezone.utc)
    if request.method == "GET":
        if cfp_opening_in_days > datetime.now(timezone.utc):
            return render_template(
                "cfp.html",
                year=year,
                event_date=event_date_str,
                registration_open=True,
                opening_in_days=cfp_opening_in_days,
            )
        elif cfp_closing_in_days < datetime.now(timezone.utc):
            return render_template(
                "call_to_action_close.html",
                year=year,
                call_to_action="Proposals",
                intro_message="Thank you for your interest in speaking at PyCon Togo 2025. The Call for Proposals is now closed.",
            )

        return render_template(
            "speaker.html",
            year=year,
        )
    else:

        form_data = request.form
        data = Proposal(
            format=form_data.get("format"),
            first_name=form_data.get("first_name"),
            last_name=form_data.get("last_name"),
            email=form_data.get("email"),
            phone=form_data.get("phone"),
            title=form_data.get("title"),
            level=form_data.get("level"),
            talk_abstract=form_data.get("talk_abstract"),
            talk_outline=form_data.get("talk_outline"),
            bio=form_data.get("bio"),
            needs=bool(form_data.get("needs")),
            talk_language=form_data.get("talk_language"),
            track=form_data.getlist("track"),
            technical_needs=form_data.get("technical_needs"),
        )

        if not is_valid_email(data.email):
            abort(400, description="Please enter a valid email address.")
            return

        existing_entry = get_something_email("proposals", data.email)
        print(existing_entry)
        if existing_entry:
            abort(403, description="You are already registered.")
            return

        successed = insert_something("proposals", data.dict())
        if not successed:
            abort(
                500,
                description="There was an error submitting your proposal. Please try again.",
            )
            return

        success_message = [
            "Thank you for your proposal!",
            "We have received your proposal and will review it shortly.",
        ]
        return render_template(
            "success.html",
            year=year,
            event_date=event_date_str,
            retry=False,
            message=success_message,
            status="success",
        )


@app.route("/sponsor", methods=["GET", "POST"])
def sponsor():
    if request.method == "GET":
        headline = get_sponsortirtbytitle("headline")
        inkind = get_sponsortirtbytitle("inkind")

        return render_template(
            "sponsor.html",
            year=year,
            event_date=event_date_str,
            headline=headline,
            inkind=inkind,
            sponsor_tiers=sponsor_tiers,
        )
    else:
        form_data = request.form
        data = SponsorInquiry(
            company=form_data.get("company"),
            email=form_data.get("email"),
            website=form_data.get("website"),
            contact=form_data.get("contact"),
            title=form_data.get("title"),
            phone=form_data.get("phone"),
            level=form_data.get("level"),
            message=form_data.get("message"),
        )

        if not is_valid_email(data.email):
            abort(400)
            return

        try:
            send_sponsor_email(
                first_name=data.company,
                email_to=data.email,
            )
            successed = insert_something("sponsorinquiry", data.dict())
        except Exception as e:
            successed = False
            abort(422, description="Unprocessable Entity")
            return

        if not successed:
            abort(500, description="Internal Server Error")
            return

        return render_template(
            "success.html",
            year=year,
            event_date=event_date_str,
            retry=False,
            message=[
                "Thank you, We appreciate your interest in sponsoring our event!",
                "We have received your inquiry and will contact you shortly.",
            ],
            status="success",
        )


@app.route("/sponsors")
def sponsors():
    return render_template(
        "sponsors.html",
        year=year,
        gold_sponsors=gold_sponsors,
        silver_sponsors=silver_sponsors,
        bronze_sponsors=bronze_sponsors,
        headline_sponsors=headline_sponsors,
        inkind_sponsors=inkind_sponsors,
        community_sponsors=community_sponsors,
        media_sponsors=media_sponsors,
        educational_supporters=educational_supporters,
    )


@app.route("/contact")
def contact():
    return render_template(
        "contact.html",
        year=year,
        sponsor_tiers=sponsor_tiers,
    )


@app.route("/about")
def about_us():
    return render_template(
        "about.html",
        year=year,
        sponsor_tiers=sponsor_tiers,
    )


@app.route("/code-of-conduct")
def code_of_conduct():
    return render_template(
        "coc.html",
        year=year,
        sponsor_tiers=sponsor_tiers,
    )


@app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html",
            year=year,
            message="Oops! The page you're looking for seems to have disappeared or doesn't exist. Perhaps it has gone off to discover the wild python in Africa!",
        ),
        404,
    )


@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html", year=year, message=e.description), 403


@app.errorhandler(400)
def bad_request(e):
    return (
        render_template(
            "400.html",
            year=year,
            message="Bad Request: The server could not understand the request due to invalid syntax.",
        ),
        400,
    )


@app.errorhandler(422)
def unprocessable_entity(e):
    return (
        render_template(
            "422.html",
            year=year,
            message="Unprocessable Entity: The server understands the content type of the request entity, but was unable to process the contained instructions.",
        ),
        422,
    )


@app.errorhandler(500)
def internal_server_error(e):
    return (
        render_template(
            "500.html", year=year, message="Oops! Something went wrong on our end."
        ),
        500,
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8800)
