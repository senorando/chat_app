import React, { useState, useEffect } from 'react';
import * as ReactDOM from 'react-dom';

import { Content } from './Content';
import { Users } from './Users';
import { Socket } from './Socket';

export function App() {
    const [user_info, setInfo] = useState("");
    function getInfo() {
        useEffect(() => {
            Socket.on('Connected', (data) => {
                if(data[2].sess_id == Socket.id) {
                    const username = data[3].name;
                    setInfo(username);
                }
            });
            return () => {
                Socket.off('Disconnected', "")
            }
        });
    }
    getInfo();
    return (
        <div>
            <Content user_info={ user_info } />
            <p id="username"> Here's your alias TODO{ user_info } </p>
            <Users />
        </div>
        );
    }
ReactDOM.render(<App />, document.getElementById('content'));
