import React from 'react';
import ReactDOM from 'react-dom';
import { GoogleLogin, GoogleLogout } from 'react-google-login';

import { Socket } from './Socket';

const clientId = '665762907278-4khe1gncrp9k6j23jfgej1l6i17s61k7.apps.googleusercontent.com';

export function Login() {
  const onSuccess = (res) => {
    const data = {
      name: res.profileObj.name,
      email: res.profileObj.email,
      imgUrl: res.profileObj.imageUrl,
    };
    console.log('|Login Success| currentUser: ', data);
    Socket.emit('new google', (data));
  };
  const onFailure = (res) => {
    console.log('|Login Failed| res:', res);
  };
  return (
    <div id="GoogleLogin">
      <GoogleLogin
        clientId={clientId}
        buttonText="Login"
        onSuccess={onSuccess}
        onFailure={onFailure}
        cookiePolicy="single_host_origin"
      />
    </div>
  );
}
export function Logout() {
  const onSuccess = () => {
    alert('Successfully Logged Out!');
  };
  return (
    <div id="GoogleLogout">
      <GoogleLogout
        clientId={clientId}
        buttonText="Logout"
        onLogoutSuccess={onSuccess}
      />
    </div>
  );
}
