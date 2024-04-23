import React from 'react';
import { FaCircle } from 'react-icons/fa';

function ChatList({ chatList, handleChooseRoom }) {
  return (
    <div className="search-results-container">
      <ul className="list-unstyled chat-list mt-2 mb-0">
        {chatList.map(chat => (
          <li className="clearfix" key={chat.id} onClick={() => handleChooseRoom(chat.id)}>
            <img src="https://bootdey.com/img/Content/avatar/avatar1.png" alt="avatar" className="avatar-img-2"/>
            <div className="about">
              <div className="name">{chat.room_name}</div>
              <div className="status">
                <FaCircle className={chat.status === 1 ? 'online' : 'offline'} /> {chat.status === 1 ? 'online' : `offline since ${chat.created_at}`}
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ChatList;