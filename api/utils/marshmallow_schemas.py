from marshmallow import Schema, fields, validate
from api.models import User


class BaseSchema(Schema):
    uuid = fields.String(dump_only=True, validate=[
        validate.Length(max=36)])
    name = fields.String(required=True)
    photo = fields.String()
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    description = fields.String()


class ActivityTypesSchema(BaseSchema):
    description = fields.String(
        required=True,
        error_messages={
            'required': 'A description is required.'
            }
    )
    value = fields.Integer(
        required=True,
        error_messages={
            'required': 'Please send the activity points value'
            }
    )


class LoggedActivitySchema(BaseSchema):
    status = fields.String(dump_only=True)
    value = fields.Integer(
        required=True,
        error_messages={
            'required': 'Please send the activity points value'
            }
    )
    user = fields.String(dump_only=True, attribute='user.name')
    society = fields.String(dump_only=True, attribute='society.name')
    activity = fields.String(dump_only=True, attribute='activity.name')
    approved_by = fields.Method('get_approver', dump_only=True)

    @staticmethod
    def get_approver(obj):
        if obj.approver_id:
            approver = User.query.get(obj.approver_id)
            return approver.name
        else:
            return


get_activity_types_schema = ActivityTypesSchema(many=True)
get_logged_activities_schema = LoggedActivitySchema(many=True)
