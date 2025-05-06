import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './EditPost.css'; 

/*
    Title: EditPost Component
    Purpose:
    The purpose of this component is to allow users to edit an existing blog post.
    It fetches the post data from the backend using the post ID from the URL,
    and allows users to update the title, content, short description, tags, and image.
    The component also provides functionality to save the post as a draft or publish it.
*/

function EditPost() {
  const { id } = useParams();
  const [post, setPost] = useState(null);  // Post data state
  const [error, setError] = useState(null);  // Error state
  const navigate = useNavigate();

  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [currentStatus, setCurrentStatus] = useState('draft');
  const [shortDesc, setShortDesc] = useState('');
  const [tagInput, setTagInput] = useState('');
  const [tags, setTags] = useState([]);
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  useEffect(() => {
    // Fetch the post data from the backend
    const fetchPost = async () => {
      try {
        const response = await fetch(`/api/blog/get-single-post/${id}`, {
          method: 'GET',
          credentials: 'include',  // Ensure cookies are sent with the request
        });
        if (!response.ok) {
          const data = await response.json();
          setError(data.message || 'Error retrieving post');
        } else {
          const data = await response.json();
          setPost(data.post[0]); // Assuming the response is in the format { post: [{...}] }
        }
      } catch (err) {
        setError('Error fetching data');
      }
    };

    fetchPost();
  }, [id]);  // Refetch the data when the post ID changes

  // Set the initial state of the form fields when the post data is fetched
  useEffect(() => {
    if (post) {
      setTitle(post.title);  // Set the title state
      setContent(post.content);  // Set the content state
      setShortDesc(post.shortdescription);  // Set short description state
      setTags(post.tags || []);  // Set tags state
      setCurrentStatus(post.status);  // Set the status state
    }
  }, [post]);

  // Function to handle the addition of tags
  // This function is triggered when the user presses the Enter key in the tag input field
  const handleAddTag = (e) => {
    if (e.key === 'Enter' && tagInput.trim() !== '') {
      setTags([...tags, tagInput.trim()]);
      setTagInput('');  // Clear the input field after adding the tag
    }
  };

  // Function to handle the change in the image input field
  // This function is triggered when the user selects an image file
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);  // Store the image file
      setImagePreview(URL.createObjectURL(file));  // Create a preview of the image
    }
  };

  // Function to handle the removal of a tag
  // This function is triggered when the user clicks the remove button on a tag
  const handleRemoveTag = (tagToRemove) => {
    const updatedTags = tags.filter(tag => tag !== tagToRemove);
    setTags(updatedTags);
  };
  

  // Function to handle saving the post
  // This function is triggered when the user clicks the Publish or Save as Draft button
  const handleSave = (status) => {
    const formData = new FormData();
    formData.append('title', title);
    formData.append('content', content);
    formData.append('status', status);
    formData.append('shortdescription', shortDesc);
    formData.append('tags', JSON.stringify(tags));  // Convert tags to JSON string
    if (image) {
      formData.append('image', image);  // Append the image file if available
    }

    // Send the form data to the backend to update the post
    // The backend should handle the PUT request to update the post
    fetch(`/blog/updateposts/${id}`, {
      method: 'PUT',
      body: formData,
      credentials: 'include',
    })
      .then(res => {
        if (!res.ok) {
          throw new Error('Failed to update post.');
        }
        return res.json();
      })
      .then(data => {
        console.log(data.message);
        navigate('/account-portal');  // Redirect after saving
      })
      .catch(err => console.error(err));
  };

  if (error) return <div>{error}</div>;  // Show error if there's any
  if (!post) return <div>Loading...</div>;  // Show loading state while data is being fetched

  return (
    // Render the form for editing the blog post
    // The form includes fields for title, content, short description, tags, and image upload
    <div>
      <h3 className="edit-post-header">Edit Blog Post</h3>
      <div className="blog-form-section">
      <small className="blog-labels">Blog Title</small>
      <input
        type="text"
        placeholder="Blog Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <small className="blog-labels">Short Description</small>
      <textarea
        placeholder="Short Description about your post"
        value={shortDesc}
        onChange={(e) => setShortDesc(e.target.value)}
        maxLength={150}
      />
      <small className="blog-labels">Blog Content</small>
      <textarea
        type="text"
        placeholder="Content of your post"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />
      <small className="blog-labels">Tags That Relate to Blog</small>
      <input
        type="text"
        placeholder="Enter topic and press Enter"
        value={tagInput}
        onChange={(e) => setTagInput(e.target.value)}
        onKeyDown={handleAddTag}
      />
      <div className="tag-list">
        {tags.map((tag, i) => (
          <span key={i} className="tag-chip">{tag}</span>
        ))}

      </div>
        <div className="tag-list">
        {tags.map((tag, i) => (
            <span key={i} className="tag-chip">
            {tag}
            <button onClick={() => handleRemoveTag(tag)}>X</button>  {/* Add a button to remove tag */}
            </span>
        ))}
        <p> </p>
        </div>
      {post.image_url && (
                  <img
                    src={post.image_url}// Adjust the URL as needed
                    alt="Blog Post"
                    className="post-image"
                  />
        )}
        {/* Display the image if it exists */}
        <small className="blog-labels">Upload Image</small>
      <input type="file" accept="image/*" onChange={handleImageChange} />
      {imagePreview && <img src={imagePreview} alt="Image Preview" className="preview-image" />}
      
      {/*Display buttons for saving the post or as a draft */}
      <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
        <button onClick={() => handleSave('published')} className="publish-button">Publish</button>
        <button onClick={() => handleSave('draft')} className="draft-button">Save as Draft</button>
      </div>
    </div>
    </div>
  );
}

export default EditPost;
