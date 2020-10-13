import React, { useState, useEffect } from 'react';
import { animateScroll } from "react-scroll";

import { Socket } from './Socket';

export function Chatbox(props) {
    const msgs = props.chatLog;
    
    function scroll() {
        animateScroll.scrollToBottom({
            containerId: "logs"
        });
    }
    useEffect(() => { scroll(); });
    return (
        <div id="logs"
            className="chat">
            <ul id="msg_list">
                { msgs.map(( msgs, index ) => (
                    <li id="chat_msg"
                        key={ index }
                        index={ index }>
                        <span id="people">
                            { msgs.name }
                        </span>
                        <span id="text">
                            { msgs.text }
                        </span>
                    </li>
                ))}
            </ul>
        </div>
        );
}