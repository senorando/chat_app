import React, { useState } from 'react';

import { Socket } from './Socket';

export function TextBox(props) {
  function pushVal(e) {
    const in_message = document.getElementById('msg');
    const data = {
      message: in_message.value,
      user_id: props.email,
      name: props.name,
      imageUrl: props.image,
    };
    console.log(data);
    if (data.message[0] === '!' && data.message[1] === '!') {
      console.log(`Sent command to the server!\n"${data.message}"`);
      Socket.emit('new command', data);
    } else {
      console.log(`Sent message to the server!\n"${data.message}"`);
      Socket.emit('new message', data);
    }
    e.preventDefault();
    document.getElementById('msg').value = '';
  }
  return (
    <div id="TextBox">
      <form
        className="chat"
        onSubmit={pushVal}
      >
        <input
          id="msg"
          className="msg_txt"
          placeholder="Enter a message here..."
          type="text"
        />
        <button
          className="send"
          type="submit"
        >
          Send
        </button>
      </form>
    </div>

  );
}
