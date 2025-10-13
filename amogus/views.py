from amogus import app
from flask import jsonify
from datetime import datetime

@app.route("/healthcheck")
def healthcheck():
    time = datetime.now()
    response = {
        "time": time,
        "status": "very good! !",
        "amogus": "healthy as usual",
    }
    return jsonify(response)
