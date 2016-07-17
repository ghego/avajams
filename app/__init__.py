from flask import Flask
from helpers.formatter import CustomJSONEncoder


app = Flask(__name__)
app.config.from_object('config')
app.json_encoder = CustomJSONEncoder

# Routes / Controllers
from app.controllers import application_controller