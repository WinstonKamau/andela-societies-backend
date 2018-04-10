from marshmallow import (
    Schema, fields, validate, validates_schema, ValidationError
)
from api.models import User, ActivityType


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
    value = fields.Integer(dump_only=True)
    user = fields.String(attribute='user.name', dump_only=True)
    activity_id = fields.String(
        validate=[validate.Length(max=36)], dump_only=True
    )
    activity = fields.String(attribute='activity.name', dump_only=True)
    activity_type = fields.String(
        attribute='activity_type.name', dump_only=True
    )
    activity_type_id = fields.String(
        validate=[validate.Length(max=36)], dump_only=True
    )
    society_id = fields.String(
        validate=[validate.Length(max=36)], dump_only=True
    )
    society = fields.String(attribute='society.name', dump_only=True)
    approved_by = fields.Method('get_approver', dump_only=True)

    @staticmethod
    def get_approver(obj):
        if obj.approver_id:
            approver = User.query.get(obj.approver_id)
            return approver.name
        return


class LogActivitySchema(BaseSchema):
    name = fields.String(required=False)
    activity_id = fields.String(
        validate = [validate.Length(max=36)], load_only=True
    )
    activity_type_id = fields.String(
        validate = [validate.Length(max=36)], load_only=True
    )
    date = fields.Date(load_only=True)
    no_of_interviewees = fields.Integer(load_only=True)

    @validates_schema
    def validate_logged_activity(self, data):
        if (data.get('activity_type_id') and data.get('activity_id')) or not \
                data.get('activity_type_id') and not data.get('activity_id'):
            raise ValidationError(
                'Please send either an activity_type_id or an activity_id only',
                'error'
            )

        if data.get('activity_type_id') and not(data.get('date') and \
                data.get('description')):
            raise ValidationError(
                'Please send a date and description', 'error'
            )

        bootcamp_interviews = ActivityType.query.filter_by(
            name='Bootcamp Interviews').one_or_none()
        if data.get('activity_type_id') == bootcamp_interviews.uuid \
                and not (data.get('date') and data.get('no_of_interviewees')
                         and data.get('description')):
            raise ValidationError(
                'Please send all required fields for a bootcamp interview' \
                ' i.e. a date, number of interviewees and a description',
                'error'
            )


get_activity_types_schema = ActivityTypesSchema(many=True)
get_logged_activities_schema = LoggedActivitySchema(many=True)
single_logged_activity_schema = LoggedActivitySchema()
logged_activity_schema = LoggedActivitySchema()
log_activity_schema = LogActivitySchema()
