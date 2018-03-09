import json

from api.models import Activity
from tests.base_test import BaseTestCase


class ActivitiesTestCase(BaseTestCase):
    """Test activities endpoints."""

    def test_get_activities(self):
        response = self.client.get('api/v1/activities', headers=self.header)
        self.assertEqual(response.status_code, 200)

        activities = Activity.query.all()
        response_json = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(activities), len(response_json['data']))

    def test_get_activities_by_unauthorized_user(self):
        response = self.client.get(
            'api/v1/activities', headers=self.bad_token_header)
        self.assertEqual(response.status_code, 401)

        expected_message = "Unauthorized. The authorization token"
        " supplied is invalid"
        response_json = json.loads(response.get_data(as_text=True))
        self.assertEqual(expected_message, response_json["message"])

    def test_get_activities_without_authorization_header(self):
        response = self.client.get(
            'api/v1/activities')
        self.assertEqual(response.status_code, 400)

        expected_message = "Bad request. Header does not contain authorization"
        " token"
        response_json = json.loads(response.get_data(as_text=True))
        self.assertEqual(expected_message, response_json["message"])
