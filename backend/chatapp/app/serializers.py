from rest_framework import serializers
from .models import UserProfile, Rooms, RoomParticipants, Messages, Receivers, BlockedUser
from datetime import timedelta

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'username', 'password', 'avatar', 'address', 'phone')
        extra_kwargs = {'password': {'write_only': True}}

    
    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

class RoomsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rooms
        fields = '__all__'


class RoomParticipantsSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Rooms.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

    class Meta:
        model = RoomParticipants
        fields = '__all__'

class BlockedUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = UserProfile.objects.all())
    blocked_user = serializers.PrimaryKeyRelatedField(queryset = UserProfile.objects.all())
    
    class Meta:
        model = BlockedUser
        fields = '__all__'

class MessagesSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Rooms.objects.all())
    formatted_time = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    is_block = serializers.SerializerMethodField()

    class Meta:
        model = Messages
        fields = fields = ['id', 'sender', 'room', 'content','username', 'avatar', 'formatted_time','status', 'is_block']

    def get_formatted_time(self, obj):
        time = obj.created_at
        time += timedelta(hours=7)
        
        formatted_time = time.strftime("%Y-%m-%d %I:%M %p")  # Ví dụ: 2024-04-12 02:09 AM
        return formatted_time
    
    def get_username(self, obj):
        return obj.sender.username

    def get_avatar(self, obj):
        return str(obj.sender.avatar)
    
    def get_is_block(self, obj):
        sender_id = obj.sender.id
        try:
            user_id = self.context['user_id']
            is_blocked = BlockedUser.objects.filter(user=sender_id, blocked_user=user_id).exists()
            return 1 if is_blocked else 0
        except KeyError:
            return 0
  
    
        


class ReceiversSerializer(serializers.ModelSerializer):
    message = serializers.PrimaryKeyRelatedField(queryset=Messages.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

    class Meta:
        model = Receivers
        fields = '__all__'
