from .view import *
from .user import *
from .api import *
from main import app, config


@app.context_processor
def consts():
    return {
        "DEBUG": config.DEBUG,
        "SALT": config.PASSWORD_SALT
    }
