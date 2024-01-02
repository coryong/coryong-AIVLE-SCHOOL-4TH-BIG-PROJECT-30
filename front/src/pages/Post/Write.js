import axios from 'axios';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import Button from '../../pages/ui/Button';
import ImageUploadExample from './ImageUploadExample';
import './Post.css';



const Wrapper = styled.div`
    padding: 32px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #f7f7f7;
`;

const Container = styled.div`
    width: 100%;
    max-width: 720px;
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    margin-bottom: 16px;
`;

const StyledForm = styled.form`
    display: flex;
    flex-direction: column;
    gap: 20px;
`;

const StyledLabel = styled.label`
    display: flex;
    flex-direction: column;
    font-weight: 600;
    color: #333;
`;

const StyledInput = styled.input`
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-top: 8px;
`;

const StyledTextArea = styled.textarea`
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-top: 8px;
    height: 120px; /* 또는 원하는 높이 */
`;
const CreatePost = () => {
  const [newPost, setNewPost] = useState({ title: '', body: '' });
  const navigate = useNavigate();

  // 이 부분은 인증 토큰을 어디서 가져오는지에 따라 달라집니다.
  // 예를 들어, localStorage에서 토큰을 가져오는 경우:
  const yourAuthToken = localStorage.getItem('token');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewPost({ ...newPost, [name]: value });
  };

  const addPost = async () => {
    try {
      const response = await axios.post('http://localhost:8000/post/post/', newPost, {
        headers: {
          'Authorization': `Bearer ${yourAuthToken}`  // 헤더에 토큰 추가
          
        }
      });

      if (response.status === 201) {
        navigate('/post');
      } else {
        console.error('Failed to add post');
      }
    } catch (error) {
      console.error('Error adding post:', error);
    }
  };

  return (
    <Wrapper>
      <Container>
        <div className="board-title">Write content</div>
        <StyledForm onSubmit={(e) => {
          e.preventDefault();
          addPost();
        }}>
          <StyledLabel>
            Title
            <StyledInput
              type="text"
              name="title"
              height={20}
              value={newPost.title}
              onChange={handleInputChange}
            />
          </StyledLabel>
          <StyledLabel>
            Body
            <StyledTextArea
              name="body"
              height={480}
              value={newPost.body}
              onChange={handleInputChange}
            />
          </StyledLabel>
          <ImageUploadExample />
          <Button title='Add Post' type="submit"/>
        </StyledForm>
      </Container>
    </Wrapper>
  );
};

export default CreatePost;
