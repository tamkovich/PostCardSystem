from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from card.models import UserCard
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class UserCardAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='testcfuser', email='test@gmail.com')
        user_obj.set_password("somerandompassword")
        user_obj.save()
        cards = UserCard.objects.create(user=user_obj,
                                        city="Barcelona",
                                        visited_date="2018-05-27T09:04:32Z",
                                        transport="airplane",
                                        value=150.99,
                                        )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_card(self):
        card_count = UserCard.objects.count()
        self.assertEqual(card_count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse("api-cards:card-create")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        data = {
                "city": "Barcelona",
                "visited_date": "2018-05-27T09:04:32Z",
                "transport": "airplane",
                "value": 150.99
        }
        url = api_reverse("api-cards:card-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        card = UserCard.objects.first()
        data = {}
        url = card.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        card = UserCard.objects.first()
        url = card.get_api_url()
        data = {
            "city": "Barcelona",
            "visited_date": "2018-05-27T09:04:32Z",
            "transport": "airplane",
            "value": 150.99
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        card = UserCard.objects.first()
        print(card.city)
        url = card.get_api_url()
        data = {
            "city": "Barcelona",
            "visited_date": "2018-05-27T09:04:32Z",
            "transport": "airplane",
            "value": 151.99
        }
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    # def test_post_item_with_user(self):
    #     user_obj = User.objects.first()
    #     payload = payload_handler(user_obj)
    #     token_rsp = encode_handler(payload)
    #     self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
    #     data = {
    #             "city": "Barcelona",
    #             "visited_date": "2018-05-27T09:04:32Z",
    #             "transport": "airplane",
    #             "value": 150.99
    #     }
    #     url = api_reverse("api-cards:card-create")
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        owner = User.objects.create(username="tuo222")
        card = UserCard.objects.create(
            user=owner,
            city="Barcelona",
            visited_date="2018-05-27T09:04:32Z",
            transport="airplane",
            value=150.99,
        )

        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)

        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        url = card.get_api_url()
        data = {
                "city": "Barcelona",
                "visited_date": "2018-05-27T09:04:32Z",
                "transport": "airplane",
                "value": 150.99
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_login(self):
        data = {
            'username': 'testcfuser',
            'password': 'somerandompassword',
        }
        url = api_reverse("api-login")
        self.client.post(url, data)
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
