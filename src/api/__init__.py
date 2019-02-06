from flask import Flask
api_server = Flask(__name__)

from . import auth
from . import commands
