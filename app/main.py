from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'password'

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)