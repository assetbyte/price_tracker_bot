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
    created_at = serializers.DateTimeField(read_only=True, required=False)
    
class TrackingCreateSerializer(serializers.Serializer):
    origin_name = serializers.CharField(max_length=255)
    destination_name = serializers.CharField(max_length=255)
    departure_date = serializers.DateField()
    target_price = serializers.DecimalField(
      max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    
        