import React from "react";
import styled from "styled-components";

const MyListContainer = styled.div`
  padding: 20px;
`;

function MyList() {
  return (
    <MyListContainer>
      <h1>My List</h1>
      <p>This is where you can find your own list of places.</p>
    </MyListContainer>
  );
}

export default MyList;