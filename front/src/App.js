import React from "react";
import styled from "styled-components";
import { BrowserRouter,Routes,Route } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Home from "./pages/Home";
import MyList from "./pages/MyList";
import LikedList from "./pages/LikedList";
import Setting from "./pages/Setting";
const Center = styled.div`
  height: 92vh;
  display: flex;
  flex-direction: row;
`

class App extends React.Component {
  render() {
    return(
      <BrowserRouter>
        
        <Center>
          <Sidebar/>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/mylist" element={<MyList />} />
            <Route path="/likedlist" element={<LikedList />} />
            <Route path="/setting" element={<Setting />} />
          </Routes>
        </Center>
      </BrowserRouter>
    );
  }
}
export default App;