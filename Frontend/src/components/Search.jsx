import React from "react";  

/*
    Title: SearchBar Component

    Purpose:
    The purpose of this component is to provide a search bar for users to filter blog posts.
    It takes a query string and a function to update the query as props.
*/

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