import {Route, Routes} from 'react-router-dom';
import Home from './pages/Home.js';
import Login from './pages/Login.js';
import Join from './pages/Join.js';
import Post from './pages/Post.js';
import Categories from './components/Categories.js';

const App = () => {
  return(
    <Routes>
      <Route element={<Categories />}>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/join" element={<Join />} />
        <Route path="/post" element={<Post />} />
      </Route>
    </Routes>
  );
};

export default App;
