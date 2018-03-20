"""Module to house setup, teardown and utility class for testing."""

import datetime
from unittest import TestCase

from api.models import Activity, Point, Society, User, db
from app import create_app
from jose import jwt


class BaseTestCase(TestCase):
    """Contain utility required for testing."""

    exp_date = datetime.datetime.utcnow()
    test_payload = {
        "UserInfo": {
            "email": "test.test@andela.com",
            "first_name": "test",
            "id": "-Ktest_id",
            "last_name": "test",
            "name": "test test",
            "picture": "https://www.link.com",
            "roles": {
                    "Andelan": "-Ktest_andelan_id",
                    "Fellow": "-Ktest_fellow_id"
            }
        },
        "exp": exp_date + datetime.timedelta(days=1)
    }

    test_expired_payload = {
        "UserInfo": {
            "email": "test.test@andela.com",
            "first_name": "test",
            "id": "-Ktest_id",
            "last_name": "test",
            "name": "test test",
            "picture": "https://www.link.com",
            "roles": {
                    "Andelan": "-Ktest_andelan_id",
                    "Fellow": "-Ktest_fellow_id"
            }
        },
        "exp": exp_date - datetime.timedelta(days=300)
    }

    test_invalid_payload = {
        "UserInfo": {
            "emal": "test.test@andela.com",
            "first_name": "test",
            "ids": "-Ktest_id",
            "last_name": "test",
            "name": "test test",
            "pic": "https://www.link.com",
            "roles": {
                    "Andelan": "-Ktest_andelan_id",
                    "Fellow": "-Ktest_fellow_id"
            }
        },
        "exp": exp_date + datetime.timedelta(days=1)
    }

    def setUp(self):
        """Setup function to configure test enviroment."""
        self.app = create_app("Testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        # test client
        self.client = self.app.test_client()

        self.header = {
            "Authorization": self.generate_token(self.test_payload)
        }

        self.no_header = {
            "Lolz": self.generate_token(self.test_expired_payload)
        }

        self.expired_header = {
            "Authorization": self.generate_token(self.test_expired_payload)
        }

        self.invalid_header = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc\
            2VySW5mbyI6eyJpZCI6Ii1LZWJnOXF3dE5wWTBpS1NoQVBHIiwiZW1haWwiOiJqb25h\
            dGhhbi5rYW1hdUBhbmRlbGEuY29tIiwiZmlyc3RfbmFtZSI6IkpvbmF0aGFuIiwibGF\
            zdF9uYW1lIjoiS2FtYXUiLCJuYW1lIjoiSm9uYXRoYW4gS2FtYXUiLCJwaWN0dXJlIj\
            oiaHR0cHM6Ly9saDUuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy1iY0pfd0hXUVAxTS9BQ\
            UFBQUFBQUFBSS9BQUFBQUFBQUFDNC9SVGV2R0g5TTFNYy9waG90by5qcGc_c3o9NTA"
        }

        self.invalid_payload_header = {
            "Authorization": self.generate_token(self.test_invalid_payload)
        }

        # mock user
        self.member = User(email="someonecool.andela.com",
                           name="thecoolest",
                           uuid="-Ksomeid",
                           role="member",
                           country="ke/ug/niger/ny/sa/tz/rw")

        self.admin = User(email="coolAdmin.andela.com",
                          name="thecoolestAdmin",
                          uuid="-KsomeidAdmin",
                          role="admin",
                          country="ke/ug/niger/ny/sa/tz/rw")

        # mock societies
        self.istelle = Society(name="istelle",
                               photo="url/imgae",
                               logo="url/image",
                               color_scheme="#00ff4567")

        self.sparks = Society(name="sparks",
                              photo="url/imgae",
                              logo="url/image",
                              color_scheme="#00ff4567")

        self.phenix = Society(name="phenix",
                              photo="url/imgae",
                              logo="url/image",
                              color_scheme="#00ff4567")
        self.phenix.save()

        # mock points
        self.point = Point(value=2500,
                           name="interview-2017-sep-23rd")

        # mock interview
        self.activity = Activity(
            name="Interview",
            value=50,
            description="members earn 50 points per activity",
            photo="cool/icon/url")

    @staticmethod
    def generate_token(payload):
        """Generate token."""
        token = jwt.encode(payload, "secret", algorithm="HS256")
        return token

    def tearDown(self):
        """Clean up after every test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
