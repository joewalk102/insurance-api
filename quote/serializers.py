from rest_framework import serializers

from quote.models import Address, Quote


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
        ]

    qid = serializers.CharField(read_only=True)
    date_effective = serializers.DateTimeField()
    date_previous_canceled = serializers.DateField(required=False, allow_null=True)
    is_owned = serializers.BooleanField()

    cost_biannually = serializers.SerializerMethodField("get_cost_biannually")
    cost_monthly = serializers.SerializerMethodField("get_cost_monthly")

    address = AddressSerializer(required=True)

    def create(self, validated_data):
        for k, v in validated_data.items():
            if k == "address":
                validated_data[k], _ = AddressSerializer().create(v)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            if k == "address":
                validated_data[k], _ = AddressSerializer().create(v)
        return super().create(validated_data)

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
