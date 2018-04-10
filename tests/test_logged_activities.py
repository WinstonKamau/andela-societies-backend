import json

from.base_test import BaseTestCase
from api.models import LoggedActivity


class LoggedActivitiesTestCase(BaseTestCase):
    """Test activity types endpoints."""

    def setUp(self):
        # inherit parent tests setUp
        super().setUp()

        # add test users and logged activity
        self.test_user.save()
        self.log_alibaba_challenge.save()

    def test_logged_activity_deleted_successfully(self):
        """Test that a logged activity was deleted successfully."""
        message = 'Logged activity has been deleted successfully.'
        logged_activity = LoggedActivity.query.filter_by(
                          name='my logged activity').first()

        response = self.client.delete(
            '/api/v1/users/logged-activities/'+logged_activity.uuid,
            headers=self.header
        )

        self.assertTrue(response.status_code == 200)
        response_details = json.loads(response.get_data(as_text=True))

        self.assertEqual(message, response_details['message'])

    def test_delete_nonexistant_logged_activity(self):
        """Test a scenario where a logged activity
        to be deleted does not exist.
        """
        message = 'Logged Activity does not exist!'
        logged_activity_id = 'qwerfdse-23232-ucvhh-1233'
        response = self.client.delete(
            '/api/v1/users/logged-activities/'+logged_activity_id,
            headers=self.header
        )

        self.assertTrue(response.status_code == 404)
        response_details = json.loads(response.get_data(as_text=True))

        self.assertEqual(message, response_details['message'])
