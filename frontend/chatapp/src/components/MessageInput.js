import React from 'react';

import { FaPaperPlane } from 'react-icons/fa';

function MessageInput({ message, handleMessageChange, handleSendMessage, handleMessageKeyPress }) {
  return (
    <div className="chat-message clearfix">
      <div className="input-group mb-0">
        <div className="input-group-prepend">
          <span className="input-group-text" onClick={handleSendMessage}>
            <FaPaperPlane />
          </span>
        </div>
        <input
          type="text"
          className="form-control"
          placeholder="Enter text here..."
          value={message}
          onChange={handleMessageChange}
          onKeyPress={handleMessageKeyPress}
        />
      </div>
    </div>
  );
}

export default MessageInput;