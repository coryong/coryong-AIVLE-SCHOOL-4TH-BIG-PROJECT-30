import React, { useState,useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; 

function Register() {
    const [formData, setFormData] = useState({
        nickname: '',
        email: '',
        name: '',
        password: '',
        cover_letter: '',
        occupation: '',
        technology_stacks: []  // 기술 스택을 배열로 초기화
    });
    const [techStacks, setTechStacks] = useState([]);  // 기술 스택 상태
    const navigate = useNavigate();
    // 기술 스택 데이터 불러오기
    useEffect(() => {
        fetch('http://localhost:8000/user/TechnologyStack/')
            .then(response => response.json())
            .then(data => setTechStacks(data))
            .catch(error => {
            // 에러 처리
                console.error('Error fetching tech stacks:', error);
            });
    }, []);  // 빈 의존성 배열로 마운트 시에만 호출

    

    // CSRF 토큰을 가져오는 함수
    const getCsrfToken = () => {
        let token = null;
        if (document.cookie) {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (name === 'csrftoken') {
                    token = value;
                    break;
                }
            }
        }
        return token;
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
          ...formData,
          [name]: value,
        });
      };
    
    const handleTechStackChange = (e) => {
        try {
            // 선택된 기술 스택의 ID를 배열로 변환
            const selectedStacks = Array.from(e.target.selectedOptions, option => parseInt(option.value));
            setFormData({
                ...formData,
                technology_stacks: selectedStacks,
            });
        } catch (error) {
            // 에러 처리
            console.error('Error handling tech stack change:', error);
        }
    };
    const handleSubmit = (e) => {
      e.preventDefault();
      const csrftoken = getCsrfToken();

      axios.post('http://localhost:8000/user/signup/', formData, {
          headers: {
              'X-CSRFToken': csrftoken
          }
      })
      .then(res => {
          console.log(res);
          navigate('/login'); // 회원가입 성공 후 로그인 페이지로 이동
      })
      .catch(err => {
          console.error(err);
          // 에러 처리
      });
  };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" name="nickname" onChange={handleChange} placeholder="Nickname" />
            <input type="email" name="email" onChange={handleChange} placeholder="Email" />
            <input type="text" name="name" onChange={handleChange} placeholder="Name" />
            <input type="password" name="password" onChange={handleChange} placeholder="Password" />
            <textarea name="cover_letter" onChange={handleChange} placeholder="Cover Letter"></textarea>
            <input type="text" name="occupation" onChange={handleChange} placeholder="Occupation" />
            <select multiple name="technology_stacks" onChange={handleTechStackChange}>
                {techStacks.map(stack => (
                    <option key={stack.id} value={stack.id}>{stack.stack_name}</option>
                ))}
            </select>
            <button type="submit">Register</button>
        </form>
    );
}

export default Register;
