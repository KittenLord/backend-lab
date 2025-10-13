from amogus import app

@app.route("/")
def healthcheck():
    return "<html><head></head><body><h1>Amogus</h1></body><html>"
