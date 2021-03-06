"""Activities Module."""
from flask import g, request
from flask_restful import Resource

from api.services.auth import roles_required, token_required
from api.utils.helpers import response_builder

from .marshmallow_schemas import activity_schema


class ActivitiesAPI(Resource):
    """Contains CRUD endpoints for activities."""

    def __init__(self, **kwargs):
        """Inject dependency for resource."""
        self.Activity = kwargs['Activity']

    @token_required
    @roles_required(["success ops", "society president"])
    def post(self):
        """Create an activity."""
        payload = request.get_json(silent=True)

        if payload:
            result, errors = activity_schema.load(payload)

            if errors:
                status_code = activity_schema.context.get('status_code')
                activity_schema.context = {}
                validation_status_code = status_code or 400
                return response_builder(errors, validation_status_code)
            else:
                activity = self.Activity(
                            name=result['name'],
                            description=result['description'],
                            activity_type_id=result['activity_type_id'],
                            activity_date=result['activity_date'],
                            added_by_id=g.current_user.uuid
                                    )
                activity.save()

                return response_builder(dict(
                                        message='Activity created'
                                        ' successfully.',
                                        data=result), 201)
        return response_builder(dict(
                                message="Data for creation must be provided."),
                                400)
