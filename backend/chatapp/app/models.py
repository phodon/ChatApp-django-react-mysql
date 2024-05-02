from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, username, password, **extra_fields)



class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    status = models.IntegerField(default=0)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
    
class BlockedUser(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='block_user_user_1')
    blocked_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='block_user_user_2')

class Rooms(models.Model):
    isGroupChat = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=255, blank=True)
    status = models.IntegerField(default=1)
    admin = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

class RoomParticipants(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class Messages(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField()

class Receivers(models.Model):
    message = models.ForeignKey(Messages, on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

