from rest_framework import serializers

from quote.models import Address, Quote, QuotePurchase


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["zipcode", "state"]

    zipcode = serializers.IntegerField(required=True)
    state = serializers.CharField(max_length=2, required=True)

    def create(self, validated_data):
        return Address.objects.get_or_create(**validated_data)


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = [
            "qid",
            "date_effective",
            "date_previous_canceled",
            "is_owned",
            "address",
            "cost_monthly",
            "cost_biannually",
            "breakdown_monthly",
            "breakdown_biannually",
        ]

    qid = serializers.CharField(required=False)
    date_effective = serializers.DateTimeField()
    date_previous_canceled = serializers.DateField(required=False, allow_null=True)
    is_owned = serializers.BooleanField()
    breakdown_biannually = serializers.JSONField(read_only=True)
    breakdown_monthly = serializers.JSONField(read_only=True)

    cost_biannually = serializers.SerializerMethodField("get_cost_biannually")
    cost_monthly = serializers.SerializerMethodField("get_cost_monthly")

    address = AddressSerializer(required=True)

    def create(self, validated_data):
        if "qid" in validated_data:
            # QID should be generated, not provided.
            del validated_data["qid"]
        for k, v in validated_data.items():
            if k == "address":
                validated_data[k], _ = AddressSerializer().create(v)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            if k == "address":
                validated_data[k], _ = AddressSerializer().create(v)
        return super().update(instance, validated_data)

    def validate(self, attrs):
        try:
            if attrs["address"]["state"] not in Address.states_lookup:
                raise ValueError("Invalid State Provided.")
        except KeyError:
            raise ValueError("`address.state` not provided.")
        # With more time: For more validation, I would add another layer to
        # validate state/zip combination or only accept zip and fill
        # state automatically
        return super().validate(attrs)

    def get_cost_biannually(self, obj):
        return "{:.2f}".format(round(obj.cost_biannually, 2))

    def get_cost_monthly(self, obj):
        return "{:.2f}".format(round(obj.cost_monthly, 2))


class QuotePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotePurchase
        fields = ["payment_frequency", "payment_amount", "quote", "discount_canceled_amt", "discount_owns_property_amt",
                  "fee_canceled_amt", "fee_state_amt", "cost_breakdown", "quote_id", "pk"]

    pk = serializers.IntegerField(read_only=True)
    payment_frequency = serializers.CharField(required=True)
    payment_amount = serializers.FloatField(read_only=True)
    cost_breakdown = serializers.DictField(read_only=True)
    discount_canceled_amt = serializers.FloatField(read_only=True)
    discount_owns_property_amt = serializers.FloatField(read_only=True)
    fee_canceled_amt = serializers.FloatField(read_only=True)
    fee_state_amt = serializers.FloatField(read_only=True)

    quote = QuoteSerializer(read_only=True, required=False)
    quote_id = serializers.CharField(write_only=True)

    def create(self, validated_data: dict):
        # Get the quote from the provided ID
        qid = validated_data["quote_id"]
        quote = Quote.objects.get(qid=qid)
        validated_data["quote"] = quote
        del validated_data["quote_id"]

        if validated_data["payment_frequency"] == "Monthly":
            cost, breakdown = quote.cost_and_breakdown_monthly
        else:
            cost, breakdown = quote.cost_and_breakdown_biannually

        # Set values for this purchase
        validated_data.update(
            payment_amount=cost,
            discount_canceled_amt=breakdown["discounts"]["canceled"]["money"],
            discount_owns_property_amt=breakdown["discounts"]["owns_property"]["money"],
            fee_canceled_amt=breakdown["fees"]["canceled"]["money"],
            fee_state_amt=breakdown["fees"]["state_with_volcano"]["money"],
        )
        return super().create(validated_data)
