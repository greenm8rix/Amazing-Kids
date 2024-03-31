import os
from random import randint
import uuid
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_restful import Resource, Api
import requests
from flask import (
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
    session,
)
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectField,
    TextAreaField,
    FileField,
)
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from model import LoginModel, products, StripeCustomer
from config import db, app
from google.cloud import storage
from storage import test, test1

storage_client = "storage.Client()"
api = Api(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"
login_manager.login_message = "User needs to be logged in to view this page"

login_manager.login_message_category = "error"
import stripe

# secret_key = os.environ.get("STRIPE_SECRET_KEY")
secret_key = "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"
# publishable_key = os.environ.get("STRIPE_PUBLISHABLE_KEY")
publishable_key = "pk_live_51MFGxiSEhGK1MQdSIge0YfXx7zGLPJruOD7fVi3WS3uhcfoBiMoYfChIuyp5raBV5291ArVDBAUhjELz3MmFP5Jx00DYtKrxkW"
price_id = "price_1MFHSYSEhGK1MQdS74qKjdLP"
price_id1 = "price_1MFHSYSEhGK1MQdS74qKjdLP"
endpoint_secret = "whsec_BCZROJMuoDGWgKlF0DwXxP5q1kLkBLug"
stripe_keys = {
    "secret_key": secret_key,
    "publishable_key": publishable_key,
    "price_id": price_id,
    "endpoint_secret": endpoint_secret,
}
stripe.api_key = stripe_keys["secret_key"]


@login_manager.user_loader
def load_user(user_id):
    return LoginModel.query.get((user_id))


class accountform(FlaskForm):

    submit = SubmitField(
        "Manage Billing",
        render_kw={"type": "submit"},
    )


class RegisterForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Length(min=4, max=40)],
        render_kw={
            "placeholder": "Email",
            "type": "email",
        },
    )

    first_name = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={
            "placeholder": "first name",
        },
    )
    last_name = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={
            "placeholder": "last name",
        },
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={
            "placeholder": "Password",
        },
    )

    submit = SubmitField(
        "Register",
        render_kw={
            "class": "bordder-primary w-full cursor-pointer rounded-md border bg-primary py-3 px-5 text-base text-white transition duration-300 ease-in-out hover:shadow-md"
        },
    )

    def validate_email(self, email):
        existing_user_email = (
            db.session.query(LoginModel).filter(LoginModel.email == email.data).first()
        )
        if existing_user_email:
            raise ValidationError(
                "That email already exists. Please choose a different one."
            )


class LoginForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Length(min=4, max=40)],
        render_kw={
            "placeholder": "Email",
            "type": "email",
        },
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={
            "placeholder": "Password",
        },
    )

    submit = SubmitField(
        "Login",
        render_kw={
            "class": "bordder-primary w-full cursor-pointer rounded-md border bg-primary py-3 px-5 text-base text-white transition duration-300 ease-in-out hover:shadow-md"
        },
    )


class Amazingkids(Resource):
    @app.route("/")
    @app.route("/index")
    def index():
        form0 = RegisterForm()
        form1 = LoginForm()
        return render_template("index.html", form_register=form0, form_login=form1)

    @app.route("/create-checkout-session")
    def create_checkout_session():
        domain_url = "https://amazingkidsschool.com/"
        stripe.api_key = stripe_keys["secret_key"]
    
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "index",
                mode="subscription",
                client_reference_id=current_user.id,
                line_items=[
                    {
                        "price": stripe_keys["price_id"],
                        "quantity": 1,
                    }
                ],
            )
            user = (
                db.session.query(LoginModel)
                .filter(LoginModel.id == current_user.id)
                .first()
            )
            db.session.commit()
            return jsonify({"sessionId": checkout_session["id"]})
        except Exception as e:
            return jsonify(error=str(e)), 403

    @app.route("/webhook", methods=["POST"])
    def stripe_webhook():
        payload = request.get_data(as_text=True)
        sig_header = request.headers.get("Stripe-Signature")

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, stripe_keys["endpoint_secret"]
            )

        except ValueError as e:
            # Invalid payload
            return "Invalid payload", 400
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return "Invalid signature", 400

        # Handle the checkout.session.completed event
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]

            # Fulfill the purchase...
            Amazingkids.handle_checkout_session_positive(session)
        if event["type"] == "customer.subscription.deleted":
            session = event["data"]["object"]
            Amazingkids.handle_checkout_session_negative(session)

        return "Success", 200

    def handle_checkout_session_positive(session):
        user_data = (
            db.session.query(LoginModel)
            .filter(LoginModel.id == session["client_reference_id"])
            .first()
        )
        product_data = db.session.query(products).first()
        stripe_user = (
            db.session.query(StripeCustomer)
            .filter(
                StripeCustomer.user_id == session["client_reference_id"],
            )
            .first()
        )
        if not stripe_user:
            new_user = StripeCustomer(
                stripeCustomerId=session["customer"],
                stripeSubscriptionId=session["subscription"],
                user_id=session["client_reference_id"],
            )
            db.session.add(new_user)
        else:
            if stripe_user:
                subscription = stripe.Subscription.retrieve(
                    stripe_user.stripeSubscriptionId
                )
                if subscription.status != "active":
                    stripe_user.stripeCustomerId = (session["customer"],)
                    stripe_user.stripeSubscriptionId = session["subscription"]
                else:
                    stripe.Subscription.modify(subscription.id)
            stripe_user.stripeCustomerId = (session["customer"],)
            stripe_user.stripeSubscriptionId = session["subscription"]

        user_data.subscription_tier = True

        db.session.commit()

    def handle_checkout_session_negative(session):
        user_data = (
            db.session.query(LoginModel)
            .filter(LoginModel.id == session["client_reference_id"])
            .first()
        )
        product_data = db.session.query(products).first()
        stripe_user = (
            db.session.query(StripeCustomer)
            .filter(
                StripeCustomer.user_id == session["client_reference_id"],
            )
            .first()
        )
        if stripe_user:
            subscription = stripe.Subscription.retrieve(
                stripe_user.stripeSubscriptionId
            )
            stripe.Subscription.modify(subscription.id, cancel_at_period_end=True)
        stripe_user.stripeCustomerId = (session["customer"],)
        stripe_user.stripeSubscriptionId = session["subscription"]

        user_data.subscription_tier = product_data.Product

        db.session.commit()

    @app.route("/account", methods=["GET"])
    @login_required
    def account():
        form0 = RegisterForm()
        form1 = LoginForm()
        form = accountform()
        if current_user.is_authenticated:
            customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
            if customer:
                subscription = stripe.Subscription.retrieve(
                    customer.stripeSubscriptionId
                )
                if subscription.status == "active":
                    return render_template(
                        "account.html",
                        form_register=form0,
                        form_login=form1,
                        data="Active",
                        form=form,
                    )
        return render_template(
            "account.html", form_register=form0, form_login=form1, form=form, data=None
        )

    @app.route("/account", methods=["POST"])
    @login_required
    def manage():
        form = accountform()
        if form.validate_on_submit:
            stripe.api_key = stripe_keys["secret_key"]
            stripe.billing_portal.Configuration.create(
                business_profile={
                    "headline": "Amazing Kids partners with Stripe for simplified billing.",
                },
                features={
                    "invoice_history": {"enabled": True},
                    "subscription_cancel": {"enabled": True},
                },
            )
            stripe_user = (
                db.session.query(StripeCustomer).filter(
                    StripeCustomer.user_id == current_user.id,
                )
            ).first()

            if not stripe_user:
                return redirect("pricing")
            session = stripe.billing_portal.Session.create(
                customer=stripe_user.stripeCustomerId,
                return_url="https://amazingkidsschool.com/account",
            )

        return redirect(session.url)

    @app.route("/config")
    def get_publishable_key():
        stripe_config = {"publicKey": stripe_keys["publishable_key"]}
        return jsonify(stripe_config)

    @app.route("/success")
    def success():

        return render_template("success.html")

    @app.route("/pricing")
    def pricing():
        form0 = RegisterForm()
        form1 = LoginForm()
        if current_user.is_authenticated:
            customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
            if customer:
                subscription = stripe.Subscription.retrieve(
                    customer.stripeSubscriptionId
                )
                if subscription.status == "active":
                    return render_template(
                        "pricing.html",
                        form_register=form0,
                        form_login=form1,
                        data="Active",
                    )

        return render_template(
            "pricing.html", form_register=form0, form_login=form1, data=None
        )

    @app.route("/signup", methods=["POST"])
    def signup():
        form = RegisterForm()
        form0 = LoginForm()
        if form.validate_on_submit():

            hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            new_user = LoginModel(
                id=uuid.uuid4(),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=hashed_password,
                subscription_tier=False,
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            return render_template("index.html", form_register=form, form_login=form0)

    @app.route("/signin", methods=["GET", "POST"])
    def signin():
        if current_user.is_authenticated:
            return redirect(url_for("index"))

        form = LoginForm()
        form0 = RegisterForm()
        if form.validate_on_submit():
            user = (
                db.session.query(LoginModel)
                .filter(LoginModel.email == form.email.data)
                .first()
            )
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                if current_user.subscription_tier == True:
                    return redirect(url_for("games"))
                else:
                    return redirect(url_for("games"))
        return render_template("index.html", form_register=form0, form_login=form)

    @app.route("/logout", methods=["GET", "POST"])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.route("/contact")
    def contact():
        form0 = RegisterForm()
        form1 = LoginForm()
        return render_template("contact.html", form_register=form0, form_login=form1)

    @app.route("/worksheets")
    @login_required
    def worksheets():
        form0 = RegisterForm()
        form1 = LoginForm()
        x = test()
        y = test1()
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer:
            subscription = stripe.Subscription.retrieve(customer.stripeSubscriptionId)
            if subscription.status != "active":
                return redirect(url_for("pricing"))
            return render_template(
                "worksheets.html",
                data=x,
                form_register=form0,
                form_login=form1,
                datas=y,
            )
        else:
            return redirect(url_for("pricing"))

    @app.route("/games")
    @login_required
    def games():
        form0 = RegisterForm()
        form1 = LoginForm()
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer:
            subscription = stripe.Subscription.retrieve(customer.stripeSubscriptionId)
            print(subscription.status)
            if subscription.status != "active":
                return redirect(url_for("pricing"))
            return render_template("games.html", form_register=form0, form_login=form1)
        else:
            return render_template("games.html", form_register=form0, form_login=form1)

    @app.route("/math")
    @login_required
    def math():
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer:
            subscription = stripe.Subscription.retrieve(customer.stripeSubscriptionId)
            print(subscription.status)
            if subscription.status != "active":
                return redirect(url_for("pricing"))
            return render_template("math.html")
        else:
            return redirect(url_for("pricing"))

    @app.route("/puzzle")
    @login_required
    def puzzle():
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer:
            subscription = stripe.Subscription.retrieve(customer.stripeSubscriptionId)
            print(subscription.status)
            if subscription.status != "active":
                return redirect(url_for("pricing"))
            return render_template("pic.html")
        else:
            return redirect(url_for("pricing"))

    @app.route("/crossword")
    @login_required
    def crossword():
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer:
            subscription = stripe.Subscription.retrieve(customer.stripeSubscriptionId)
            print(subscription.status)
            if subscription.status != "active":
                return redirect(url_for("pricing"))
            x = randint(1, 4)
            return render_template(f"crossword{x}.html")
        else:
            return redirect(url_for("pricing"))

    @app.route("/countanimals")
    @login_required
    def countanimals():
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer:
            subscription = stripe.Subscription.retrieve(customer.stripeSubscriptionId)
            print(subscription.status)
            if subscription.status != "active":
                return redirect(url_for("pricing"))
            return render_template(f"countanimals.html")
        else:
            return redirect(url_for("pricing"))

    @app.route("/guesstheword")
    @login_required
    def guesstheword():
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer:
            subscription = stripe.Subscription.retrieve(customer.stripeSubscriptionId)
            print(subscription.status)
            if subscription.status != "active":
                return redirect(url_for("pricing"))
            x = randint(1, 4)
            return render_template(f"guesstheword{x}.html")
        else:
            return redirect(url_for("pricing"))

    @app.route("/piano")
    @login_required
    def piano():
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer:
            subscription = stripe.Subscription.retrieve(customer.stripeSubscriptionId)
            print(subscription.status)
            if subscription.status != "active":
                return redirect(url_for("pricing"))
            return render_template(f"piano.html")
        else:
            return redirect(url_for("pricing"))

    @app.route("/hangman")
    @login_required
    def hangman():
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer:
            subscription = stripe.Subscription.retrieve(customer.stripeSubscriptionId)
            print(subscription.status)
            if subscription.status != "active":
                return redirect(url_for("pricing"))
            return render_template(f"hangman.html")
        else:
            return redirect(url_for("pricing"))

    @app.route("/pacman")
    @login_required
    def pacman():
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer:
            subscription = stripe.Subscription.retrieve(customer.stripeSubscriptionId)
            print(subscription.status)
            if subscription.status != "active":
                return redirect(url_for("pricing"))
            return render_template(f"pacman.html")
        else:
            return redirect(url_for("pricing"))

    @app.route("/tos")
    def tos():
        form0 = RegisterForm()
        form1 = LoginForm()
        return render_template(f"tos.html", form_register=form0, form_login=form1)


api.add_resource(Amazingkids)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=8080, debug=True, threaded=True)
