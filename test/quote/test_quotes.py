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
        response = self.client.post("/quote/quotes/", data, format="json").json()

        obj = Quote.objects.first()

        assert response == {
            "qid": obj.qid,
            "date_effective": "2022-01-01T00:00:00Z",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"zipcode": 99999, "state": "WA"},
            "cost_monthly": "13.99",
            "cost_biannually": "83.91",
            "breakdown_monthly": {
                "fees": {
                    "canceled": {"applies": True, "multiplier": 0.15, "money": 1.5},
                    "state_with_volcano": {
                        "applies": True,
                        "multiplier": 0.25,
                        "money": 2.5,
                    },
                },
                "discounts": {
                    "canceled": {"applies": False, "multiplier": 0.1, "money": 0},
                    "owns_property": {"applies": False, "multiplier": 0.2, "money": 0},
                },
            },
            "breakdown_biannually": {
                "fees": {
                    "canceled": {"applies": True, "multiplier": 0.15, "money": 8.99},
                    "state_with_volcano": {
                        "applies": True,
                        "multiplier": 0.25,
                        "money": 14.98,
                    },
                },
                "discounts": {
                    "canceled": {"applies": False, "multiplier": 0.1, "money": 0},
                    "owns_property": {"applies": False, "multiplier": 0.2, "money": 0},
                },
            },
        }

    def test_create_with_qid_provided(self):
        provided_qid = "FFFFFFFFFF"
        data = {
            "qid": provided_qid,
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"state": "WA", "zipcode": "99999"},
        }
        response = self.client.post("/quote/quotes/", data, format="json").json()
        assert response["qid"] != provided_qid

    def test_dedupe_address(self):
        data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"state": "WA", "zipcode": "99999"},
        }

        # we should have two quotes but only one address
        self.client.post("/quote/quotes/", data, format="json")
        self.client.post("/quote/quotes/", data, format="json")

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
        response = self.client.post("/quote/quotes/", data, format="json")
        qid = response.json()["qid"]

        response = self.client.get(f"/quote/quotes/{qid}/", format="json").json()

        assert response == {
            "qid": qid,
            "date_effective": "2022-01-01T00:00:00Z",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"zipcode": 99999, "state": "WA"},
            "cost_monthly": "13.99",
            "cost_biannually": "83.91",
            "breakdown_monthly": {
                "fees": {
                    "canceled": {"applies": True, "multiplier": 0.15, "money": 1.5},
                    "state_with_volcano": {
                        "applies": True,
                        "multiplier": 0.25,
                        "money": 2.5,
                    },
                },
                "discounts": {
                    "canceled": {"applies": False, "multiplier": 0.1, "money": 0},
                    "owns_property": {"applies": False, "multiplier": 0.2, "money": 0},
                },
            },
            "breakdown_biannually": {
                "fees": {
                    "canceled": {"applies": True, "multiplier": 0.15, "money": 8.99},
                    "state_with_volcano": {
                        "applies": True,
                        "multiplier": 0.25,
                        "money": 14.98,
                    },
                },
                "discounts": {
                    "canceled": {"applies": False, "multiplier": 0.1, "money": 0},
                    "owns_property": {"applies": False, "multiplier": 0.2, "money": 0},
                },
            },
        }

    def test_get_all(self):
        data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"state": "WA", "zipcode": "99999"},
        }
        # create 5 quotes
        [self.client.post("/quote/quotes/", data, format="json") for _ in range(5)]

        response = self.client.get("/quote/quotes/", format="json").json()

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
        response = self.client.post(
            "/quote/quotes/", initial_data, format="json"
        ).json()
        initial_qid = response["qid"]

        new_data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": None,
            "is_owned": True,
            "address": {"state": "WA", "zipcode": "99999"},
        }
        response = self.client.patch(
            f"/quote/quotes/{initial_qid}/", new_data, format="json"
        ).json()

        obj = Quote.objects.first()

        assert response == {
            "qid": obj.qid,
            "date_effective": "2022-01-01T00:00:00Z",
            "date_previous_canceled": None,
            "is_owned": True,
            "address": {"zipcode": 99999, "state": "WA"},
            "cost_monthly": "9.49",
            "cost_biannually": "56.94",
            "breakdown_monthly": {
                "fees": {
                    "canceled": {"applies": False, "multiplier": 0.15, "money": 0},
                    "state_with_volcano": {
                        "applies": True,
                        "multiplier": 0.25,
                        "money": 2.5,
                    },
                },
                "discounts": {
                    "canceled": {"applies": True, "multiplier": 0.1, "money": 1.0},
                    "owns_property": {"applies": True, "multiplier": 0.2, "money": 2.0},
                },
            },
            "breakdown_biannually": {
                "fees": {
                    "canceled": {"applies": False, "multiplier": 0.15, "money": 0},
                    "state_with_volcano": {
                        "applies": True,
                        "multiplier": 0.25,
                        "money": 14.98,
                    },
                },
                "discounts": {
                    "canceled": {"applies": True, "multiplier": 0.1, "money": 5.99},
                    "owns_property": {
                        "applies": True,
                        "multiplier": 0.2,
                        "money": 11.99,
                    },
                },
            },
        }


class TestQuoteDelete(APITestCase):
    def test_delete(self):
        data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"state": "WA", "zipcode": "99999"},
        }
        self.client.post("/quote/quotes/", data, format="json")

        obj = Quote.objects.first()

        assert obj is not None

        response = self.client.delete(f"/quote/quotes/{obj.qid}/")
        assert response.status_code == 204
        assert Quote.objects.first() is None
