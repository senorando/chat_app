import React, { useEffect } from 'react';
import { animateScroll } from 'react-scroll';
import Linkify from 'react-linkify';

export function Chatbox(props) {
  const msgs = props.chatLog;

  function scroll() {
    animateScroll.scrollToBottom({
      containerId: 'msg_list',
    });
  }
  function checkPIC(url) {
    return (url.toLowerCase().match(/\.(jpeg|jpg|gif|png)$/) != null);
  }

  useEffect(() => { scroll(); });
  return (
    <div
      id="logs"
      className="chat"
    >
      <ul id="msg_list">
        {msgs.map((msgs, index) => {
          if (msgs.email === props.email) {
            return (
              <li id="self" key={index}>
                <span id="msgs">
                  {checkPIC(msgs.text)
                    ? <img id="sent_img" src={msgs.text} alt={msgs.text} />
                    : <Linkify>{ msgs.text }</Linkify>}
                </span>
                <br />
                <span id="time">{ msgs.time }</span>
                
              </li>
            );
          }
          return (
            <li id={msgs.name.valueOf() === 'BimboBOT' ? 'chat_bot' : 'others'} key={index}>
              { msgs.email !== msgs.prev_email? 
                <div id="msg_head" className={msgs.name.valueOf() === 'BimboBOT' ? 'chat_bot' : 'others'}>
                  <div id="msg_img"><img className="prof_pic" src={msgs.image} alt="prof_pic" /></div>
                  <div id="msg_name">
                    <strong>
                      { msgs.name }
                      {' '}
                    </strong>
                    
                  </div>
                  <br/>
                </div>
                :
                <div id="fake_head" className={msgs.name.valueOf() === 'BimboBOT' ? 'chat_bot' : 'others'}></div>
              }
                
                <div id={msgs.name.valueOf() === 'BimboBOT' ? 'chat_bot_cont' : 'others_cont'}>
                {checkPIC(msgs.text)?
                   <img id="sent_img" src={msgs.text} alt={msgs.text} />
                  : <Linkify>{ msgs.text }</Linkify>}
                  <br />
                <span id="time">{ msgs.time }</span>
                </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
