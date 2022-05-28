import string
from random import choice

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from utils.const import DISCOUNTS
from utils.const import FEES
from utils.const import VOLCANO_INSURANCE

LETTERS_AND_NUMBERS = string.ascii_uppercase + string.digits


class Address(models.Model):
    states_lookup = {
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DC",
        "DE",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
    }
    states_with_volcanoes = {
        "AK",
        "AZ",
        "CA",
        "CO",
        "HI",
        "ID",
        "NV",
        "NM",
        "OR",
        "UT",
        "WA",
        "WY",
    }

    zipcode = models.IntegerField()
    state = models.CharField(max_length=2)

    @property
    def has_volcano(self):
        return self.state in self.states_with_volcanoes


class Quote(models.Model):
    qid = models.CharField(primary_key=True, max_length=10)
    date_effective = models.DateTimeField(null=False)
    date_previous_canceled = models.DateField(null=True)
    is_owned = models.BooleanField(null=False)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cost_monthly = None
        self._cost_biannually = None
        self._breakdown_monthly = None
        self._breakdown_biannually = None

    def save(self, **kwargs):
        """Overwriting the `save` method to insert a unique `qid`"""
        if not self.qid:
            rand_id = None
            try:
                while True:
                    # Try until we find a QID that doesn't already exist.
                    rand_id = "".join([choice(LETTERS_AND_NUMBERS) for _ in range(10)])
                    Quote.objects.get(qid=rand_id)
            except ObjectDoesNotExist:
                pass
            self.qid = rand_id
        return super(Quote, self).save(**kwargs)

    @property
    def additional_fees(self):
        return {
            "canceled": {
                "applies": self.date_previous_canceled is not None,
                "multiplier": FEES.CANCELED_POLICY.PERCENT / 100,
            },
            "state_with_volcano": {
                "applies": self.address.has_volcano,
                "multiplier": FEES.STATE_WITH_VOLCANO.PERCENT / 100,
            },
        }

    @property
    def discounts(self):
        return {
            "canceled": {
                "applies": self.date_previous_canceled is None,
                "multiplier": DISCOUNTS.NO_CANCELLED_POLICY.PERCENT / 100,
            },
            "owns_property": {
                "applies": self.is_owned,
                "multiplier": DISCOUNTS.OWNED_PROPERTY.PERCENT / 100,
            },
        }

    def _calc_fees(self, base_cost):
        policy_cost = base_cost
        fees = self.additional_fees
        discounts = self.discounts
        for modifier in fees.values():
            if modifier["applies"]:
                modifier["money"] = base_cost * modifier["multiplier"]
                policy_cost += modifier["money"]
            else:
                modifier["money"] = 0
        for modifier in discounts.values():
            if modifier["applies"]:
                modifier["money"] = base_cost * modifier["multiplier"]
                policy_cost -= modifier["money"]
            else:
                modifier["money"] = 0
        return policy_cost, {"fees": fees, "disctounts": discounts}

    @property
    def cost_and_breakdown_biannually(self):
        if self._cost_biannually is None or self._breakdown_biannually is None:
            self._cost_biannually, self._breakdown_biannually = self._calc_fees(
                VOLCANO_INSURANCE.BASE_COST_BIANNUALLY
            )
        return self._cost_biannually, self._breakdown_biannually

    @property
    def cost_biannually(self):
        return self.cost_and_breakdown_biannually[0]

    @property
    def breakdown_biannually(self):
        return self.cost_and_breakdown_biannually[1]

    @property
    def cost_and_breakdown_monthly(self):
        if self._cost_monthly is None or self._breakdown_monthly is None:
            self._cost_monthly, self._breakdown_monthly = self._calc_fees(
                VOLCANO_INSURANCE.BASE_COST_MONTHLY
            )
        return self._cost_monthly, self._breakdown_monthly

    @property
    def cost_monthly(self):
        return self.cost_and_breakdown_monthly[0]

    @property
    def breakdown_monthly(self):
        return self.cost_and_breakdown_monthly[0]
