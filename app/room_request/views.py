from flask import (
    Blueprint,
)

from .forms import RoomRequestForm
from . import room_request

room_request = Blueprint('room_request', __name__)

# TODO dashboard at route /

# TODO create form at route /new
@room_request.route('/new')
def new():
    """New Room Request page."""
    