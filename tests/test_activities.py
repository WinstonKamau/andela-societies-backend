"""Tests for Activities Module."""
import json
from tests.base_test import BaseTestCase


class ActivitiesTestCase(BaseTestCase):
    """Test activities endpoints."""

    def test_create_activity(self):
        """Test that an activity has been created successfully."""
        new_activity = dict(name="tech congress",
                            description="all about tech",
                            activity_type_id=self.get_activity_type_id(
                                "Tech Event"),
                            activity_date='2020-11-20')

        response = self.client.post('/api/v1/activities',
                                    data=json.dumps(new_activity),
                                    headers=self.header,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)

        message = "Activity created succesfully."
        response_details = json.loads(response.data)

        self.assertEqual(message, response_details["message"])

    def test_description_not_given(self):
        """Test for where description isn't provided in request object."""
        new_activity = dict(name="hackathon",
                            activity_type_id=self.get_activity_type_id(
                                "Tech Event"),
                            activity_date='2020-11-20')

        response = self.client.post('/api/v1/activities',
                                    data=json.dumps(new_activity),
                                    headers=self.header,
                                    content_type='application/json')

        response_details = json.loads(response.data)

        self.assertEqual(response.status_code, 400)

        message = 'A description is required.'

        self.assertEqual(message, response_details['description']['message'])

    def test_name_not_given(self):
        """Test for where name is not provided in request object."""
        new_activity = dict(description="all about tech",
                            activity_date='2020-11-20')

        response = self.client.post('/api/v1/activities',
                                    data=json.dumps(new_activity),
                                    headers=self.header,
                                    content_type='application/json')

        response_details = json.loads(response.data)

        self.assertEqual(response.status_code, 400)

        message = 'A name is required.'

        self.assertEqual(message, response_details['name']['message'])

    def test_save_existing_activity(self):
        """Test attempt to save an already existing activity."""
        # store activity to the database
        self.js_meet_up.save()

        existing_activity = dict(
            name="Nairobi Js meetup",
            description="all about js",
            activity_type_id=self.get_activity_type_id(
                "Tech Event"),
            activity_date='2020-11-20')

        # attempt to save the already existing activity
        response = self.client.post('/api/v1/activities',
                                    data=json.dumps(existing_activity),
                                    headers=self.header,
                                    content_type='application/json')
        message = "Activity already exists!"

        response_details = json.loads(response.data)

        self.assertEqual(response.status_code, 409)

        self.assertEqual(message, response_details["message"])

    def test_non_existant_activity_type(self):
        """Test if activity type does not exist."""
        new_activity = dict(name="Tech Festival",
                            description="learn new things in tech",
                            activity_type_id="123-ab4-341",
                            activity_date="2020-11-20")

        response = self.client.post('/api/v1/activities',
                                    data=json.dumps(new_activity),
                                    headers=self.header,
                                    content_type='application/json')
        message = "Activity Type does not exist!"
        response_details = json.loads(response.data)

        self.assertEqual(response.status_code, 404)

        self.assertEqual(message, response_details["message"])

    def test_activity_date_not_given(self):
        """Test of activity date is not provided."""
        new_activity = dict(name="tech congress",
                            description="all about tech",
                            activity_type_id=self.get_activity_type_id(
                                "Tech Event"))

        response = self.client.post('/api/v1/activities',
                                    data=json.dumps(new_activity),
                                    headers=self.header,
                                    content_type='application/json')

        message = "An activity date is required."
        response_details = json.loads(response.data)

        self.assertEqual(response.status_code, 400)

        self.assertEqual(message, response_details["activity_date"]["message"])

    def test_past_activity_date(self):
        """Test if activity date given is in the past."""
        new_activity = dict(name="tech congress",
                            description="all about tech",
                            activity_type_id=self.get_activity_type_id(
                                "Tech Event"),
                            activity_date="2016-1-20")

        response = self.client.post('/api/v1/activities',
                                    data=json.dumps(new_activity),
                                    headers=self.header,
                                    content_type='application/json')

        message = "Date is in the past! Please enter a valid date."
        response_details = json.loads(response.data)

        self.assertEqual(response.status_code, 400)

        self.assertEqual(message, response_details["activity_date"]["message"])

    def test_activity_is_invalid(self):
        new_activity = dict(name="Open Source App",
                            description="open source project",
                            activity_type_id=self.get_activity_type_id(
                                "Tech Event"),
                            activity_date="2020-1-20")

        response = self.client.post('/api/v1/activities',
                                    data=json.dumps(new_activity),
                                    headers=self.header,
                                    content_type='application/json')

        message = 'This is not a valid activity!'
        response_details = json.loads(response.data)

        self.assertEqual(response.status_code, 400)

        self.assertEqual(message, response_details["message"])

