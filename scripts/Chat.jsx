import React, { useState, useEffect } from 'react';
import { animateScroll } from "react-scroll";

import { Socket } from './Socket';

export function Chatbox() {
    function scroll() {
        animateScroll.scrollToBottom({
            containerId: "logs"
        });
    }
    const [msgs, setMsgs] = useState([]);
    
    useEffect(() => { scroll(); });
    
    useEffect(() => {
        Socket.on('message received', (data) => { 
            setMsgs(data['allMessages']);
            console.log(data['allMessages']);
        });
    });
    
    return (
        <div id="logs"
            className="chat">
            <ul id="msg_list">
                { msgs.map(( msgs, index ) => (
                    <li id="chat_msg"
                        key={ index }
                        index={ index }>
                        <span id="people">
                            { msgs }
                        </span>
                    </li>
                ))}
            </ul>
        </div>
        );
}