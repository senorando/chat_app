import React, { useState, useEffect } from 'react';
import { animateScroll } from "react-scroll";

import { Socket } from './Socket';

export function Chatbox() {
    function scroll() {
        animateScroll.scrollToBottom({
            containerId: "msg_list"
        });
    }
    const [msgs, setMsgs] = useState([]);
    
    useEffect(() => { scroll(); });
    
    useEffect(() => {
        Socket.on('message received', (data) => { 
            setMsgs(data['allMessages']);
        });
    });
    
    return (
        <div id="logs"
            className="chat">
            <ul id="msg_list">
                {msgs.map((msgs,index) => {
                        if(index%2 == 1)
                            return <li id="left" key={index}>
                            <span id="people">{msgs}</span>
                            </li>
                        else
                            return <li id="right" key={index}>
                            <span id="people">{msgs}</span></li>})
                }
            </ul>
        </div>
        );
}