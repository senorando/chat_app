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
                        if(msgs.email == props.email)
                            return <li id="self" key={index}>
                                    <span id="msgs">
                                    <Linkify>{ msgs.text }</Linkify>
                                    </span><br/>
                                    <span id="time">{ msgs.time }</span><br/>
                                    </li>;
                        else
                            return <li id={ msgs.name.valueOf() == 'BimboBOT'? 'chat_bot' : 'others' } key={index}>
                            <span id="msgs"><img src={ msgs.image } /><br/><strong>{ msgs.name }: </strong>
                                <Linkify>{ msgs.text }</Linkify></span><br/>
                            <span id="time">{ msgs.time }</span><br/>
                            </li>})
                }
            </ul>
        </div>
        );
}