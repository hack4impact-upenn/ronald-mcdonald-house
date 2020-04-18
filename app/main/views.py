from flask import Blueprint, render_template

from app.models import EditableHTML

main = Blueprint('main', __name__)


@main.route('/')
def index():
    editable_html_obj = EditableHTML.get_editable_html("home_page_language")
    return render_template('main/index.html', editable_html_obj=editable_html_obj)
