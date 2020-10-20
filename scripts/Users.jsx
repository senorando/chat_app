import React, { useState, useEffect } from 'react';

import { Socket } from './Socket';

export function Users(props) {
    const currUsr = props.user_info
    const [users, setUsers] = useState([]);
    const [numUsers, updateNum] = useState();
    
    function getUsers() {
        useEffect(() => {
            Socket.on('active users', (data) => {
                setUsers(data['activeUsers']);
                updateNum(data['numUsers']);
                });
            Socket.off('active users', '');
        });
    }
    getUsers();
    function usersOn() {
        if(numUsers % 2 == 1) {
            return <h4 id="actives">You're the only user online :(</h4>;
        }else{
            return <h4 id="actives"><strong>{ numUsers }</strong> Online Users</h4>;
        }
    }
    let head = usersOn();
    return (
            <div className="active_user">
                { head }
                <ul id="user_list">
                    {users.map(( users, index ) => {
                        if(currUsr == users)
                            return <li id="people"
                                    key={ index }
                                    index={ index }>
                                    <i>You: { users }</i></li>;
                        else
                            return <li id="people"
                                    key={ index }
                                    index={ index }>
                                    { users }</li>;})
                    }
                </ul>
            </div>
        );
}