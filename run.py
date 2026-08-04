import os
from flask import Flask, render_template, request, redirect, url_for
if os.path.exists('env.py'):
    import env

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# ensures your Flask dev server only starts when you run the file directly, not when it's imported elsewhere.
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", 5000)), 
        debug=True # turn off debug mode in production for security reasons
    )