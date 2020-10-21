import React, { useState, useEffect } from 'react';
import { animateScroll } from "react-scroll";
import Linkify from 'react-linkify';

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
                        if(msgs.name == props.name)
                            return <li id="self" key={index}>
                                    <img src={ msgs.image }/><br/><strong>You</strong><br/>
                                    <span id="people">
                                    <Linkify>{ msgs.text }</Linkify>
                                    </span><br/>
                                    <span id="time">{ msgs.time }</span>
                                    </li>;
                        else
                            return <li id={ msgs.name.valueOf() == 'BimboBOT'? 'chat_bot' : 'others' } key={index}>
                            <span id="people"><img src={ msgs.image } /><br/><strong>{ msgs.name }:</strong><br/>
                                <Linkify>{ msgs.text }</Linkify></span><br/>
                            <span id="time">{ msgs.time }</span>
                            </li>})
                }
            </ul>
        </div>
        );
}