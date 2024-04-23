import React from 'react';

function CreateRoomForm({ roomName, handleRoomNameChange, handleCreateRoom }) {
  return (
    <div>
      <div className="input-group mb-3">
        <input type="text" className="form-control" placeholder="Enter room name" value={roomName} onChange={handleRoomNameChange} />
      </div>
      <div className="text-center">
        <button className="btn btn-outline-primary mt-3" onClick={handleCreateRoom}>Create New Room</button>
      </div>
    </div>
  );
}

export default CreateRoomForm;