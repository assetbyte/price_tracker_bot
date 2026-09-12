from rest_framework import serializers


class TrackingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.BigIntegerField()
    origin_name = serializers.CharField(max_length=255)
    destination_name = serializers.CharField(max_length=255)
    departure_date = serializers.DateField()
    target_price = serializers.DecimalField(
      max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    transport_type = serializers.CharField(max_length=255)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True, default=None
    )
    car_type = serializers.CharField(
        max_length=100, required=False, allow_null=True, default=None
    )
    created_at = serializers.DateTimeField(read_only=True, required=False)
    origin_code = serializers.CharField(max_length=255)
    destination_code = serializers.CharField(max_length=255)
    
class TrackingCreateSerializer(serializers.Serializer):
  user_id = serializers.BigIntegerField()
  origin_code = serializers.CharField(max_length=50)
  destination_code = serializers.CharField(max_length=50)
  origin_name = serializers.CharField(max_length=255)
  destination_name = serializers.CharField(max_length=255)
  departure_date = serializers.DateField()
  transport_type = serializers.CharField(max_length=50, default='train')
  price = serializers.DecimalField(max_digits=10, decimal_places=2)
  target_price = serializers.DecimalField(max_digits=10, decimal_places=2)
  car_type = serializers.CharField(
      max_length=100, required=False, allow_null=True, default=None
  )
