import React, { useState, useEffect } from 'react';

import { Main } from './Main';

import { Login } from './GoogleButton';
import { Text_Box } from './Text_Box';
import { Chatbox } from './Chat';
import { Socket } from './Socket';

export function Content(props) {
    const [chatLog, updateChat] = useState([]);
    const isLoggedIn = props.isLoggedIn;
    
    function nextLine() {
        useEffect(() => {
            Socket.on('message received', (data) => {
                console.log("Received messages from server...\n" + data['allMessages']);
                updateChat(data['allMessages']);
            });
            return (() => {
                Socket.off('message received', "");
            });
        });
    }
    nextLine();
    
    return (
        <div>
            <Chatbox name={ props.name } 
                email={ props.email } 
                image={ props.image } 
                sid={ props.sid } 
                chatLog={ chatLog } 
                 />
            <br/>
            { isLoggedIn? 
                <Text_Box name={ props.name } 
                email={ props.email }
                image={ props.image }
                />
                : 
                <div id="Login">Please login to Google!<Login /></div>
            }
        </div>
    );
}
