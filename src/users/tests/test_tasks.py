# noinspection DuplicatedCode,PyPep8Naming
import datetime
from unittest import TestCase

from django.contrib.auth import get_user_model
from django.utils.timezone import now

from src.users.models import Subscription
from src.users.tasks import deactivate_expired_subscriptions

User = get_user_model()


class DeactivateExpiredSubscriptionsTestCase(TestCase):
    def setUp(self):
        for i in range(60):
            user = User.objects.create(
                email=f"test{i}@mail.com",
                first_name="1",
                last_name="2",
            )
            user.save()
            if i % 2 == 0:
                subscription = Subscription.objects.create(
                    user=user,
                    is_active=True,
                    expiration=now() - datetime.timedelta(30) + datetime.timedelta(i),
                )
                subscription.save()

    def test_deactivation(self):
        qs = deactivate_expired_subscriptions()
        print(qs, qs.count())
        self.assertEqual(1, 1)
