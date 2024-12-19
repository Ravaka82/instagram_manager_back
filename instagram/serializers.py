from rest_framework import serializers
from .models import InstagramAccount

class InstagramAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramAccount
        fields = '__all__'
