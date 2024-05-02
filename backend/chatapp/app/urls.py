from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login_user/', views.loginUser, name='login_user'),
    path('chat/', views.chat, name = 'chat'),
    path('list_chat/', views.getListChat, name = 'getListChat'),
    path('search_user/', views.searchUser, name = 'searchUser'),
    path('message/<str:id>', views.getMessage, name = 'getMessage'),
    path('get_room_detail/<str:id>',views.getRoomInfo, name = 'getRoomInfo'),
    path('remove_member/', views.removeMember, name='removeMember'),
    path('add_member/', views.addMember, name='addMember'),
    path('create_room/', views.createRoom, name = 'createRoom'),
    path('user_info/', views.userInfo, name='userInfo'),
    path('user_update/', views.userUpdate, name='userUpdate'),
    path('block/',views.block, name = 'block'),
    path('unblock/',views.unblock, name = 'unblock')
]