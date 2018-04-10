"""Module for Logged Activities in Andela."""
from flask import g, jsonify
from flask_restplus import Resource

from api.models import LoggedActivity
from api.utils.auth import token_required


class UserLoggedActivitiesAPI(Resource):
    """Logged Activities Resources."""
    decorators = [token_required]

    def delete(self, logged_activity_id):
        """Delete a logged activity."""
        message = 'Logged activity has been deleted successfully.'

        logged_activity = LoggedActivity.query.filter_by(
            uuid=logged_activity_id,
            user_id=g.current_user.uuid).first()

        if not logged_activity:
            response = jsonify(message='Logged Activity does not exist!')
            response.status_code = 404
        else:
            logged_activity.delete()

            response = jsonify(
                message=message
            )
            response.status_code = 200

        return response
