import React from "react";
import styled from "styled-components";

const SettingContainer = styled.div`
  padding: 20px;
`;

function Setting() {
  return (
    <SettingContainer>
      <h1>Settings</h1>
      <p>Adjust your preferences here.</p>
    </SettingContainer>
  );
}

export default Setting;
