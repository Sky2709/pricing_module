from django.db import models
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder


User = get_user_model()

class PricingConfig(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    days_of_week = models.JSONField(default=list)  # Store days of the week as a list of strings

    base_distance = models.DecimalField(max_digits=5, decimal_places=2)
    base_price =models.DecimalField(max_digits=8, decimal_places=2)
    additional_distance_price = models.DecimalField(max_digits=8, decimal_places=2)


    time_multipliers = models.JSONField(
        default = list,
        help_text="JSON: [{'threshold':60, 'multiplier': 1.0}, ... ]"
    )

    free_waiting_minutes = models.IntegerField(default=0)
    waiting_charge_per_interval = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    waiting_charge_interval = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class PricingConfigLog(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.CASCADE, related_name='logs')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField(encoder=DjangoJSONEncoder)

    def __str__(self):
        return f"{self.config.name} - {self.changed_at}"    