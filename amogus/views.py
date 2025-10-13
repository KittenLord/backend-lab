from amogus import app

@app.route("/healthcheck")
def healthcheck():
    return "<html><head></head><body><h1>Amogus is very healthy</h1></body><html>"
