import React, { useState, useEffect } from 'react';

import * as ReactDOM from 'react-dom';

import { Content } from './Content';
import { Users } from './Users';
import { Socket } from './Socket';

export default function App() {
  const [currUsr, setUsr] = useState({
    name: '', email: '', image: '', sid: '',
  });
  const { name } = currUsr;
  const { email } = currUsr;
  const { image } = currUsr;
  const { sid } = currUsr;
  const [isLoggedIn, setStatus] = useState(false); //

  Socket.emit('connect');

  function getNewUser() {
    useEffect(() => {
      Socket.on('set user', (data) => {
        if (data.sid === Socket.id) {
          console.log(`Welcome: ${data.name}\nEmail: ${data.email}\nImage/: ${data.imgUrl}`);
          setUsr((prevState) => ({
            name: data.name,
            email: data.email,
            image: data.imgUrl,
            sid: data.sid,
          }));
          setStatus((prevStatus) => true);
        }
      });
      Socket.off('set user', '');
      
      Socket.on('failed login', (data) => {
        if (data.sid === Socket.id) {
          alert('Login Failed! \'' + data['email'] + '\' already logged in!');
        }else{
          alert('Someone just tried to login with your email! If this wasn\'t you then change your password immediately!');
        }
      });
      Socket.off('failed login', '');
    });
  }
  getNewUser();
  return (
    <div>
      <h1 id="title">Not Discord</h1>
      <p id="welcome">
        {' '}
        Welcome!
        <strong>
          { name }
          {' '}
        </strong>
      </p>
      <Users
        name={name}
        email={email}
        image={image}
        sid={sid}
      />
      <Content
        name={name}
        email={email}
        image={image}
        sid={sid}
        isLoggedIn={isLoggedIn}
      />
    </div>
  );
}
ReactDOM.render(<App />, document.getElementById('content'));
