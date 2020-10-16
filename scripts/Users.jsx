import React, { useState, useEffect } from 'react';

import { Socket } from './Socket';

export function Users() {
    const [users, setUsers] = useState([]);
    
    function getUsers() {
        useEffect(() => {
            Socket.on('users received', (data) => { 
                console.log(data);
                const user_name = data;
                // setUsers(user_name);
                // console.log("New User: " + user_name);
                });
        });
    }
    getUsers();
    
    return (
            <div className="active_user">
                <h4 id="actives"> Online Users</h4>
                <ol id="user_list">
                    {users.map(( users, index ) => (
                        <li id="people"
                            key={ index }
                            index={ index }>
                            { users }
                        </li>
                    ))}
                </ol>
            </div>
        );
}