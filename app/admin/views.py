from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_rq import get_queue

from app import db
from app.admin.forms import (
    ChangeAccountTypeForm,
    ChangeUserEmailForm,
    InviteUserForm,
    NewUserForm,
)
from app.decorators import admin_required
from app.email import send_email
from app.models import EditableHTML, Role, User, RoomRequest
from sqlalchemy import func
import re

admin = Blueprint('admin', __name__)


@admin.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard page."""
    users = User.query.all()
    roles = Role.query.all()
    room_requests = RoomRequest.query.all()
    duplicates = duplicate_requests(room_requests)

    return render_template('admin/index.html', users=users, roles=roles, room_requests=room_requests, duplicates=duplicates)


@admin.route('/new-user', methods=['GET', 'POST'])
@login_required
@admin_required
def new_user():
    """Create a new user."""
    form = NewUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} successfully created'.format(user.full_name()),
              'form-success')
    return render_template('admin/new_user.html', form=form)


@admin.route('/invite-user', methods=['GET', 'POST'])
@login_required
@admin_required
def invite_user():
    """Invites a new user to create an account and set their own password."""
    form = InviteUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user.id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=user,
            invite_link=invite_link,
        )
        flash('User {} successfully invited'.format(user.full_name()),
              'form-success')
    return render_template('admin/new_user.html', form=form)


@admin.route('/room-request-form', methods=['GET'])
def manage():
    room_requests = RoomRequest.query.all()
    return render_template('room_request/manage.html', room_requests=room_requests)

@admin.route('/users')
@login_required
@admin_required
def registered_users():
    """View all registered users."""
    users = User.query.all()
    roles = Role.query.all()
    return render_template(
        'admin/registered_users.html', users=users, roles=roles)


@admin.route('/user/<int:user_id>')
@admin.route('/user/<int:user_id>/info')
@login_required
@admin_required
def user_info(user_id):
    """View a user's profile."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/change-email', methods=['GET', 'POST'])
@login_required
@admin_required
def change_user_email(user_id):
    """Change a user's email."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = ChangeUserEmailForm()
    if form.validate_on_submit():
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Email for user {} successfully changed to {}.'.format(
            user.full_name(), user.email), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route(
    '/user/<int:user_id>/change-account-type', methods=['GET', 'POST'])
@login_required
@admin_required
def change_account_type(user_id):
    """Change a user's account type."""
    if current_user.id == user_id:
        flash('You cannot change the type of your own account. Please ask '
              'another administrator to do this.', 'error')
        return redirect(url_for('admin.user_info', user_id=user_id))

    user = User.query.get(user_id)
    if user is None:
        abort(404)
    form = ChangeAccountTypeForm()
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('Role for user {} successfully changed to {}.'.format(
            user.full_name(), user.role.name), 'form-success')
    return render_template('admin/manage_user.html', user=user, form=form)


@admin.route('/user/<int:user_id>/delete', methods=['GET', 'DELETE'])
@login_required
@admin_required
def delete_user_request(user_id):
    """Request deletion of a user's account."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/manage_user.html', user=user)


@admin.route('/user/<int:user_id>/_delete', methods=['GET', 'DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user's account."""
    if current_user.id == user_id:
        flash('You cannot delete your own account. Please ask another '
              'administrator to do this.', 'error')
    else:
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted user %s.' % user.full_name(), 'success')
    return redirect(url_for('admin.index'))


@admin.route('/_update_editor_contents', methods=['POST'])
@login_required
@admin_required
def update_editor_contents():
    """Update the contents of an editor."""

    edit_data = request.form.get('edit_data')
    editor_name = request.form.get('editor_name')

    editor_contents = EditableHTML.query.filter_by(
        editor_name=editor_name).first()
    if editor_contents is None:
        editor_contents = EditableHTML(editor_name=editor_name)
    editor_contents.value = edit_data

    db.session.add(editor_contents)
    db.session.commit()

    return 'OK', 200


@admin.route('/edit_email_confirmation')
@login_required
@admin_required
def update_email_confirmation():
    editable_html_obj = EditableHTML.get_editable_html('email_confirmation')
    return render_template(
        'room_request/edit_text.html', editable_html_obj=editable_html_obj, title="Confirmation Email")


@admin.route('/edit_home')
@login_required
@admin_required
def update_home():
    editable_html_obj = EditableHTML.get_editable_html('home_page_language')
    return render_template(
        'room_request/edit_text.html', editable_html_obj=editable_html_obj, title="Home Page Language")


@admin.route('/edit_form_instructions')
@login_required
@admin_required
def update_form_instructions():
    """Update the email confirmation upon room request submission."""
    editable_html_obj = EditableHTML.get_editable_html("form_instructions")
    return render_template(
        'room_request/edit_text.html', editable_html_obj=editable_html_obj, title="Form Instructions")


def duplicate_requests(room_requests):
    """Find duplicate room requests."""

    def extract_primary_phone(room_request):
        """Extract and normalize the primary phone field, possibly caching the value."""

        clean_phone = '+1{},\n'.format(re.sub(r'[^0-9]', '', room_request.primary_phone))
        return room_request.primary_phone

    def extract_email(room_request):
        """Extract and normalize the email field, possibly caching the value."""

        return room_request.email.lower()

    def build_graph(room_requests, extractors):
        """Build a graph from the room requests and extractors."""

        # Create one relation per extractor.
        relations = [{} for _ in range(len(extractors))]

        # For each request, apply all extractors.
        for room_request in room_requests:
            for i, extractor in enumerate(extractors):
                extracted_value = extractor(room_request)
                relations[i].setdefault(extracted_value, []).append(room_request)

        # Return the list of built relations.
        return relations

    def children(extractors, relations, room_request):
        """Get all children associated with a given room requests."""

        for i, extractor in enumerate(extractors):
            extracted_value = extractor(room_request)
            yield from relations[i].get(extracted_value, [])

    def dfs(extractors, relations, seen, room_request):
        """
        Perform DFS starting at a given room requests and returns a list of newly seen nodes. Note that the seen set
        will be mutated.
        """

        # Room already seen.
        if room_request in seen:
            return []

        # The connected component.
        component = []

        # Initialize bookkeeping data structures.
        queue = [room_request]
        seen.add(room_request)

        # Continue until the queue is empty.
        while queue:
            # Add node to the component.
            node = queue.pop()
            component.append(node)

            # Add all children of the node.
            for child in children(extractors, relations, node):
                if child not in seen:
                    queue.append(child)
                    seen.add(child)

        # Return the connected component.
        return component

    # Initialize auxiliary data structures.
    extractors = [extract_primary_phone, extract_email]
    relations = build_graph(room_requests, extractors)

    # Keep track of seen nodes.
    seen = set()

    # Keep track of duplicate groups.
    groups = []

    # Run DFS on each room request, adding duplicate groups as necessary.
    for room_request in room_requests:
        group = dfs(extractors, relations, seen, room_request)

        # Add group.
        if len(group) > 1:
            groups.append(group)

    return groups
