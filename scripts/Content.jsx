import React, { useState, useEffect } from 'react';

import { Login } from './GoogleButton';
import { TextBox } from './TextBox';
import { Chatbox } from './Chat';
import { Socket } from './Socket';

export function Content(props) {
  const [chatLog, updateChat] = useState([]);
  const isLoggedIn = props.isLoggedIn;

  function nextLine() {
    useEffect(() => {
      Socket.on('message received', (data) => {
        updateChat(data.allMessages);
      });
      return (() => {
        Socket.off('message received', '');
      });
    });
  }
  nextLine();
  const ChatboxEl = (
    <Chatbox
      name={props.name}
      email={props.email}
      image={props.image}
      sid={props.sid}
      chatLog={chatLog}
    />
  );
  const GoogleButton = isLoggedIn
    ? (
      <TextBox
        name={props.name}
        email={props.email}
        image={props.image}
      />
    )
    : <Login />;
  return (
    <div>
      { ChatboxEl }
      <br />
      { GoogleButton }
    </div>
  );
}
