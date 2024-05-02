import React from 'react';

function SearchResults({ searchResults, handleAddUser, handleBlockUser }) {
  return (
    <div className="search-results-container">
      <ul className="list-group search-results">
        {searchResults.length > 0 && searchResults.map(user => (
          <li key={user.id} className="list-group-item d-flex justify-content-between align-items-center">
            <div className="w-75">
              <div className="text-muted email-phone"><strong>Email:</strong> {user.email}</div>
              <div className="text-muted email-phone"><strong>Phone:</strong> {user.phone}</div>
            </div>
            <div>
              <button onClick={() => handleAddUser(user.id)} className="btn btn-primary btn-sm">Add</button>
              <p></p>
              <button onClick={() => handleBlockUser(user.id,user.isBlock)} className="btn btn-primary btn-sm"> {user.isBlock === 1 ? 'Unblock' : 'Block'}</button>
            </div>

          </li>
        ))}
      </ul>
    </div>
  );
}

export default SearchResults;