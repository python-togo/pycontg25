import typing

if not hasattr(typing, "_ClassVar") and hasattr(typing, "ClassVar"):
    typing._ClassVar = typing.ClassVar

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
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


    
app = Flask(__name__)

app.static_folder = "static"
app.template_folder = "templates"

application = app
year = datetime.now().year
event_date = datetime(2025, 8, 23, 7, 0, 0)
event_date_str = event_date.strftime("%d %B %Y at %H:%M")
regigstration_date = datetime(2025, 7, 23, 0, 0, 0)
opening_in = regigstration_date - datetime.now()
opening_in_days = opening_in.days
sponsor_tiers = get_sponsorteirs()
proposal_opining_date = datetime(2025, 6, 3, 16).strftime("%d %B %Y at %H:%M UTC")
proposal_closing_date = datetime(2025, 6, 30, 16).strftime("%d %B %Y at %H:%M UTC")


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
       
        '''if regigstration_date >  datetime.now():
            return render_template(
                "registration.html",
                year=year,
                event_date=event_date_str,
                registration_open=True,
                opening_in_days=opening_in_days,
            )'''
        
        return render_template(
            "register.html",
            year=year,
            event_date=event_date_str,
            registration_open=False,
        )
    else:
        if regigstration_date >  datetime.now():
            return render_template(
                "registration.html",
                year=year,
                event_date=event_date_str,
                registration_open=True,
                opening_in_days=opening_in_days,
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
        )

        if not is_valid_email(data.email):
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=True,
                root="/register",
                status="error",
                message=[
                    "Oops! Something went wrong.",
                    "Please enter a valid email address.",
                ],
            )

        existing_entry = get_something_email("registrations", data.email)
        
        if existing_entry:
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=False,
                status="error",
                message=[
                    "Oops! Something went wrong.",
                    "You are already registed, please check your email.",
                ],
            )

        successed = insert_something("registrations", data.dict())
        if not successed:
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=True,
                root="/register",
                status="error",
                message=[
                    "Oops! Something went wrong.",
                    "There was an error submitting your registration. Please try again.",
                ],
            )

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

@app.route("/health-safety")
def health_safety():
    return render_template(
        "health-safety.html",
        year=year,
    )

@app.route("/schedule")
def schedule():
    return redirect(url_for("coming_soon"))

@app.route("/volunteer", methods=["GET", "POST"])
def volunteer():
    if request.method == "GET":
        if datetime.now() > datetime(2025, 5, 31, 16, 0, 0):
            return render_template(
                "call_to_action_close.html",
                year=year,
                call_to_action="volunteers",
            )  
        return render_template(
            "volunteer.html",
            year=year,
        )
    else:
        if datetime.now() > datetime(2025, 5, 31, 16, 0, 0):
            return render_template(
                "call_to_action_close.html",
                year=year,
                call_to_action="volunteers",
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


@app.route("/proposal", methods=["GET", "POST"])
def proposal():
    cfp_opening_in_days = datetime(2025, 6, 2, 16, 0, 0)
    cfp_closing_in_days = datetime(2025, 6, 30, 16, 0, 0)
    if request.method == "GET":
        if cfp_opening_in_days > datetime.now():
            return render_template(
                "cfp.html",
                year=year,
                event_date=event_date_str,
                registration_open=True,
                opening_in_days=cfp_opening_in_days,
            )
        elif cfp_closing_in_days < datetime.now():
            return render_template(
                "call_to_action_close.html",
                year=year,
                call_to_action="Proposals",
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
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=True,
                root="/proposal",
                status="error",
                message=[
                    "Oops! Something went wrong.",
                    "Please enter a valid email address.",
                ],
            )

        existing_entry = get_something_email("proposals", data.email)
        print(existing_entry)
        if existing_entry:
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=False,
                status="error",
                message=[
                    "Oops! Something went wrong.",
                    "We have already received a proposal from you. please feel free to reach out to us at contact@pytogo.org.",
                ],
            )

        successed = insert_something("proposals", data.dict())
        if not successed:
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=True,
                root="/proposal",
                status="error",
                message=[
                    "Oops! Something went wrong.",
                    "There was an error submitting your proposal. Please try again.",
                ],
            )

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
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=True,
                root="/sponsor",
                status="error",
                message=[
                    "Oops! Something went wrong.",
                    "Please enter a valid email address.",
                ],
            )

        successed = insert_something("sponsorinquiry", data.dict())
        if not successed:
            return render_template(
                "success.html",
                year=year,
                event_date=event_date_str,
                retry=True,
                root="/sponsor",
                status="error",
                message=[
                    "Oops! Something went wrong.",
                    "There was an error submitting. Please try again.",
                ],
            )

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

# api 



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", year=year), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", year=year), 500  


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
