from flask import Flask, render_template
from api import get_status

app = Flask(__name__)

@app.route("/")
def index():
    status = get_status()
    return render_template("index.html", status=status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
