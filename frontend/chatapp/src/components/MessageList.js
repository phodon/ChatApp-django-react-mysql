import React from 'react';
import { ListGroup } from 'react-bootstrap';

function MessageList({ messageList, user_id, username, avatar }) {
  return (
    <div className="chat-history">
      <ListGroup style={{ maxHeight: '500px', overflowY: 'auto' }}>
        {messageList.map(message => (
          <ListGroup.Item key={message.id} className={`clearfix ${message.sender === user_id ? 'own-message' : 'other-message'}`}>
            <div className="message-data">
              {message.sender !== user_id && (
                <React.Fragment>
                  <div className="avatar-and-username">
                    <img src={message.avatar ? `http://127.0.0.1:8000/media/${message.avatar}` : 'https://bootdey.com/img/Content/avatar/avatar2.png'} alt="avatar" className="avatar-img-2" />
                    <span>{message.username}</span>
                    <span className="message-data-time">{message.formatted_time}</span>
                  </div>
                </React.Fragment>
              )}
              {message.sender === user_id && (
                <React.Fragment>
                  <img src={avatar ? `http://127.0.0.1:8000${avatar}` : 'https://bootdey.com/img/Content/avatar/avatar2.png'} alt="avatar" className="avatar-img-2" />
                  <span >{username}</span>
                  <span className="message-data-time">{message.formatted_time}</span>
                </React.Fragment>
              )}
              {message.is_block === 1 && (
                <div className="blocked-message">Bạn không thể xem tin nhắn này</div>
              )}
            </div>
            {message.is_block !== 1 && (
              <div className={`message ${message.sender === user_id ? 'text-own-message' : 'other-message'}`}>
                {message.content}
              </div>
            )}
          </ListGroup.Item>
        ))}
      </ListGroup>
    </div>
  );
}

export default MessageList;
