import React, { useContext } from 'react'
import { BrowserRouter, Routes, Route} from 'react-router-dom'
import './App.scss';
import Login from './components/Login';
import Signup from './components/Signup';
import 'bootstrap/dist/css/bootstrap.min.css'
import Home from './components/Home';
import UserInfo from './components/UserInfo'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Login/>}></Route>
        <Route path='/signup' element={<Signup/>}></Route>
        <Route path='/home' element={<Home/>}></Route>
        <Route path='/user_info' element={<UserInfo/>}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
