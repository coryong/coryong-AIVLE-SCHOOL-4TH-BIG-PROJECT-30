import React from 'react';
import Layout from './components/Layout/Layout.jsx'; //Header,footer보여주기
import {AuthProvider } from './components/context/AuthContext.js';
import Container from '@mui/material/Container'; //npm install @mui/material @mui/styled-engine-sc styled-components
//npm install @mui/material @emotion/react @emotion/styled 둘다 설치해야 보인다


const App = () => {
  return (
    <Container fixed>
      <AuthProvider>
        <Layout>
        </Layout>
      </AuthProvider>
    </Container>
  );
};

export default App;
