from rest_framework.test import APITestCase

from quote.models import Quote
from quote.models import QuotePurchase


class TestPurchaseCreate(APITestCase):
    def test_create(self):
        data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"state": "WA", "zipcode": "99999"},
        }
        qid = self.client.post("/quote/quotes/", data, format="json").json()["qid"]

        response = self.client.post(
            f"/quote/purchase/",
            {"quote_id": qid, "payment_frequency": "Monthly"},
            format="json",
        ).json()

        assert response == {
            "payment_frequency": "Monthly",
            "payment_amount": 13.99,
            "quote": {
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
                        "owns_property": {
                            "applies": False,
                            "multiplier": 0.2,
                            "money": 0,
                        },
                    },
                },
                "breakdown_biannually": {
                    "fees": {
                        "canceled": {
                            "applies": True,
                            "multiplier": 0.15,
                            "money": 8.99,
                        },
                        "state_with_volcano": {
                            "applies": True,
                            "multiplier": 0.25,
                            "money": 14.98,
                        },
                    },
                    "discounts": {
                        "canceled": {"applies": False, "multiplier": 0.1, "money": 0},
                        "owns_property": {
                            "applies": False,
                            "multiplier": 0.2,
                            "money": 0,
                        },
                    },
                },
            },
            "discount_canceled_amt": 0.0,
            "discount_owns_property_amt": 0.0,
            "fee_canceled_amt": 1.5,
            "fee_state_amt": 2.5,
            "pk": 1,
        }


class TestPurchaseGet(APITestCase):
    def test_get_one(self):
        # create quote
        data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"state": "WA", "zipcode": "99999"},
        }
        qid = self.client.post("/quote/quotes/", data, format="json").json()["qid"]

        # create purchase record
        self.client.post(
            f"/quote/purchase/",
            {"quote_id": qid, "payment_frequency": "Monthly"},
            format="json",
        ).json()

        response = self.client.get(f"/quote/purchase/1/", format="json").json()

        assert response == {
            "payment_frequency": "Monthly",
            "payment_amount": 13.99,
            "quote": {
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
                        "owns_property": {
                            "applies": False,
                            "multiplier": 0.2,
                            "money": 0,
                        },
                    },
                },
                "breakdown_biannually": {
                    "fees": {
                        "canceled": {
                            "applies": True,
                            "multiplier": 0.15,
                            "money": 8.99,
                        },
                        "state_with_volcano": {
                            "applies": True,
                            "multiplier": 0.25,
                            "money": 14.98,
                        },
                    },
                    "discounts": {
                        "canceled": {"applies": False, "multiplier": 0.1, "money": 0},
                        "owns_property": {
                            "applies": False,
                            "multiplier": 0.2,
                            "money": 0,
                        },
                    },
                },
            },
            "discount_canceled_amt": 0.0,
            "discount_owns_property_amt": 0.0,
            "fee_canceled_amt": 1.5,
            "fee_state_amt": 2.5,
            "pk": 1,
        }

    def test_get_all(self):
        # create quote
        data = {
            "date_effective": "2022-01-01T00:00:00.000",
            "date_previous_canceled": "2022-01-01",
            "is_owned": False,
            "address": {"state": "WA", "zipcode": "99999"},
        }
        qid = self.client.post("/quote/quotes/", data, format="json").json()["qid"]

        # create purchase record
        data = {"quote_id": qid, "payment_frequency": "Monthly"}
        [self.client.post(f"/quote/purchase/", data, format="json") for _ in range(10)]

        response = self.client.get(f"/quote/purchase/", format="json").json()

        assert response["count"] == 10
        assert "next" in response
        assert "previous" in response
        assert "results" in response
        assert len(response["results"]) == 10
