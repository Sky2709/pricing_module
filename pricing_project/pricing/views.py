# pricing/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PricingConfig
from decimal import Decimal
import json

class CalculatePriceAPI(APIView):
    def post(self, request):
        data = request.data
        
        # Validate required parameters
        required = ['distance', 'total_ride_time', 'waiting_time', 'day_of_week']
        if missing := [field for field in required if field not in data]:
            return Response(
                {"error": f"Missing fields: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Convert to proper types
            day = int(data['day_of_week'])
            distance = Decimal(str(data['distance']))
            ride_time = Decimal(str(data['total_ride_time']))  # in minutes
            waiting_time = Decimal(str(data['waiting_time']))  # in minutes
        except (TypeError, ValueError) as e:
            return Response(
                {"error": f"Invalid data format: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find active config for this day
        config = PricingConfig.objects.filter(
            is_active=True,
            days_of_week__contains=[day]
        ).first()
        
        if not config:
            return Response(
                {"error": "No pricing configuration available for this day"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calculate distance price
        if distance <= config.base_distance:
            distance_price = config.base_price
        else:
            extra_distance = distance - config.base_distance
            distance_price = config.base_price + (extra_distance * config.additional_distance_price)
        
        # Calculate time multiplier
        time_multiplier = Decimal('1.0')
        if config.time_multipliers:
            # Handle JSON string if needed
            multipliers = config.time_multipliers
            if isinstance(multipliers, str):
                multipliers = json.loads(multipliers)
            
            # Find the appropriate multiplier
            for tier in sorted(multipliers, key=lambda x: x['threshold']):
                if ride_time <= tier['threshold']:
                    time_multiplier = Decimal(str(tier['multiplier']))
                    break
        
        time_price = ride_time * time_multiplier
        
        # Calculate waiting charges
        if waiting_time <= config.free_waiting_minutes:
            waiting_charge = Decimal('0')
        else:
            chargeable_time = waiting_time - config.free_waiting_minutes
            # Ceiling division: intervals = ceil(chargeable_time / interval)
            intervals = -(-chargeable_time // config.waiting_charge_interval)
            waiting_charge = intervals * config.waiting_charge_per_interval
        
        # Calculate total price
        total_price = distance_price + time_price + waiting_charge
        
        return Response({
            "total_price": float(total_price),
            "breakdown": {
                "distance_price": float(distance_price),
                "time_price": float(time_price),
                "waiting_charge": float(waiting_charge)
            },
            "config_used": config.name
        })