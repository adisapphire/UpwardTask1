import { Button, Row, Col } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import React from "react";

export default function Header(props) {
  let navigate = useNavigate();

  const logout = () => {
    localStorage.clear();
    window.location.href = "/login/";
  };

  return (
    <Row>
      <Col className="ml-auto">
        <Row>
          <Col className="col-sm-auto">
            <div className="mt-1 ms-1">Hello {props.username}!</div>
          </Col>
          <Col className="col-sm-3">
            <Button onClick={() => navigate("/")} variant="outline-success">
              Home
            </Button>{" "}
          </Col>
        </Row>
      </Col>
      {props.isAuth === false ? (
        <Col className="mr-auto">
          <Button
            className="float-end me-1"
            onClick={() => navigate("/signup")}
            variant="outline-success"
          >
            SignUp
          </Button>{" "}
          <Button
            className="float-end me-1"
            onClick={() => navigate("/login")}
            variant="outline-success"
          >
            LogIn
          </Button>{" "}
        </Col>
      ) : (
        <Col className="mr-auto">
          <Button
            className="float-end me-1"
            onClick={() => logout()}
            variant="outline-success"
          >
            LogOut
          </Button>{" "}
        </Col>
      )}
    </Row>
  );
}
