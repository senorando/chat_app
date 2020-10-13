import React, { useState } from 'react';

import { Socket } from './Socket';

export function Text_Box(props) {
    console.log(props.name);
    
    function pushVal(val) {
        let in_message = document.getElementById("msg");
        let data = [
            { name: props.name },
            { message: in_message.value }
        ];
        Socket.emit("Incoming Message... ", data);
        val.preventDefault();
        document.getElementById("msg").value = "";
    }
    return (
        <form className="chat"
            onSubmit = { pushVal }>
            <input id="msg"
                className="msg_txt"
                placeholder="Enter a message here..."
                type="text"/>
            <button className="send"
                type="submit">
                Send
            </button>
        </form>
    );
}