from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import os
if os.path.exists('env.py'):
    import env


app = Flask(__name__)

# Email setup settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

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


@app.route('/contact-us')
def contact_us():   
    return render_template('contact-us.html')

@app.route('/form_submit', methods=["POST"])
def form_submit():

    print(request.form)

    inquiry_type = request.form.get('inquiryType')
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    msg = Message(
        subject = inquiry_type, 
        body = f"Name: {name}\nEmail: {email}\n\n{message}",
        recipients = [os.getenv('EMAIL')]
    )
    
    response_msg = Message (
        subject = "Thank you for contacting Faros Soundworks",
        body = f"Hi {name}\n\nWe have received your message and we will response shortly.\n\nHere is what you wrote to us:\n{message}",
        recipients = [email],
    )
    mail.send(msg)
    mail.send(response_msg)
    return redirect ('/')


# ensures your Flask dev server only starts when you run the file directly, not when it's imported elsewhere.
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", 5000)), 
        debug=True # turn off debug mode in production for security reasons
    )