from rest_framework.test import APITestCase

from quote.models import Quote, Address


class TestQuoteCreate(APITestCase):
    def test_create(self):
        data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"state": "WA", "zipcode": "99999"},
        }
        response = self.client.post("/quotes/", data, format="json")

        obj = Quote.objects.first()

        assert response.json() == {
            "qid": obj.qid,
            "date_effective": "2022-01-01T00:00:00Z",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "cost_monthly": 13.986,
            "cost_biannually": 83.916,
            "address": {"zipcode": 99999, "state": "WA"},
        }

    def test_dedupe_address(self):
        data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"state": "WA", "zipcode": "99999"},
        }

        # we should have two quotes but only one address
        self.client.post("/quotes/", data, format="json")
        self.client.post("/quotes/", data, format="json")

        assert Quote.objects.count() == 2
        assert Address.objects.count() == 1


class TestQuoteGet(APITestCase):
    def test_get_one(self):
        data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"state": "WA", "zipcode": "99999"},
        }
        response = self.client.post("/quotes/", data, format="json")
        qid = response.json()["qid"]

        response = self.client.get(f"/quotes/{qid}/", format="json")

        assert response.json() == {
            "qid": qid,
            "date_effective": "2022-01-01T00:00:00Z",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "cost_monthly": 13.986,
            "cost_biannually": 83.916,
            "address": {"zipcode": 99999, "state": "WA"},
        }

    def test_get_all(self):
        data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"state": "WA", "zipcode": "99999"},
        }
        # create 5 quotes
        [self.client.post("/quotes/", data, format="json") for _ in range(5)]

        response = self.client.get(f"/quotes/", format="json").json()

        assert response["count"] == 5
        assert "next" in response
        assert "previous" in response
        assert "results" in response
        assert len(response["results"]) == 5


class TestQuoteEdit(APITestCase):
    def test_edit(self):
        initial_data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"state": "WA", "zipcode": "99999"},
        }
        self.client.post("/quotes/", initial_data, format="json")
        new_data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": None,
            "is_owned": True,
            "address": {"state": "WA", "zipcode": "99999"},
        }
        response = self.client.post("/quotes/", new_data, format="json")

        obj = Quote.objects.first()

        assert response.json() == {
            "qid": obj.qid,
            "date_effective": "2022-01-01T00:00:00Z",
            "date_previous_canceled": None,
            "is_owned": True,
            "address": {"zipcode": 99999, "state": "WA"},
            "cost_monthly": 9.4905,
            "cost_biannually": 56.943,
        }


class TestQuoteDelete(APITestCase):
    def test_delete(self):
        data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"state": "WA", "zipcode": "99999"},
        }
        response = self.client.post("/quotes/", data, format="json")

        obj = Quote.objects.first()

        assert response.json() == {
            "qid": obj.qid,
            "date_effective": "2022-01-01T00:00:00Z",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "cost_monthly": 13.986,
            "cost_biannually": 83.916,
            "address": {"zipcode": 99999, "state": "WA"},
        }

        response = self.client.delete(f"/quotes/{obj.qid}/")
        assert response.status_code == 204
        assert Quote.objects.first() is None
