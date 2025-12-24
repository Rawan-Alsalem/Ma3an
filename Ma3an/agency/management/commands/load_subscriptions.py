from django.core.management.base import BaseCommand
from agency.models import Subscription

class Command(BaseCommand):
    help = "Load default subscription plans"

    def handle(self, *args, **options):

        subscriptions = [
            {
                "subscriptionType": "basic",
                "price": 0.00,
                "tours_limit": 3,
                "supervisors_limit": 2,
                "travelers_limit": 10,
            },
            {
                "subscriptionType": "standard",
                "price": 1999.00,
                "tours_limit": 10,
                "supervisors_limit": 5,
                "travelers_limit": 100,
            },
            {
                "subscriptionType": "premium",
                "price": 3999.00,
                "tours_limit": None,
                "supervisors_limit": None,
                "travelers_limit": None,
            },
        ]

        created_count = 0
        updated_count = 0

        for data in subscriptions:
            obj, created = Subscription.objects.update_or_create(
                subscriptionType=data["subscriptionType"],
                defaults={
                    "price": data["price"],
                    "tours_limit": data["tours_limit"],
                    "supervisors_limit": data["supervisors_limit"],
                    "travelers_limit": data["travelers_limit"],
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✔ Subscriptions loaded | Created: {created_count}, Updated: {updated_count}"
            )
        )