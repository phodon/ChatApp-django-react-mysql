from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserProfileSerializer, MessagesSerializer, RoomsSerializer, RoomParticipantsSerializer, ReceiversSerializer
from .models import UserProfile, Messages, RoomParticipants, Receivers, Rooms
from rest_framework_simplejwt.tokens import RefreshToken
from app.middlewares import UserMiddleware
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

# Create your views here.
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    confirm_password = request.data.get('confirm_password')

    if not username or not password or not confirm_password:
        return Response({'error':'Username, Email, Password, Confirm_password is required'}, status=status.HTTP_400_BAD_REQUEST)
    if confirm_password != password:
        return Response({'error':'Password not like Confirm_password'}, status=status.HTTP_400_BAD_REQUEST)
    if 'avatar' not in request.data: 
        return Response({'error':'Avatar is required'}, status=status.HTTP_400_BAD_REQUEST)

    if UserProfile.objects.filter(email=email).exists():
        return Response({'error':'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

    if UserProfile.objects.filter(username=username).exists():
        return Response({'error':'Username already registered'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserProfileSerializer(data=request.data)  # Truyền request.data vào Serializer

    if serializer.is_valid():
        serializer.save()
        return Response({'message':'Register is success', 'data':serializer.data}, status=status.HTTP_201_CREATED)

    return Response({'message':'Information is invalid', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
        'avatar': user.avatar.url if user.avatar else None  # Lấy đường dẫn ảnh đại diện nếu có
    }
    print(user_data)

    return Response({'refresh_token': refresh,'access_token': access, 'user_data': user_data})

@csrf_exempt
@UserMiddleware
@api_view(['POST'])
def chat(request):

    room_id = request.data.get('room_id')
    try:
        room = Rooms.objects.get(id=room_id)
    except Rooms.DoesNotExist:
        return Response({'error':'Room not found'}, status = status.HTTP_401_UNAUTHORIZED)
    
    try: 
        user = UserProfile.objects.get(id = request.user_id)
    except UserProfile.DoesNotExist:
        return Response({'error':'User not found'}, status = status.HTTP_401_UNAUTHORIZED)

    request.data['sender'] = user.id
    request.data['room'] = room.id
    request.data['status'] = 1
    mess_serializer = MessagesSerializer(data=request.data)

    if mess_serializer.is_valid():
        list_id_receiver = list(RoomParticipants.objects.filter(room_id = room.id).values_list('user_id', flat=True))

        if len(list_id_receiver)==1:
            return Response({'error': 'phong chua co ai'}, status=status.HTTP_401_UNAUTHORIZED)
        message = mess_serializer.save()
        
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
    
@csrf_exempt
@UserMiddleware
@api_view(['GET'])
def getListChat(request):
    try: 
        user = UserProfile.objects.get(id=request.user_id)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Lấy danh sách các phòng mà người dùng đã tham gia
    user_rooms = RoomParticipants.objects.filter(user=user.id)
    print(user_rooms)
    
    # Chuyển đổi danh sách các phòng thành một danh sách dictionary
    rooms_data = []
    for room in user_rooms:
        try:
            room_obj = Rooms.objects.get(id=room.room_id)
            serializer = RoomsSerializer(room_obj)
            rooms_data.append(serializer.data)
        except Rooms.DoesNotExist:
            pass
    
    return Response(rooms_data)

@csrf_exempt
@UserMiddleware
@api_view(['GET'])
def searchUser(request):
    search_query = request.query_params.get('search', '')
    if search_query == '':
        return Response({"message":'khong co j'})
    users = UserProfile.objects.filter(Q(username__icontains=search_query) | Q(email__icontains=search_query))
    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)

@csrf_exempt
@UserMiddleware
@api_view(['GET'])
def getMessage(request,id):
    list_message = Messages.objects.filter(room_id = id).order_by('created_at')
    serializer = MessagesSerializer(list_message,many = True)
    return Response(serializer.data)

@csrf_exempt
@UserMiddleware
@api_view(['GET'])
def getRoomInfo(request, id):
    try:
        room = Rooms.objects.get(id=id)
        serializer = RoomsSerializer(room, many=False)
        list_id_member = list(RoomParticipants.objects.filter(room_id=room.id).values_list('user_id', flat=True))
        list_member = [] 
        for user_id in list_id_member:
            try:
                tmp = UserProfile.objects.get(id=user_id)
                user_data = {
                    'id': tmp.id,
                    'email': tmp.email,
                    'username': tmp.username
                }
                list_member.append(user_data)
            except UserProfile.DoesNotExist:
                pass
        data = serializer.data
        data['list_member'] = list_member
        return Response(data)
    except Rooms.DoesNotExist:
        return Response("id phong k ton tai")
    
@csrf_exempt
@UserMiddleware
@api_view(['DELETE'])
def removeMember(request):
    try:
        member_id = int(request.query_params.get('member', ''))
        room_id = int(request.query_params.get('room', ''))
        
        room = Rooms.objects.get(id=room_id)
        if room.admin_id != request.user_id:
            return Response({'message': 'Bạn không phải là admin'})
        
        list_member = RoomParticipants.objects.filter(room_id=room.id).values_list('user_id', flat=True)
        if member_id not in list_member or member_id == request.user_id:
            return Response({'message': 'Không có trong nhóm hoặc bạn là admin'})

        RoomParticipants.objects.filter(room_id=room_id, user_id=member_id).delete()
        return Response({'message': 'Xóa thành công'})
    
    except (ValueError, Rooms.DoesNotExist):
        return Response({'message': 'ID phòng không hợp lệ hoặc không tồn tại'}, status=400)
    
    except Exception as e:
        return Response({'message': f'Lỗi: {str(e)}'}, status=400)
    
@csrf_exempt
@UserMiddleware
@api_view(['POST'])
def addMember(request):
    print("ok")
    try:
        member_id = int(request.query_params.get('member', ''))
        room_id = int(request.query_params.get('room', ''))
        
        room = Rooms.objects.get(id=room_id)
        member = UserProfile.objects.get(id=member_id)
        
        list_member = RoomParticipants.objects.filter(room_id=room.id).values_list('user_id', flat=True)
        if member_id in list_member or request.user_id not in list_member:
            return Response({'message': 'bạn không ở trong nhóm này hoặc người bạn thêm đã có trong nhóm'})

        # Tạo một serializer với dữ liệu đầu vào
        serializer = RoomParticipantsSerializer(data={'room': room.id, 'user': member.id})
        if serializer.is_valid():
            serializer.save()
            print("ok123")
            return Response({'message': 'Thêm thành công'})
            
        else:
            return Response(serializer.errors, status=400)

    except (ValueError, Rooms.DoesNotExist, UserProfile.DoesNotExist):
        return Response({'message': 'ID phòng không hợp lệ hoặc không tồn tại'}, status=400)
    
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
    print(list_room_names)

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

        return Response(room_serializer.data)
    else:
        return Response({'error': 'Error'}, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@UserMiddleware
@api_view(['GET'])
def userInfo(request):
    try:
        user = UserProfile.objects.get(id=request.user_id)
        serializer = UserProfileSerializer(user)
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
        if address:
            user.address = address
        if phone:
            user.phone = phone
        if avatar!=None:
            user.avatar = avatar
        user.save()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
   
