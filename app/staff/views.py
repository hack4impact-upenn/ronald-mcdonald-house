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

from app.decorators import staff_required
from app.models import EditableHTML, Role, RoomRequest
import re

staff = Blueprint('staff', __name__)


@login_required
@staff_required
@staff.route('/')
def index():
    """Staff dashboard page."""
    roles = Role.query.all()
    room_requests = RoomRequest.query.all()
    duplicates = duplicate_requests(room_requests)

    return render_template('staff/index.html', roles=roles, room_requests=room_requests, duplicates=duplicates)


@staff_required
@staff.route('/room-request-form', methods=['GET'])
def manage():
    room_requests = RoomRequest.query.all()
    return render_template('room_request/manage.html', room_requests=room_requests)


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
