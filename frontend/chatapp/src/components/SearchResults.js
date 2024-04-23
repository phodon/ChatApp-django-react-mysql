import React from 'react';

function SearchResults({ searchResults, handleAddUser }) {
  return (
    <div className="search-results-container">
      <ul className="list-group search-results">
        {searchResults.length > 0 && searchResults.map(user => (
          <li key={user.id} className="list-group-item d-flex justify-content-between align-items-center">
            <div className="w-75">
              <div className="text-muted email-phone"><strong>Email:</strong> {user.email}</div>
              <div className="text-muted email-phone"><strong>Phone:</strong> {user.phone}</div>
            </div>
            <button onClick={() => handleAddUser(user.id)} className="btn btn-primary btn-sm">Add</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SearchResults;