from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import PricingConfig, PricingConfigLog
from django_json_widget.widgets import JSONEditorWidget


class PricingConfigForm(forms.ModelForm):
    class Meta:
        model = PricingConfig
        fields = '__all__'

    def clean_days_of_week(self):
        days = self.cleaned_data['days_of_week']
        if not all(0 <= day <= 6 for day in days):
            raise ValidationError("Days must be between 0-6")
        return days

    def clean_time_multipliers(self):
        tm = self.cleaned_data['time_multipliers']
        try:
            thresholds = [t['threshold'] for t in tm]
            if thresholds != sorted(thresholds):
                raise ValidationError("Thresholds must be in ascending order")
        except (TypeError, KeyError):
            raise ValidationError("Invalid format. Use: [{'threshold': 60, 'multiplier': 1.0}]")
        return tm
    

@admin.register(PricingConfig)
class PricingConfigAdmin(admin.ModelAdmin):
    form = PricingConfigForm
    list_display = ('name', 'is_active', 'base_price', 'base_distance')
    list_filter = ('is_active',)
    actions = ['activate', 'deactivate']

    def save_model(self, request, obj, form, change):
        if change:
            original = PricingConfig.objects.get(pk=obj.pk)
            changes = {}
            for field in ['name', 'is_active', 'days_of_week', 'base_distance', 
                         'base_price', 'additional_distance_price', 'time_multipliers',
                         'free_waiting_minutes', 'waiting_charge_per_interval', 'waiting_charge_interval']:
                old_val = getattr(original, field)
                new_val = getattr(obj, field)
                if old_val != new_val:
                    changes[field] = {'old': old_val, 'new': new_val}
            
            if changes:
                PricingConfigLog.objects.create(
                    config=obj,
                    changed_by=request.user,
                    changes=changes
                )
        super().save_model(request, obj, form, change)

    def activate(self, request, queryset):
        queryset.update(is_active=True)
    activate.short_description = "Activate selected configs"

    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
    deactivate.short_description = "Deactivate selected configs"

@admin.register(PricingConfigLog)
class PricingConfigLogAdmin(admin.ModelAdmin):
    list_display = ('config', 'changed_by', 'changed_at')
    readonly_fields = ('config', 'changed_by', 'changed_at', 'changes')
    date_hierarchy = 'changed_at'    