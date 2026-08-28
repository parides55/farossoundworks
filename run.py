from flask import Flask, render_template, request, redirect, url_for, session
from flask_babel import Babel, _
from flask_mail import Mail, Message
import os
if os.path.exists('env.py'):
    import env


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

app.config['BABEL_DEFAULT_LOCALE'] = 'en'   # default language
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'es']  # add your languages


# Locale selector function
def get_locale():
    # First check session
    if 'lang' in session:
        return session['lang']
    # Fallback to browser preference
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])


# Pass it into Babel
babel = Babel(app, locale_selector=get_locale)


# Route to change language
@app.route('/set_language/<lang_code>')
def set_language(lang_code):
    if lang_code in app.config['BABEL_SUPPORTED_LOCALES']:
        session['lang'] = lang_code
    return redirect(request.referrer or url_for('index'))


# Email setup settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/work')
def work():
    return render_template('work.html')


@app.route('/facilities')
def facilities():   
    return render_template('facilities.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/founder')
def about_us():
    return render_template('about-us.html')


@app.route('/contact-us')
def contact_us():   
    return render_template('contact-us.html')

@app.route('/form_submit', methods=["POST"])
def form_submit():

    inquiry_type = request.form.get('inquiryType')
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # Quote-only fields
    project_types = request.form.getlist("orchestral") \
        + request.form.getlist("composition") \
        + request.form.getlist("arrangement") \
        + request.form.getlist("orchestration") \
        + request.form.getlist("music-direction") \
        + request.form.getlist("midi-mockups") \
        + request.form.getlist("score-preparation") \
        + request.form.getlist("music-production") \
        + request.form.getlist("mixing-final-delivery")

    number_of_players = request.form.get("number-of-players")
    preferred_date = request.form.get("preferred-date")

    # Handle file uploads
    uploaded_files = request.files.getlist("file-upload")

    is_quote = inquiry_type == "Quote request" or bool(project_types)

    try:
        # --- Email to you (admin) ---
        admin_html = f"""\
        <h2>{inquiry_type}</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
        """

        if is_quote:
            admin_html += f"""
            <p><strong>Project type(s):</strong> {", ".join(project_types) or "—"}</p>
            <p><strong>Approx. number of players:</strong> {number_of_players or "—"}</p>
            <p><strong>Preferred date:</strong> {preferred_date or "—"}</p>
            """

        admin_html += f"""
        <p><strong>Message:</strong></p>
        <p>{message}</p>
        """

        msg = Message(
            subject=inquiry_type,
            recipients=[os.getenv('EMAIL')],
            html=admin_html,
            reply_to=email,
        )

        # Attach uploaded files
        for f in uploaded_files:
            if f and f.filename:
                file_data = f.read()
                if file_data:  # skip empty
                    msg.attach(
                        filename=f.filename,
                        content_type=f.content_type or "application/octet-stream",
                        data=file_data,
                    )

        # --- Confirmation email to user ---
        user_html = f"""\
        <p>Hi {name},</p>
        <p>We have received your message and will respond shortly.</p>
        <p>Here is what you wrote to us:</p>
        <blockquote style="border-left:3px solid #ccc; padding-left:1em; color:#555;">
            {message}
        </blockquote>
        <p>— Faros Soundworks</p>
        """

        response_msg = Message(
            subject="Thank you for contacting Faros Soundworks",
            recipients=[email],
            html=user_html,
        )

        mail.send(msg)
        mail.send(response_msg)
        return redirect('/')

    except Exception as e:
        print("EMAIL ERROR:", e)
        return "Unable to send email.", 500

# ensures your Flask dev server only starts when you run the file directly, not when it's imported elsewhere.
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", 5000)), 
        debug=True # turn off debug mode in production for security reasons
    )