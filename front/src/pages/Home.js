import React from "react";
import styled from "styled-components";

const HomeContainer = styled.div`
  padding: 20px;
`;

function Home() {
  return (
    <HomeContainer>
      <h1>Home</h1>
      <p>Welcome to the home page!</p>
    </HomeContainer>
  );
}

export default Home;