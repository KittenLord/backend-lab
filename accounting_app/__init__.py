from flask import Flask

app = Flask(__name__)

import accounting_app.views
