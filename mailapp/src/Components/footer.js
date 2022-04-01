import React from "react";

export const Footer = () => {
  let footerstyle = {
    position: "absolute",
    top: "90vh",
    width: "100%",
  };

  return (
    <div>
      <footer className="bg-dark text-light py-3" style={footerstyle}>
        <p className="text-center">Copyright &copy; mailapp.co</p>
      </footer>
    </div>
  );
};
