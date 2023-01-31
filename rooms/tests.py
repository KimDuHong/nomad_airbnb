from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESC = "Amenity Des"
    URL = "/api/v1/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):

        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    def test_create_amenity(self):
        response = self.client.post(
            self.URL,
            data={
                "name": self.NAME,
                "description": self.DESC,
            },
        )
        data = response.json()
        self.assertEqual(response.status_code, 200, "NOT 200 CODE")

        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 400, "NOT 400 CODE")
        self.assertIn("name", response.json())

        response = self.client.post(
            self.URL,
            data={
                "name": "a" * 151,
                "description": self.DESC,
            },
        )
        data = response.json()
        self.assertEqual(response.status_code, 400, "name length")

        response = self.client.post(
            self.URL,
            data={
                "name": "a",
                "description": "a" * 151,
            },
        )
        data = response.json()
        self.assertEqual(response.status_code, 400, "desc length")


class TestAmenity(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity Des"
    URL = "/api/v1/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenitiy_not_found(self):
        response = self.client.get(self.URL + "2/")
        self.assertEqual(response.status_code, 404, "Test One")

    def test_get_amenity(self):

        response = self.client.get(self.URL + "1/")
        self.assertEqual(response.status_code, 200, "Test Two")

        data = response.json()
        self.assertEqual(
            data["name"] + data["description"],
            self.NAME + self.DESC,
            "Test Three",
        )

    def test_put_amentity(self):
        response = self.client.put(
            self.URL + "1/",
            data={
                "name": self.NAME,
                "description": self.DESC,
            },
        )
        data = response.json()
        self.assertEqual(response.status_code, 200, "Test Put")
        self.assertIn("name", data)
        self.assertIn("description", data)

        response = self.client.put(self.URL + "1/", data={"name": ""})
        self.assertEqual(response.status_code, 400, "name_null check")

        response = self.client.put(self.URL + "1/", data={"name": "a" * 151})
        self.assertEqual(response.status_code, 400, "name_len check")

        response = self.client.put(self.URL + "1/", data={"description": "1"})
        self.assertEqual(response.status_code, 200, "Test Put description")

        response = self.client.put(self.URL + "1/", data={"description": "1" * 151})
        self.assertEqual(response.status_code, 400, "Test Put description")

    def test_delete_amenity(self):
        response = self.client.delete(self.URL + "1/")
        self.assertEqual(response.status_code, 204, "Test Four ")
        response = self.client.get(self.URL + "1/")
        self.assertEqual(response.status_code, 404, "404")


class TestRoom(APITestCase):
    URL = "/api/v1/rooms/"

    def setUp(self):
        user = User.objects.create(
            username="TestUser",
        )
        user.set_password("TestPassword")
        user.save()
        self.user = user

    def test_create_room(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403, "Authorization Required")

        self.client.force_login(self.user)
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 400, "Serializer check error")
