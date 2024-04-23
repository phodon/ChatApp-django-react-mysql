import React from 'react';
import { FaCogs, FaCircle } from 'react-icons/fa';
import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'

function ChatHeader({ avatar, username, handleShowRoomInfo, handleLogout, showRoomInfo, roomInfo, handleDeleteMember, selectedChatId }) {

  const navigate = useNavigate();

  const handleShowInfo = async () => {
    navigate('/user_info');
  };

  return (
    <div className="chat-header clearfix">
      <div className="row">
        <div className="col-lg-6">
          <img src={avatar ? `http://127.0.0.1:8000${avatar}` : 'https://bootdey.com/img/Content/avatar/avatar2.png'} alt="avatar" className="avatar-img-2" onClick={handleShowInfo}/>
          <div className="chat-about">
            <h6 className="m-b-0">{username}</h6>
          </div>
        </div>
        <div className="col-lg-6 hidden-sm text-right">
          <button className="btn btn-outline-info" onClick={() => handleShowRoomInfo(selectedChatId)}><FaCogs /></button>
          <a>             </a>
          <button className="btn btn-outline-warning" onClick={handleLogout}><FaCircle />Logout</button>
          {showRoomInfo || roomInfo && (
            <div>
              <div className="room-info-container">
                <h2>Room Name: {roomInfo.room_name}</h2>
                <p>Members:</p>
                <ul>
                  <ul className="list-unstyled">
                    {roomInfo.list_member.map(member => (
                      <li key={member.id} className="d-flex justify-content-between align-items-center">
                        <div>
                          {member.username} - {member.email}
                        </div>
                        <div>
                          <button onClick={() => handleDeleteMember(member.id)} className="btn btn-danger btn-sm mr-2">Delete</button>
                        </div>
                      </li>
                    ))}
                  </ul>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ChatHeader;