import React, { useState, useEffect } from 'react';

import * as ReactDOM from 'react-dom';

import { Content } from './Content';
import { Users } from './Users';
import { Socket } from './Socket';

export function App() {
    const [userName, setName] = useState();
    const [currUsr, setUsr] = useState();
    
    function getNewUser() {
        useEffect(() => {
            Socket.on('set user', (data) => {
                if(data['user_id'] == Socket.id){
                    console.log("New User: " + data['name'] + "\nSID: " + Socket.id);
                    setUsr(data['name']);
                }
                setName(data['name']);
            });
            Socket.off('set user', '');
        });
    }
    getNewUser();
    return (
        <div>
            <Content user_info={ currUsr } />
            <p id="username"> Welcome! Your name is: <strong>{ currUsr } </strong></p>
            <Users user_info={ currUsr }/>
        </div>
        );
    }
ReactDOM.render(<App />, document.getElementById('content'));