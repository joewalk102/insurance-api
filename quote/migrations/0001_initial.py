# Generated by Django 4.0.4 on 2022-05-28 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("zipcode", models.IntegerField()),
                ("state", models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name="Quote",
            fields=[
                (
                    "qid",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                ("date_effective", models.DateTimeField()),
                ("date_previous_canceled", models.DateField(null=True)),
                ("is_owned", models.BooleanField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "address",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="quote.address",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuotePurchase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("payment_amount", models.FloatField()),
                (
                    "payment_frequency",
                    models.CharField(
                        choices=[("BA", "Biannually"), ("MO", "Monthly")], max_length=2
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("discount_canceled_amt", models.FloatField()),
                ("discount_owns_property_amt", models.FloatField()),
                ("fee_canceled_amt", models.FloatField()),
                ("fee_state_amt", models.FloatField()),
                (
                    "quote",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="quote.quote",
                    ),
                ),
            ],
        ),
    ]
