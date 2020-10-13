import React, { useState, useEffect } from 'react';

import { Main } from './Main';
import { Text_Box } from './Text_Box';
import { Chatbox } from './Chat';
import { Socket } from './Socket';

export function Content(props) {
    const [chatLog, updateChat] = useState([]);
    
    function nextLine() {
        useEffect(() => {
            Socket.on('Message Received...', (data) => {
                updateChat(data);
            });
            return () => {
                Socket.off('Message Received...', "");
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
