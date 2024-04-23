import React from 'react';
import { FaSearch } from 'react-icons/fa';

function SearchBar({ searchQuery, handleChangeSearch, handleClick, handleKeyPress}) {
  return (
    <div className="input-group">
      <div className="input-group-prepend">
        <span className="input-group-text" onClick={handleClick}><FaSearch /></span>
      </div>
      <input
        type="text"
        className="form-control"
        placeholder="Search..."
        value={searchQuery}
        onChange={handleChangeSearch}
        onKeyPress={handleKeyPress}
      />
    </div>
  );
}

export default SearchBar;