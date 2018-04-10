"""Module for Logged Activities in Andela."""
from datetime import datetime

from flask import jsonify, request, g
from flask_restplus import Resource

from api.models import LoggedActivity, User, Activity, ActivityType, db
from api.utils.auth import token_required
from api.utils.marshmallow_schemas import (
    single_logged_activity_schema, log_activity_schema
)


class LoggedActivitiesAPI(Resource):
    """Logged Activities Resources."""
    decorators = [token_required]

    def post(self):
        """Log a new activity"""
        if request.get_json():
            payload = request.get_json()
            result, errors = log_activity_schema.load(payload)

            if errors:
                return dict(validation_errors=errors), 400

            if result.get('activity_id'):
                activity = Activity.query.get(result['activity_id'])
                if not activity:
                    return dict(message='Invalid activity id'), 422

                activity_type = activity.activity_type
                if activity_type.name == 'Bootcamp Interviews' and \
                        not (result.get('no_of_interviewees')
                             and result.get('description')):
                    return dict(
                        message='Please send the number of interviewees and' \
                        ' their names in the description'
                    ), 400
                time_difference = datetime.utcnow() - activity.created_at
            else:
                activity_type = ActivityType.query.get(
                    result['activity_type_id']
                )
                if not activity_type:
                    return dict(message='Invalid activity type id'), 422
                activity = None
                time_difference = datetime.utcnow().date() - result['date']


            if time_difference.days > 30:
                return dict(
                    message = 'You\'re late. That activity' \
                    ' happened more than 30 days ago'
                ), 422

            society = g.current_user.society
            if not society:
                return dict(
                    message = 'You are not a member of any society yet'
                ), 422

            activity_value = activity_type.value if not \
                activity_type.name == 'Bootcamp Interviews' else \
                activity_type.value * result['no_of_interviewees']
            logged_activity = LoggedActivity (
                name=result.get('name'), description=result.get('description'),
                society=society, user=g.current_user, activity=activity,
                photo=result.get('photo'), value=activity_value,
                activity_type=activity_type
            )

            db.session.add(logged_activity)
            db.session.commit()

            return dict(
                data=single_logged_activity_schema.dump(logged_activity).data,
                message = 'Activity logged successfully'
            ), 201

        else:
            return dict(message='No data was sent to the server'), 400
