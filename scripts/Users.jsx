import React, { useState, useEffect } from 'react';
import Linkify from 'react-linkify';

import { Socket } from './Socket';

export function Users(props) {
    const currUsr = { 
        'name': props.name,
        'image': props.image,
        'email': props.email
    };
    const [users, setUsers] = useState([]);
    const [numUsers, setNum] = useState(0);
    
    function getUsers() {
        useEffect(() => {
            Socket.on('active users', (data) => {
                setUsers(data['activeUsers']);
                setNum(data['numUsers']);
                console.log(data['numUsers'] + " Active Users");
                });
            Socket.off('active users', '');
        });
    }
    getUsers();
    const Current_User_el = <span id="names_me">
                                <div id="prof_pic"><img src={ users['imgUrl'] } /></div>
                                <div id="actives">
                                    <i>{ users['name'] }<br/>
                                        <Linkify id="emails">{ users['email'] }</Linkify>
                                    </i>
                                </div>
                            </span>;
    const Other_User_el = <span id="names_others">
                            <div id="prof_pic">
                                <img id="prof_pic" src={ users['imgUrl'] } />
                            </div>
                            <div id="actives">
                                { users['name'] }<br/>
                                <Linkify id="emails">
                                    { users['email'] }
                                </Linkify>
                            </div>
                           </span>
    return (
            <div className="active_user">
                
                <ul id="user_list">
                    <li><h4 id="actives"><strong>{ numUsers }</strong> Online Users</h4></li>
                    {users.map(( users, index ) => {
                        if(currUsr['email'] == users['email'] && currUsr['email'] != "")
                            return <li id="users"
                                    key={ index }
                                    index={ index }>
                                        <span id="names_me">
                                            <div id="prof_pic"><img src={ users['imgUrl'] } /></div>
                                            <div id="actives">
                                                <i>{ users['name'] }<br/>
                                                <Linkify id="emails">{ users['email'] }</Linkify>
                                                </i>
                                            </div>
                                        </span>
                                    </li>;
                        else
                            return <li id={ users['email'] == " "? "bot" : "users"}
                                    key={ index }
                                    index={ index }>
                                        <span id={ users['email'] == " "? "names_bot" : "names_others"}>
                                            <div id="prof_pic">
                                                <img id="prof_pic" src={ users['imgUrl'] } />
                                            </div>
                                            <div id="actives">
                                                { users['name'] }<br/>
                                                <Linkify id="emails">
                                                    { users['email'] }
                                                </Linkify>
                                            </div>
                                        </span>
                                    </li>;})
                    }
                </ul>
            </div>
        );
}