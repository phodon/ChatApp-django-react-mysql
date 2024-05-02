import React, { useContext, useEffect } from 'react';
import { useState } from 'react';
import './style.css';
import { UserContext } from '../context/Usercontext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import ChatHeader from './ChatHeader';
import SearchBar from './SearchBar';
import SearchResults from './SearchResults';
import CreateRoomForm from './CreateRoomForm';
import ChatList from './ChatList'

function Home() {
    const { logout } = useContext(UserContext);
    const navigate = useNavigate();
    const [chatList, setChatList] = useState([]);
    const [selectedChatId, setSelectedChatId] = useState(null);
    const [messageList, setMessageList] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResult] = useState([]);
    const [message, setMessage] = useState('');
    const access_token = jwtDecode(localStorage.getItem('access_token'))
    const user_id = access_token.user_id
    const [roomInfo, setRoomInfo] = useState(null);
    const [showRoomInfo, setShowRoomInfo] = useState(true);
    const [roomName, setRoomName] = useState('');
    const [username, setUsername] = useState('');
    const [avatar, setAvatar] = useState('');

    const toggleRoomInfo = () => {
        setShowRoomInfo(!showRoomInfo);
    };

    const handleBlockUser = (userId, isBlock) => {
        if (isBlock === 0) {
            axios.post(`/api/block/`, { blocked_user: userId }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`
                }
            })
                .then(response => {
                    console.log(response.data.message);
                    fetchResultSearch()
                })
                .catch(error => {
                    console.error('Error adding user:', error);
                });
        } else {
            axios.post(`/api/unblock/`, { unblocked_user: userId }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`
                }
            })
                .then(response => {
                    console.log(response.data.message);
                    fetchResultSearch()
                })
                .catch(error => {
                    console.error('Error adding user:', error);
                });
        }
    };

    useEffect(() => {
        setUsername(localStorage.getItem('username'));
        setAvatar(localStorage.getItem('avatar'));
        console.log(avatar)
    }, []);


    const handleRoomNameChange = (e) => {
        setRoomName(e.target.value);
    }

    const handleCreateRoom = async () => {
        try {
            const response = await axios.post(
                '/api/create_room/',
                { room_name: roomName },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`
                    }
                }
            );
            console.log(response.data);
            setRoomName('');
            fetchChatList();
        } catch (error) {
            console.error('Error creating room:', error);
        }
    };

    const handleAddUser = (userId) => {
        axios.post(`/api/add_member/?member=${userId}&room=${selectedChatId}`, null, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
        })
            .then(response => {
                console.log(response.data.message);
            })
            .catch(error => {
                console.error('Error adding user:', error);
            });
    };

    const handleMessageChange = (e) => {
        setMessage(e.target.value);
    };

    const handleDeleteMember = (memberId) => {
        axios.delete(`/api/remove_member/?member=${memberId}&room=${selectedChatId}`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
        })
            .then(response => {
                console.log('Response:', response.data);
                setShowRoomInfo(true);
            })
            .catch(error => {
                console.error('Error deleting member:', error);
            });
    };

    const handleShowRoomInfo = async (room_id) => {
        fetchRoomInfo(room_id);
        toggleRoomInfo();
    };

    const handleSendMessage = async () => {
        if (!message.trim()) return;

        try {
            const response = await axios.post(
                '/api/chat/',
                {
                    room_id: selectedChatId,
                    content: message
                },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`
                    }
                }
            );
            fetchMessages(selectedChatId);
            console.log('sao vay nhi');
        } catch (error) {
            console.error('Error sending message:', error.response.data);
        }
        setMessage('');
    };

    const handleMessageKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    };

    const fetchResultSearch = async () =>{
        try {
            const response = await axios.get(`/api/search_user/?search=${searchQuery}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            setSearchResult(response.data);
        } catch (error) {
            console.error('Error searching user:', error);
        }
    }

    const handleSearch = async () => {
        fetchResultSearch()
    };

    const handleChangeSearch = (e) => {
        setSearchQuery(e.target.value);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };

    const handleClick = () => {
        handleSearch();
    };

    const fetchChatList = async () => {
        try {
            const response = await axios.get('/api/list_chat/', {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            setChatList(response.data);
        } catch (error) {
            console.error('Error fetching chat list:', error);
            if (error.response && error.response.status === 401) {
                logout();
                navigate("/");
            }
        }
    };

    useEffect(() => {
        fetchChatList();
    }, [logout, navigate]);

    const fetchMessages = async (roomId) => {
        try {
            const response = await axios.get(`/api/message/${roomId}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            setMessageList(response.data);
        } catch (error) {
            console.error('Error fetching messages:', error);
        }
    };

    const fetchRoomInfo = async (room_id) => {
        try {
            const response = await axios.get(`/api/get_room_detail/${room_id}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            setRoomInfo(response.data);
        } catch (error) {
            console.error('Error fetching room info:', error);
        }
    };

    const handleLogout = () => {
        logout()
        navigate("/");
    }

    const handleChooseRoom = (roomId) => {
        fetchRoomInfo(roomId);
        setSelectedChatId(roomId);
        fetchMessages(roomId);
    };

    return (
        <div className="container">
            <div className="row clearfix">
                <div className="col-lg-12">
                    <div className="card chat-app">
                        <div id="plist" className="people-list">
                            <SearchBar searchQuery={searchQuery} handleChangeSearch={handleChangeSearch} handleClick={handleClick} handleKeyPress={handleKeyPress} />
                            <ChatList chatList={chatList} handleChooseRoom={handleChooseRoom} />
                            <CreateRoomForm roomName={roomName} handleRoomNameChange={handleRoomNameChange} handleCreateRoom={handleCreateRoom} />
                            <SearchResults searchResults={searchResults} handleAddUser={handleAddUser} handleBlockUser={handleBlockUser} />
                        </div>

                        <div className="chat">
                            <ChatHeader
                                avatar={avatar}
                                username={username}
                                handleShowRoomInfo={handleShowRoomInfo}
                                handleLogout={handleLogout}
                                showRoomInfo={showRoomInfo}
                                roomInfo={roomInfo}
                                handleDeleteMember={handleDeleteMember}
                                selectedChatId={selectedChatId}
                            />
                            <MessageList messageList={messageList} user_id={user_id} username={username} avatar={avatar} />
                            <MessageInput
                                message={message}
                                handleMessageChange={handleMessageChange}
                                handleMessageKeyPress={handleMessageKeyPress}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Home;
