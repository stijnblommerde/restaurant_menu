from flask import Blueprint

main = Blueprint('main', __name__)

# avoid circular reference;
# import views & errors after main has been created
from . import views, errors