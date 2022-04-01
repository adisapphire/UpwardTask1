import React, { useState } from "react";
import { axiosInstance } from "../axiosApi";

export const SignUp = () => {
  const [email, setemail] = useState("");
  const [pwd, setpwd] = useState("");
  const [username, setusername] = useState("");

  const submit = (e) => {
    e.preventDefault();
    axiosInstance.defaults.headers["Content-Type"] = "application/json";
    axiosInstance
      .post("/register/", {
        email: email,
        username: username,
        password: pwd,
      })
      .then((result) => {
        axiosInstance.defaults.headers["Authorization"] =
          "JWT " + result.data.token;
        localStorage.setItem("access_token", result.data.token);
        localStorage.setItem("refresh_token", result.data.refresh);
        localStorage.setItem("userData", result.data.user.username);
        window.location.href = "/";
      })
      .catch((error) => {
        throw error;
      });
  };

  return (
    <div className="row g-3 align-items-center">
      <h4 className="start-50">SignUp</h4>
      <form onSubmit={submit}>
        <div className="col-auto">
          <label htmlFor="username" className="form-label">
            Username
          </label>
          <input
            type="username"
            value={username}
            onChange={(e) => setusername(e.target.value)}
            className="form-control"
            id="username"
            aria-describedby="usernameHelp"
            required
          />
        </div>
        <div className="col-auto">
          <label htmlFor="email" className="form-label">
            Email address
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setemail(e.target.value)}
            className="form-control"
            id="email"
            aria-describedby="emailHelp"
            required
          />
          <div id="emailHelp" className="form-text">
            We'll never share your email with anyone else.
          </div>
        </div>
        <div className="mb-3">
          <label htmlFor="pwd" className="form-label">
            Password
          </label>
          <input
            type="password"
            value={pwd}
            onChange={(e) => setpwd(e.target.value)}
            className="form-control"
            id="pwd"
            required
          />
        </div>
        <button type="submit" className="btn btn-sm btn-success">
          SignUp
        </button>
      </form>
    </div>
  );
};
