import "./App.css";
import Header from "./Components/header";
import { Home } from "./Components/home";
import { LogIn } from "./Components/login";
import { SignUp } from "./Components/signup";
import { Footer } from "./Components/footer";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import { useState, useEffect } from "react";

function App() {
  const [isAuth, setIsAuth] = useState(false);
  const [username, serUsername] = useState("");
  const [datajson, setDatajson] = useState([]);

  useEffect(() => {
    if (localStorage.getItem("access_token") !== null) {
      setIsAuth(true);
      serUsername(localStorage.getItem("userData"));
    }
  }, []);

  return (
    <div className="App">
      <Router>
        <Header isAuth={isAuth} username={username} />
        <Routes>
          <Route
            exact
            path="/"
            element={
              localStorage.getItem("access_token") !== null ? (
                <Home username={username} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />
          <Route exact path="/login" element={<LogIn />} />
          <Route exact path="/signup" element={<SignUp />} />
          {/* <Route path="*" element={<NotFound/>}/> */}
        </Routes>
        <Footer />
      </Router>
    </div>
  );
}

export default App;
