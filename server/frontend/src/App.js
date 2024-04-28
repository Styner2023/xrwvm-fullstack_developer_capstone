import React from 'react';
// import Dealers from './components/Dealers';
import Dealers from './components/Dealers/Dealers';
import Dealer from "./components/Dealers/Dealer"
import Register from "./components/Register/Register";
import LoginPanel from "./components/Login/Login";
import RootPage from "./components/RootPage"; // Import your RootPage component
import LogoutPage from "./components/LogoutPage"; // Import your LogoutPage component
import { Routes, Route } from "react-router-dom";
import PostReview from "./components/Dealers/PostReview"

function App() {
    return (
      <Routes>
        <Route path="/login" element={<LoginPanel />} />
        <Route path="/root" element={<RootPage />} />
        <Route path="/logout" element={<LogoutPage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dealers" element={<Dealers/>} /> 
        <Route path="/dealer/:id" element={<Dealer/>} />
        <Route path="/postreview/:id" element={<PostReview/>} />
      </Routes>
    );
}

export default App;