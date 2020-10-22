import React, { useState, useEffect } from 'react';

import * as ReactDOM from 'react-dom';

import { Content } from './Content';
import { Users } from './Users';
import { Socket } from './Socket';

export function App() {
    const [userName, setName] = useState();
    const [currUsr, setUsr] = useState({ name: '', email: '', image: '', sid: '' });
    const name = currUsr.name;
    const email = currUsr.email;
    const image = currUsr.image;
    const sid = currUsr.sid;
    const [isLoggedIn, setStatus] = useState(false);    //
    
    function getNewUser() {
        useEffect(() => {
            Socket.on('set user', (data) => {
                if(data['sid'] == Socket.id){
                    console.log("Welcome: " + data['name'] + "\nEmail: " + data['email'] + "\nImage/: " + data['imgUrl']);
                    setUsr(prevState => {
                        return { 
                            name: data['name'], 
                            email: data['email'], 
                            image: data['imgUrl'], 
                            sid: data['sid'] 
                        };
                    });
                    setStatus(prevStatus => true);      //
                }
                setName(data['name']);
            });
            Socket.off('set user', '');
        });
    }
    getNewUser();
    return (
        <div>
            <h1 id="title">Not Discord</h1>
            <p id="welcome"> Welcome! <strong>{ name } </strong></p>
            <Users name={ name } 
                email={ email } 
                image={ image } 
                sid={ sid }/>
            <Content name={ name } 
                email={ email } 
                image={ image } 
                sid={ sid }
                isLoggedIn={ isLoggedIn }/>
        </div>
        );
    }
ReactDOM.render(<App />, document.getElementById('content'));