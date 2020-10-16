import React, { useState, useEffect } from 'react';

import { Main } from './Main';
import { Text_Box } from './Text_Box';
import { Chatbox } from './Chat';
import { Socket } from './Socket';

export function Content(props) {
    const [chatLog, updateChat] = useState([]);
    
    function nextLine() {
        useEffect(() => {
            Socket.on('new message', (data) => {
                console.log("Received messages from server...\n" + data['allMessages']);
                updateChat(data['allMessages']);
            });
            return () => {
                Socket.off('new message', "");
            }
        });
    }
    nextLine();
    
    return (
        <div>
            <h1 id="title">Not Discord</h1>
            <Chatbox chatLog={ chatLog } />
            <Text_Box name={ props.user_info } />
        </div>
    );
}
