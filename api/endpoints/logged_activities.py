"""Module for Logged Activities in Andela."""
from flask import jsonify
from flask_restplus import Resource

from api.models import LoggedActivity, User
from api.utils.auth import token_required
from api.utils.marshmallow_schemas import get_logged_activities_schema


class UserLoggedActivitiesAPI(Resource):
    """Logged Activities Resources."""
    decorators = [token_required]

    def get(self, user_id):
        """Get a user's logged activities by user URL parameter"""
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        message = "Logged activities fetched successfully"
        user_logged_activities = LoggedActivity.query.filter_by(
            user_id=user_id).all()

        if not user_logged_activities:
            message = "There are no logged activities for that user."

        return jsonify(
            data = get_logged_activities_schema.dump(
                user_logged_activities).data,
            message=message
        )
