import React, { useState, useEffect } from 'react';

import { Socket } from './Socket';

export function Users() {
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
    
    return (
            <div className="active_user">
                <h4 id="actives"><strong>{ numUsers }</strong> Online Users</h4>
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