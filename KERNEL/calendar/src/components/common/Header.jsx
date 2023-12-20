import React from "react";
import styled from "styled-components";
import { logo, chatIcon } from "../../assets/index";

const Header = () => {
  return (
    <StyledRoot>
      <img className="logo" src={logo} alt="" />
      <Menu>
        <li>나의 직업 가치관</li>
        <li>일정관리</li>
        <li>만다라트</li>
        <li>2023트렌드</li>
        <li>스터디그룹모집</li>
        <li>추천채용</li>
      </Menu>
      <hr />
      <Login>로그인</Login>
      <Service>마이페이지</Service>
      <SignUp>회원가입</SignUp>
      <ChatImg src={chatIcon}></ChatImg>
    </StyledRoot>
  );
};

export default Header;

const StyledRoot = styled.div`
  display: flex;
  .logo {
    display: flex;
    margin: 10px;
    cursor: pointer;
    width: 15vw;
    height: 9vh;
  }
  & > hr {
    opacity: 40%;
  }
`;

const Menu = styled.div`
  display: flex;
  align-self: center;
  margin-left: 10vw;

  li {
    display: flex;
    font-size: 15px;
    color: #6e6e6e;
    font-weight: bold;
    margin-left: 20px;
    margin-right: 20px;
    cursor: pointer;
  }
`;

const Login = styled.div`
  margin: 20px;
  color: #6e6e6e;
  font-weight: bold;
`;

const ChatImg = styled.img`
  width: 2.5vw;
  height: 5vh;
  margin: 20px;
`;

const SignUp = styled.div`
  margin: 20px;
  color: #6e6e6e;
  font-weight: bold;
  cursor: pointer;
`;

const Service = styled.div`
  margin: 20px;
  color: #6e6e6e;
  font-weight: bold;
`;
