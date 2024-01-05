import React from "react";
import { NavLink } from "react-router-dom";
import styled from "styled-components";
import SidebarItem from "./SidebarItem";
import profile from "../../assets/profile1.png";

const Side = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 10%;
  background-color: #444; /* Dark background */
  color: white; /* Light text */
  height: 100vh; /* Full viewport height */
  font-family: 'Arial', sans-serif; /* Font similar to the image */
  height: 700px;
  margin: 10px;
  gap: 10px;

`

const Profile = styled.img`
  width: 100px; /* Smaller profile picture */
  height: 100px; /* Smaller profile picture */
  border-radius: 50%; /* Circular profile picture */
  margin-top: 20px; /* Space from the top */
  border: 3px solid #555; /* Border around the profile picture */
`
const Menu = styled.div`
  margin-top: 30px;
  width: 100%; /* Full width of the sidebar */
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Align items to the left */
`
const LinkStyle = {
    color: "gray",
    textDecoration: "none"
  };
  
const ActiveLinkStyle = {
    color: "black"
  };
  

function Sidebar() {
  const menus = [
    { name: "홈", path: "/first"},
    { name: "나만의 만다르트", path: "/man" },
    { name: "추천 시스템", path: "/mylist" },
    { name: "공모전 게시판", path: "/recommend" },
    { name: "잡다 정보 게시판", path: "/post" },
    { name: "내 정보", path: "/setting"}
  ];
  return (
    <Side>
      <Profile src={profile}></Profile>
      <Menu>
        {menus.map((menu, index) => {
          return (
            <NavLink
              to={menu.path}
              key={index}
              style={({ isActive }) =>
                isActive ? { ...LinkStyle, ...ActiveLinkStyle } : LinkStyle
              }
            >
            <SidebarItem
                menu={menu}
            />
            </NavLink>
          );
        })}
      </Menu>
    </Side>
  );
}

export default Sidebar;