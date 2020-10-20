import React, { useState, useEffect } from 'react';
import { animateScroll } from "react-scroll";

import { Socket } from './Socket';

export function Chatbox(props) {
    
    const msgs = props.chatLog;
    console.log("msgs: " + props.chatLog);
    function scroll() {
        animateScroll.scrollToBottom({
        containerId: "msg_list"
        });
    }
    useEffect(() => { scroll(); });
    return (
        <div id="logs"
            className="chat">
            <ul id="msg_list">
                {msgs.map(( msgs, index) => {
                console.log(msgs.name + "\n" + props.name);
                        if(msgs.name == props.name)
                            return <li id="self" key={index}>
                                    <span id="people">{ msgs.text }</span>
                                    </li>;
                        else
                            return <li id={ msgs.name.valueOf() == 'BimboBOT'? 'chat_bot' : 'others' } key={index}>
                            <span id="people"><strong>{ msgs.name }: </strong>{ msgs.text }</span></li>})
                }
            </ul>
        </div>
        );
}