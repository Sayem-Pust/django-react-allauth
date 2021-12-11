import React, { Component } from "react";
import FacebookLogin from "react-facebook-login";
import GoogleLogin from "react-google-login";
// import fbLogin from "./services/fbLogin";
import googleLogin from "./services/googleLogin";
import "./App.css";

class App extends Component {
  render() {
    const responseFacebook = async (response) => {
      // let fbResponse = await fbLogin(response.accessToken);
      // console.log(fbResponse);
      console.log(response);
    };

    const responseGoogle = async (response) => {
      console.log(response);
      let googleResponse = await googleLogin(response.accessToken);
      console.log(googleResponse);
      
    };


    return (
      <div className="App">
        <h1>LOGIN WITH FACEBOOK AND GOOGLE</h1>

        <FacebookLogin
          appId="<FACEBOOK APP ID>"
          fields="name,email,picture"
          callback={responseFacebook}
        />
        <br />
        <br />

        <GoogleLogin
          clientId="995754490857-vqpo9naaud6f43q9p1avh7kul1b0sii6.apps.googleusercontent.com"
          buttonText="LOGIN WITH GOOGLE"
          onSuccess={responseGoogle}
          onFailure={responseGoogle}
        />
      </div>
    );
  }
}

export default App;
