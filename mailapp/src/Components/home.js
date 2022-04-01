import React, { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
// import JsonViewer from "react-json-view";
import { axiosInstance } from "../axiosApi";

export const Home = (props) => {
  let boxstyle = {
    borderRadius: "25px",
    border: "2px solid #73AD21",
    padding: "20px",
    width: "auto",
    height: "65vh",
    overflow: "auto",
    margin: "10px 10px 10px 10px",
    fontSize: "10px",
  };

  const [DataMail, setDataMail] = useState([]);
  useEffect(() => {
    axiosInstance
      .get("/sync/")
      .then((result) => {

        
        setDataMail([...result.data.results])
        
      })
      .catch((error) => {
        throw error;
      });
  }
  
  
  , []);

  useEffect(() => {
    setDataMail(DataMail.sort((a, b) => Date.parse(a.internalDate) - Date.parse(b.internalDate)));
  }, [DataMail]);

  const handleClick = () => {
    axiosInstance
      .post("/send_mail/", {
        sender: "puneetbindal8989@gmail.com",
        text: "Please Help Me!",
        msg: "Hello There, We will get back to you on this.",
      })
      .then((result) => {
        console.log(result)
        // window.location.href = "/";
      })
      .catch((error) => {
        throw error;
      });
  };

  
  return (
    <>
      { DataMail && DataMail.length ? (
        <>
          
          <Button
            onClick={handleClick}
            className="position-relative start-50 translate-middle mt-3"
            variant="btn btn-danger"
          >
            send Mail
          </Button>{" "}
          <div style={boxstyle}>
          <table id="dtHorizontalVerticalExample" className="table table-striped table-bordered table-sm "
    width="100%" >
            <thead>
              <tr className="text-primary">
                <th>Date time</th>
                <th>Sender</th>
                <th>Subject</th>
              </tr>
            </thead>
            <tbody>

            {
              DataMail.sort((a, b) => Date.parse(b.internalDate) - Date.parse(a.internalDate)).map(
                (a, i) => { 
                  return (
                      <tr className="text-info" key={i}>
                      <td className="text-info" >{a.internalDate}</td>
                      <td className="text-info" >{a.sender_mail}</td>
                      <td className="text-info" >{a.subject}</td>
                    </tr>
                  )
                  }   
              )
            
              }
            
              
            </tbody>
          </table>

          </div>
          


        </>
      ) : (
        <>
        </>
      )}
    </>
  );
};
