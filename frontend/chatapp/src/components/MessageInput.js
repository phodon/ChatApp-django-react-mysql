import React, { useState } from 'react';
import { FaSmile } from 'react-icons/fa';
import Picker from "emoji-picker-react";

function MessageInput({ message, handleMessageChange, handleMessageKeyPress }) {
  const [chosenEmoji, setChosenEmoji] = useState(null);
  const [isPickerOpen, setIsPickerOpen] = useState(false);

  const handleOpenEmoji = (event, emojiObject) => {
    setChosenEmoji(emojiObject);
  };

  const togglePicker = () => {
    setIsPickerOpen(!isPickerOpen);
  };

  return (
    <div className="chat-message clearfix">
      <div className="input-group mb-0">
        <div>
          <FaSmile onClick={togglePicker} />
          {isPickerOpen && (
            <div style={{ position: 'absolute', top: '-450px' }}>
              <Picker onEmojiClick={handleOpenEmoji} />
            </div>
          )}
        </div>
        <a style={{ width: '10px'}}></a>
        <textarea
          style={{ height: '40px', width: 'calc(100% - 90px)', resize: 'none' }}
          maxLength={100000}
          type="text"
          className="form-control"
          placeholder="Enter text here..."
          value={message}
          onChange={(e) => handleMessageChange(e, chosenEmoji)}
          onKeyPress={handleMessageKeyPress}
        />
      </div>
    </div>
  );
}

export default MessageInput;
