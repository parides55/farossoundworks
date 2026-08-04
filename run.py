import os
from flask import Flask, render_template, request, redirect, url_for
if os.path.exists('env.py'):
    import env

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')