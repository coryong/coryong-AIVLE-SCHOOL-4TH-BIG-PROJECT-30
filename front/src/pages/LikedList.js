import React from "react";
import styled from "styled-components";

const LikedListContainer = styled.div`
  padding: 20px;
`;

function LikedList() {
  return (
    <LikedListContainer>
      <h1>Liked List</h1>
      <p>Check out the places you've liked.</p>
    </LikedListContainer>
  );
}

export default LikedList;