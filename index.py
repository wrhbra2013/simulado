from flask import Flask, render_template;

app = Flask(__name__)

@app.route("/")
def boas_vindas():
    return render_template('index.html')

if __name__=="main":
    app.run()