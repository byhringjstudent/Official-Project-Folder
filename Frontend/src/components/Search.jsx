import React from "react";  

const SearchBar = ({ query, setQuery }) => {
    return (
      <input
        type="text"
        placeholder="Search blogs..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="search-bar"
      />
    );
  };
  
  export default SearchBar;