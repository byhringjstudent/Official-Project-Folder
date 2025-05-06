import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

/* 
    Title: BlogList Component

    Purpose:
    The purpose of this component is to display a list of blog posts with 
    functionality to search, edit, and delete individual posts. It allows users 
    to filter the displayed blogs based on a search query and provides buttons 
    for editing and deleting each blog post.
    The component is designed to be reusable and can be integrated into
    different parts of the application where a list of blogs is needed.

*/

const BlogList = ({ blogs, deleteBlog, query, setQuery }) => {
  const [filteredBlogs, setFilteredBlogs] = useState(blogs);
  const navigate = useNavigate();

  useEffect(() => {
    // Filter blogs based on the search query
    if (query) {
      const filtered = blogs.filter(blog =>
        blog.title.toLowerCase().includes(query.toLowerCase()) ||
        blog.shortdescription.toLowerCase().includes(query.toLowerCase()) ||
        (blog.tags && blog.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))) ||
        blog.status.toLowerCase().includes(query.toLowerCase()) // Check tags if present
      );
      setFilteredBlogs(filtered);
    } else {
      setFilteredBlogs(blogs);
    }
  }, [blogs, query]); // Re-run the effect when blogs or query changes

  return (
    <div className="blog-list-container">
      <div className="search-bar-container">
        <input
          type="text"
          placeholder="Search Blogs"
          className="blog-search-bar"
          value={query}
          onChange={(e) => setQuery(e.target.value)} // Update query on user input
        />
      </div>

      {filteredBlogs.length === 0 ? (
        <p>No matching blog posts found.</p>
      ) : (
        <ul className="blog-list">
          {filteredBlogs.map((blog) => (
            <li key={blog.blogID} className="user-blog-preview">
              <h4>{blog.title}</h4>
              <p className={`blog-status ${blog.status === 'published' ? 'published' : 'draft'}`}>
                {blog.status === 'published' ? 'Published' : 'Draft'}
              </p>
              <p>{blog.shortdescription}</p>
              <small>
                  {blog.tags.map((tag, index) => (
                    <span key={index} className="tag-badge">
                      {tag}
                    </span>
                  ))}
                </small>
                <p> </p>
              <small>{new Date(blog.date).toLocaleDateString()}</small>
              <p></p>
              <a href={`/blog/${blog.blogID}`}>Read more →</a>
              <div className="button-group">
                <button onClick={() => navigate(`/edit-post/${blog.blogID}`)} className=" button edit-button">
                  Edit
                </button>
                <button onClick={() => deleteBlog(blog.blogID)} className="button delete-button">
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default BlogList;
