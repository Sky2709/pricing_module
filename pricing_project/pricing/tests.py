# pricing/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import PricingConfig
import json

User = get_user_model()

class PricingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin', password='password'
        )
        self.client = APIClient()
        
        # Create pricing config
        self.config = PricingConfig.objects.create(
            name="Weekday Pricing",
            is_active=True,
            days_of_week=[1, 2, 3],  # Mon, Tue, Wed
            base_distance=3,
            base_price=80,
            additional_distance_price=30,
            time_multipliers=json.dumps([
                {"threshold": 60, "multiplier": 1.0},
                {"threshold": 120, "multiplier": 1.25},
                {"threshold": 180, "multiplier": 2.2}
            ]),
            free_waiting_minutes=3,
            waiting_charge_per_interval=5,
            waiting_charge_interval=3
        )

    def test_config_creation(self):
        self.assertEqual(PricingConfig.objects.count(), 1)
        config = PricingConfig.objects.first()
        self.assertEqual(config.name, "Weekday Pricing")
        self.assertEqual(config.days_of_week, [1, 2, 3])

    def test_price_calculation(self):
        test_cases = [
            # [distance, ride_time, waiting_time, day, expected]
            [2, 30, 2, 2, 80 + 30*1.0 + 0],  # Within base distance
            [4, 30, 2, 2, 80 + 1*30 + 30*1.0 + 0],  # Extra distance
            [3, 90, 2, 2, 80 + 0 + 90*1.25 + 0],  # Higher time tier
            [3, 30, 10, 2, 80 + 0 + 30*1.0 + 15],  # Waiting charges (3 intervals)
            [5, 150, 15, 2, 80 + 2*30 + 150*2.2 + 20]  # All components
        ]
        
        for case in test_cases:
            data = {
                'distance': case[0],
                'total_ride_time': case[1],
                'waiting_time': case[2],
                'day_of_week': case[3]
            }
            response = self.client.post('/pricing/api/calculate-price/', data)
            self.assertEqual(response.status_code, 200)
            self.assertAlmostEqual(response.data['total_price'], case[4], places=2)

    def test_admin_logging(self):
        self.client.force_login(self.user)
        config = PricingConfig.objects.first()
        config.base_price = 90
        config.save()
        
        log = config.logs.first()
        self.assertEqual(log.changes['base_price']['old'], '80.00')
        self.assertEqual(log.changes['base_price']['new'], '90.00')