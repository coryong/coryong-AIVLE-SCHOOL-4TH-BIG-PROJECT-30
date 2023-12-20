import React, { useState } from 'react';

const Join = () => {
  // 상태 설정
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });

  // 입력 필드 변경 핸들러
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  // 폼 제출 핸들러
  const handleSubmit = (e) => {
    e.preventDefault();
    // 여기에서 회원가입 로직을 추가할 수 있습니다.
    console.log('회원가입 정보:', formData);
    // 추가적인 로직을 작성하세요 (예: 서버로 데이터 전송 등)
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        사용자 이름:
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
        />
      </label>
      <br />
      <label>
        이메일:
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
        />
      </label>
      <br />
      <label>
        비밀번호:
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
        />
      </label>
      <br />
      <button type="submit">가입하기</button>
    </form>
  );
};

export default Join;