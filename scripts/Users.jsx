import React, { useState, useEffect } from 'react';

import { Socket } from './Socket';

export function Users() {
    const [users, setUsers] = useState([]);
    
    function numUsers() {
        useEffect(() => {
            Socket.on('User Received', (data) => { setUsers(data); });
        });
    }
    numUsers();
    
    return (
            <div className="active_user">
                <h4 id="actives"> Online Users TODO</h4>
                <ol id="user_list">
                    {users.map(( users, index ) => (
                        <li id="people"
                            key={ index }
                            index={ index }>
                            { users.name }
                        </li>
                    ))}
                </ol>
            </div>
        );
}