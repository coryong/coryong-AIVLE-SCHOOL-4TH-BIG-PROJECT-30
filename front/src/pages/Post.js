import React, { useState, useEffect } from 'react';
import axios from 'axios'; //설치 필요

const Post = () => {
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState({ title: '', content: '' });

  useEffect(() => {
    // API에서 데이터를 가져와서 상태를 업데이트합니다.
    axios.get('http://localhost:8000/api/blog/')
      .then(response => setPosts(response.data.posts))
      .catch(error => console.error(error));
  }, []);

  const addPost = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/blog/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Origin': 'http://localhost:3000',
        },
        body: JSON.stringify(newPost),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      if (data.success) {
        // Update state with the new post
        setPosts([...posts, data.post]);
        // Clear the newPost state
        setNewPost({ title: '', content: '' });
      } else {
        console.error('Failed to add post:', data.error);
      }
    } catch (error) {
      console.error('Error adding post:', error);
      // 더 많은 세부 정보를 얻기 위해 전체 응답 기록
      console.error('Full response:', error.response);
    }
  };

  return (
    <div>
      <h1>Add a New Post</h1>
      <label>
        Title:
        <input
          type="text"
          value={newPost.title}
          onChange={(e) => setNewPost({ ...newPost, title: e.target.value })}
        />
      </label>
      <br />
      <label>
        Content:
        <textarea
          value={newPost.content}
          onChange={(e) => setNewPost({ ...newPost, content: e.target.value })}
        />
      </label>
      <br />
      <button onClick={addPost}>Add Post</button>

      {/* Display existing posts */}
      <div>
        <h2>Existing Posts</h2>
        <ul>
          {posts.map((post) => (
            <li key={post.id}>
              <strong>{post.title}</strong>
              <p>{post.content}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Post;
