"""Test Authentication."""
import json
from tests.base_test import BaseTestCase


class AuthTestCase(BaseTestCase):
    """Test Authentication of Users."""

    def test_auth_valid_header(self):
        """Test API accepts valid auth header."""
        response = self.client.get('api/v1/user/profile', headers=self.header)

        self.assertEqual(response.status_code, 200)

    def test_auth_no_auth_header(self):
        """Test API rejects lack of auth header."""
        response = self.client.get('api/v1/user/profile',
                                   headers=self.no_header)

        response_json = json.loads(response.get_data(as_text=True))
        response_message = response_json['message']

        self.assertEqual(response.status_code, 400)
        self.assertIn("not contain authorization", response_message)

    def test_auth_expired_token(self):
        """Test API rejects expired token."""
        response = self.client.get('api/v1/user/profile',
                                   headers=self.expired_header)

        response_json = json.loads(response.get_data(as_text=True))
        response_message = response_json['message']

        self.assertEqual(response.status_code, 401)
        self.assertIn("expired", response_message)

    def test_auth_invalid_token(self):
        """Test API rejects invalid token."""
        response = self.client.get('api/v1/user/profile',
                                   headers=self.invalid_header)

        response_json = json.loads(response.get_data(as_text=True))
        response_message = response_json['message']

        self.assertEqual(response.status_code, 401)
        self.assertIn("invalid", response_message)

    def test_auth_invalid_payload(self):
        """Test API rejects invalid payload reuqests."""
        response = self.client.get('api/v1/user/profile',
                                   headers=self.invalid_payload_header)

        # response_json = json.loads(response.get_data(as_text=True))
        # response_message = response_json['message']

        self.assertEqual(response.status_code, 400)
        # self.assertIn("payload submitted is invalid", response_message)
