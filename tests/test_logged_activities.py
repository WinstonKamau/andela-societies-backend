import json

from.base_test import BaseTestCase
from api.models import LoggedActivity


class LogActivityTestCase(BaseTestCase):
    """Test activity types endpoints."""

    def test_log_activity_is_successful(self):
        self.alibaba_ai_challenge.save()
        self.interview.save()
        self.test_user.save()

        payload = json.dumps(
            dict(activity_id=f'{self.alibaba_ai_challenge.uuid}')
        )
        response = self.client.post(
            'api/v1/logged-activities',
            headers=self.header, data=payload
        )

        # test that request was successful
        self.assertEqual(response.status_code, 201)

        # test response message
        response_content = json.loads(response.get_data(as_text=True))
        self.assertEqual(
            response_content['message'], 'Activity logged successfully'
        )
