import Dealers from './components/Dealers/Dealers';
import Register from "./components/Register/Register";
import LoginPanel from "./components/Login/Login";
import RootPage from "./components/RootPage"; // Import your RootPage component
import LogoutPage from "./components/LogoutPage"; // Import your LogoutPage component
import { Routes, Route } from "react-router-dom";

function App() {
    return (
      <Routes>
        <Route path="/login" element={<LoginPanel />} />
        <Route path="/root" element={<RootPage />} />
        <Route path="/logout" element={<LogoutPage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dealers" element={<Dealers/>} />
      </Routes>
    );
}

export default App;