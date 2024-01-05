import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import Button from '../../pages/ui/Button';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import OutlinedInput from '@mui/material/OutlinedInput';

// Styled components
const Wrapper = styled.div`
  padding: 16px;
  width: calc(100% - 32px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #f4f4f4; // Light background for the wrapper
  min-height: 100vh; // Full viewport height
`;

const Container = styled.div`
  width: 100%;
  max-width: 720px;
  background-color: white; // White background for the form container
  padding: 20px;
  border-radius: 8px; // Rounded corners
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); // Subtle shadow for depth
  margin-bottom: 16px;

  @media (max-width: 768px) {
    margin: 0 10px; // Margin for smaller screens
  }
`;


// TitleField 컴포넌트
const TitleField = ({ title, handleInputChange }) => (
<Grid item xs={12}>
  <TextField
    fullWidth
    label="Title"
    id="Title"
    type="text"
    name="title"
    value={title}
    onChange={handleInputChange}
  />
</Grid>
);

// CategorySelect 컴포넌트
const CategorySelect = ({ categories, selectedCategories, handleCategoryChange }) => (
<Grid item xs={12}>
  <FormControl fullWidth variant="outlined">
    <InputLabel id="categories-label">Categories</InputLabel>
    <Select
      labelId="categories-label"
      id="Categories"
      multiple
      value={selectedCategories}
      onChange={handleCategoryChange}
      input={<OutlinedInput label="Categories" />}
      name="categories"
    >
      {categories.map((category) => (
        <MenuItem key={category.id} value={category.id}>
          {category.name}
        </MenuItem>
      ))}
    </Select>
  </FormControl>
</Grid>
);



// TechnologyStackSelect 컴포넌트
const TechnologyStackSelect = ({ occupationName, selectedStacks, handleStackChange, technologyStacks }) => (
<Grid item xs={12}>
  <h3>{occupationName} Required Skills</h3>{/* 직업 이름을 표시 */}
  <FormControl fullWidth variant="outlined">
    <InputLabel id="technology-stacks-label">Required Skills</InputLabel>
    <Select
      labelId="technology-stacks-label"
      id="TechnologyStacks"
      multiple
      value={selectedStacks}
      onChange={handleStackChange}
      input={<OutlinedInput label="Required Skills" />}
      name="technology_stacks"
    >
      {technologyStacks.map((stack) => (
        <MenuItem key={stack.id} value={stack.id}>
          {stack.stack_name}
        </MenuItem>
      ))}
    </Select>
  </FormControl>
</Grid>
);


// EnvSelect 컴포넌트
const EnvSelect = ({ envs, selectedEnv, handleEnvChange }) => (
  <Grid item xs={12}>
    <FormControl fullWidth variant="outlined">
      <InputLabel id="env-label">Work Environment</InputLabel>
      <Select
        labelId="env-label"
        id="env"
        value={selectedEnv}
        onChange={handleEnvChange}
        input={<OutlinedInput label="Work Environment" />}
        name="env"
      >
        {envs.map((env) => (
          <MenuItem key={env.id} value={env.id}>
            {env.env_name}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  </Grid>
);
// RecommendWrite 메인 컴포넌트
const RecommendWrite = () => {
const [newPost, setNewPost] = useState({
  title: '',
  cate: '',
  technology_stacks: [],
  env: '',
  Exp_require: '',
  occupation: [],
  Project_Description: '',
  categories: [],
  requiredSkills: {},
  image: null,
});



const [categories, setCategories] = useState([]);
const [technologyStacks, setTechnologyStacks] = useState([]); // Technology stacks state
const [selectedTechStacks, setSelectedTechStacks] = useState({}); // Selected tech stacks for each occupation
const [envs, setEnvs] = useState([]); // 'env' 데이터를 위한 상태
const navigate = useNavigate();
const yourAuthToken = localStorage.getItem('token');

const handleStackChange = (occupationId) => (event) => {
  const {
    target: { value },
  } = event;
  
  // "value"는 하나의 값이 선택된 경우 문자열 형식이며 여러 값을 선택한 경우 배열 형식입니다.
  // 항상 배열로 처리되도록 확인해야 합니다.
  const allSelectedStacks = typeof value === 'string' ? value.split(',') : value;
  
  // 주어진 직업에 대한 선택된 기술 스택을 업데이트합니다.
  setSelectedTechStacks({
    ...selectedTechStacks,
    [occupationId]: allSelectedStacks,
  });
};

const handleInputChange = (e) => {
  const { name, value } = e.target;
  setNewPost({ ...newPost, [name]: value });
};

const handleCategoryChange = (event) => {
  const { value } = event.target;
  setNewPost({ ...newPost, occupation: value});
};

const handleEnvChange = (event) => {
  const { value } = event.target;
  setNewPost({ ...newPost, env: value });
};
const handleImageChange = (e) => {
  const file = e.target.files[0]; // 파일 객체 접근
  if (file) {
    setNewPost({ ...newPost, image: file }); // 파일 객체를 상태에 저장
  }
};
const addPost = async (e) => {
  e.preventDefault();

  
  
  const formData = new FormData();
   // 텍스트 데이터를 FormData에 추가
   formData.append('title', newPost.title);
   formData.append('cate', newPost.cate);
   formData.append('Exp_require', newPost.Exp_require);
   formData.append('Project_Description', newPost.Project_Description);

   // 선택된 기술 스택을 FormData에 추가
   const combinedTechStacks = Object.values(selectedTechStacks).flat();
   const uniqueTechStacks = Array.from(new Set(combinedTechStacks));
   uniqueTechStacks.forEach(stack => formData.append('technology_stacks', stack));

   // 선택된 occupation을 FormData에 추가
   newPost.occupation.forEach(occ => formData.append('occupation', occ));

   // 선택된 env를 FormData에 추가 (하나만 선택된 경우)
   if (newPost.env) formData.append('env', newPost.env);

   // 이미지 파일을 FormData에 추가 (파일이 있는 경우)
   if (newPost.image) {
     formData.append('image', newPost.image);
   }
  try {
    const response = await axios.post('http://127.0.0.1:8000/recommend/Recommend/', formData, {
      headers: {
        'Authorization': `Bearer ${yourAuthToken}`,
      }
    });
    if (response.status === 201) {
      navigate('/recommend');
    } else {
      console.error('Failed to add post');
    }
  } catch (error) {
    console.error('Error adding post:', error);
  }
};

useEffect(() => {
  const fetchOccupations = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/user/Occupation/');
      setCategories(response.data); // 전체 occupation 데이터 저장
    } catch (error) {
      console.error('Error fetching occupations:', error);
    }
  };

  const fetchTechnologyStacks = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/user/TechnologyStack/');
      setTechnologyStacks(response.data); // Save technology stacks data
    } catch (error) {
      console.error('Error fetching technology stacks:', error);
    }
  };

  const fetchEnvs = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/user/Env/');
      setEnvs(response.data); // 'env' 데이터 저장
    } catch (error) {
      console.error('Error fetching envs:', error);
    }
  };

  fetchEnvs();
  fetchOccupations();
  fetchTechnologyStacks();
}, []);

return (
  <Wrapper>
    <Container>
      <h1>Add a New Post</h1>
      <form onSubmit={addPost}>
        <Grid container spacing={2}>
          <TitleField title={newPost.title} handleInputChange={handleInputChange} />
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="cate"
              id="cate"
              type="text"
              name="cate"
              value={newPost.cate}
              onChange={handleInputChange}
            /></Grid>
          <CategorySelect
            categories={categories.map(c => ({ id: c.id, name: c.occupation_name }))}
            selectedCategories={newPost.occupation}
            handleCategoryChange={handleCategoryChange}
          />
          {newPost.occupation.map(occupationId => (
                <TechnologyStackSelect
                key={occupationId}
                occupationName={categories.find(c => c.id === occupationId).occupation_name}
                selectedStacks={selectedTechStacks[occupationId] || []}
                handleStackChange={handleStackChange(occupationId)}
                technologyStacks={technologyStacks}
                />
                ))}
          <Grid item xs={12}>
          <EnvSelect
          envs={envs}
          selectedEnv={newPost.env}
          handleEnvChange={handleEnvChange}
        />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Experience Requirements"
              id="Exp_require"
              type="text"
              name="Exp_require"
              value={newPost.Exp_require}
              onChange={handleInputChange}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Project Description"
              id="Project_Description"
              type="text"
              name="Project_Description"
              value={newPost.Project_Description}
              onChange={handleInputChange}
            />
          </Grid>
          <Grid item xs={12}>
            <input
              type="file"
              accept='image/*'
              name="image"
              onChange={handleImageChange}
            />
          </Grid>
          </Grid>
        <p><Button title='Add Post' type="submit" /></p>
      </form>
    </Container>
  </Wrapper>
);
};

export default RecommendWrite;
