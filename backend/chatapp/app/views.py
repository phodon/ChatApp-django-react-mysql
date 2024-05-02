from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserProfileSerializer, MessagesSerializer, RoomsSerializer, RoomParticipantsSerializer, ReceiversSerializer, BlockedUserSerializer
from .models import UserProfile, Messages, RoomParticipants, Receivers, Rooms, BlockedUser
from rest_framework_simplejwt.tokens import RefreshToken
from app.middlewares import UserMiddleware
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

import logging

logger = logging.getLogger(__name__)

# Create your views here.
@api_view(['POST'])
def register(request):
    data = request.data

    required_fields = ['username', 'password', 'confirm_password', 'email', 'avatar']
    for field in required_fields:
        if field not in data or not data[field]:
            return Response({'error': f'{field.capitalize()} is required'}, status=status.HTTP_400_BAD_REQUEST)

    if data['confirm_password'] != data['password']:
        return Response({'error': 'Password does not match Confirm_password'}, status=status.HTTP_400_BAD_REQUEST)

    if UserProfile.objects.filter(email=data['email']).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

    if UserProfile.objects.filter(username=data['username']).exists():
        return Response({'error': 'Username already registered'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserProfileSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        logger.info('Register Successfully')
        return Response({'message': 'Register is success', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    return Response({'message': 'Information is invalid', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def loginUser(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token) 
    refresh = str(refresh) 

    user_data = {
        'username': user.username,
        'avatar': user.avatar.url if user.avatar else None  
    }
    logger.info('Login Successfully')

    return Response({'refresh_token': refresh,'access_token': access, 'user_data': user_data})

@csrf_exempt
@UserMiddleware
@api_view(['POST'])
def chat(request):

    room_id = request.data.get('room_id')
    try:
        room = Rooms.objects.get(id=room_id)
    except Rooms.DoesNotExist:
        return Response({'error':'Room not found'}, status = status.HTTP_404_NOT_FOUND)
    
    try: 
        user = UserProfile.objects.get(id = request.user_id)
    except UserProfile.DoesNotExist:
        return Response({'error':'User not found'}, status = status.HTTP_404_NOT_FOUND)
    
    request.data['sender'] = user.id
    request.data['room'] = room.id
    request.data['status'] = 1
    mess_serializer = MessagesSerializer(data=request.data)

    if mess_serializer.is_valid():
        list_id_receiver = list(RoomParticipants.objects.filter(room_id = room.id).values_list('user_id', flat=True))

        if len(list_id_receiver)==1:
            return Response({'error': 'phong chua co ai'}, status=status.HTTP_404_NOT_FOUND)
        message = mess_serializer.save()
        logger.debug('Sent Message Successfully')
        
        for i in list_id_receiver:
            if i != user.id:
                data = {
                    "message": message.id,
                    "receiver": i
                }
                receiver_serializer = ReceiversSerializer(data=data)
                if receiver_serializer.is_valid():
                    receiver_serializer.save()
        return Response(mess_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(mess_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@UserMiddleware
@api_view(['GET'])
def getListChat(request):
    try: 
        user = UserProfile.objects.get(id=request.user_id)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    user_rooms = RoomParticipants.objects.filter(user=user.id)
    
    rooms_data = []
    for room in user_rooms:
        try:
            room_obj = Rooms.objects.get(id=room.room_id)
            serializer = RoomsSerializer(room_obj)
            rooms_data.append(serializer.data)
        except Rooms.DoesNotExist:
            pass
    logger.debug('API getListChat')
    return Response(rooms_data)


@UserMiddleware
@api_view(['GET'])
def searchUser(request):
    try:
        user = UserProfile.objects.get(id=request.user_id)

        blocked_users = BlockedUser.objects.filter(user=user.id).values_list('blocked_user', flat=True)

        search_query = request.query_params.get('search', '')

        if not search_query:
            return Response({"message": 'No search data available'})
        
        users = UserProfile.objects.filter(Q(username__icontains=search_query) | Q(email__icontains=search_query))

        data = []

        for user in users:
            tmp = {
                'id': user.id,
                'email': user.email,
                'phone': user.phone,
                'isBlock': 1 if user.id in blocked_users else 0
            }
            data.append(tmp)

        logger.info('API searchUser')

        return Response(data)

    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@UserMiddleware
@api_view(['GET'])
def getMessage(request,id):
    list_message = Messages.objects.filter(room_id = id).order_by('created_at')
    serializers = MessagesSerializer(list_message, context={'user_id': request.user_id}, many = True )
    logger.info('API getMessage')
    return Response(serializers.data)


@UserMiddleware
@api_view(['GET'])
def getRoomInfo(request, id):
    if id == 'null':
        return Response("ID is null", status=status.HTTP_400_BAD_REQUEST)
    
    try:
        room = Rooms.objects.get(id=id)
    except Rooms.DoesNotExist:
        return Response("Room ID does not exist", status=status.HTTP_404_NOT_FOUND)
    
    serializer = RoomsSerializer(room)
    list_member = []
    room_participants = RoomParticipants.objects.filter(room_id=room.id).values_list('user_id', flat=True)
    users = UserProfile.objects.filter(id__in=room_participants)

    for user in users:
        user_data = {
            'id': user.id,
            'email': user.email,
            'username': user.username
        }
        list_member.append(user_data)

    data = serializer.data
    data['list_member'] = list_member
    logger.info('API getRoomInfo')
    return Response(data)
    
@csrf_exempt
@UserMiddleware
@api_view(['DELETE'])
def removeMember(request):
    try:
        member_id = int(request.query_params.get('member', ''))
        room_id = int(request.query_params.get('room', ''))
        
        room = Rooms.objects.get(id=room_id)
        if room.admin_id != request.user_id:
            logger.info('API removeMember, You is not Admin')
            return Response({'message': 'You is not admin'})
        
        list_member = RoomParticipants.objects.filter(room_id=room.id).values_list('user_id', flat=True)
        if member_id not in list_member or member_id == request.user_id:
            return Response({'message': 'Not in the group or you are an admin'})

        RoomParticipants.objects.filter(room_id=room_id, user_id=member_id).delete()
        logger.info('API removeMemBer')
        return Response({'message': 'Delete sucessfully'})
    
    except (ValueError, Rooms.DoesNotExist):
        return Response({'message': 'Room is not found'}, status=400)
    
    except Exception as e:
        return Response({'message': f'Error: {str(e)}'}, status=400)
    
@csrf_exempt
@UserMiddleware
@api_view(['POST'])
def addMember(request):
    try:
        member_id = int(request.query_params.get('member', ''))
        room_id = int(request.query_params.get('room', ''))
        
        room = Rooms.objects.get(id=room_id)
        member = UserProfile.objects.get(id=member_id)
        
        list_member = RoomParticipants.objects.filter(room_id=room.id).values_list('user_id', flat=True)
        if member_id in list_member or request.user_id not in list_member:
            return Response({'message': 'You are not in this group or the person you added is already in the group'})

        serializer = RoomParticipantsSerializer(data={'room': room.id, 'user': member.id})
        if serializer.is_valid():
            serializer.save()
            logger.info('API addMember')
            return Response({'message': 'Add successfully'})
            
        else:
            return Response(serializer.errors, status=400)

    except (ValueError, Rooms.DoesNotExist, UserProfile.DoesNotExist):
        return Response({'message': 'Room not found'}, status=400)
    
    except Exception as e:
        return Response({'message': f'Lỗi: {str(e)}'}, status=400)


@csrf_exempt
@UserMiddleware
@api_view(['POST'])
def createRoom(request):
    try:
        user = UserProfile.objects.get(id=request.user_id)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)

    room_name = request.data.get('room_name')  
    if not room_name:
        return Response({'error': 'Roomname is required'}, status=status.HTTP_401_UNAUTHORIZED)

    list_room = RoomParticipants.objects.filter(user=user.id)
    list_room_names = Rooms.objects.filter(id__in=list_room.values('room_id')).values_list('room_name', flat=True)

    if room_name in list_room_names:
        return Response({'error': 'Roomname already exists'}, status=status.HTTP_401_UNAUTHORIZED)

    data = {
        "room_name": room_name,
        "admin": user.id
    }
    room_serializer = RoomsSerializer(data=data)
    if room_serializer.is_valid():
        tmp = room_serializer.save()
        data2 = {
            "room": tmp.id,
            "user": user.id
        }
        roomparticipants_serializer = RoomParticipantsSerializer(data=data2)
        if roomparticipants_serializer.is_valid():
            roomparticipants_serializer.save()

        logger.info('API createRoom')
        return Response(room_serializer.data)
    else:
        return Response({'error': 'Error'}, status=status.HTTP_401_UNAUTHORIZED)



@UserMiddleware
@api_view(['GET'])
def userInfo(request):
    try:
        user = UserProfile.objects.get(id=request.user_id)
        serializer = UserProfileSerializer(user)
        logger.info('API userInfo')
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
@UserMiddleware
@api_view(['POST'])
def userUpdate(request):
    try:
        user = UserProfile.objects.get(id=request.user_id)
        address = request.data.get('address')
        phone = request.data.get('phone')
        avatar = request.data.get('avatar')
        logger.info(avatar)
        if address:
            user.address = address
        if phone:
            user.phone = phone
        if avatar!=None:
            user.avatar = avatar
        user.save()
        serializer = UserProfileSerializer(user)
        logger.info('API userUpdate')
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
@csrf_exempt
@UserMiddleware
@api_view(['POST'])
def block(request):
    try:
        user = UserProfile.objects.get(id = request.user_id)
        blocked_user = UserProfile.objects.get(id = request.data.get('blocked_user'))

        if user.id != blocked_user.id:
            data = {
                'user': user.id,
                'blocked_user': blocked_user.id
            }
            check = BlockedUser.objects.filter(user = user.id, blocked_user = blocked_user.id)
            if check:
                return Response({'message':'blocked before'}, status=status.HTTP_200_OK)
            else:
                serializer = BlockedUserSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    logger.info('API block')
                    return Response({'message':'block successful'})
                else:
                    return Response({'error':'block fail'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':'can not block yourself'}, status=status.HTTP_400_BAD_REQUEST)

    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@UserMiddleware
@api_view(['POST'])
def unblock(request):
    try:
        user = UserProfile.objects.get(id = request.user_id)
        unblocked_user = UserProfile.objects.get(id = request.data.get('unblocked_user'))

        check = BlockedUser.objects.filter(user = user.id, blocked_user = unblocked_user.id)
        if check:
            check.delete()
            logger.info('API unblock')
            return Response({'message':'unblock sucess'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'have not block before'}, status=status.HTTP_400_BAD_REQUEST)
        
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

    
    
   
