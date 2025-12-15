var pairs =
{
"authentication":{"messages":1,"status":1,"state":1,"port":1}
,"messages":{"message":1}
,"message":{"constant":1,"nsm":1}
,"constant":{"source":1}
,"source":{"nsm_msg_auth_mac_auth_status":1}
,"nsm_msg_auth_mac_auth_status":{"send":1}
,"send":{"mac":1,"port":1}
,"mac":{"authentication":1}
,"status":{"message":1}
,"nsm":{"nsm_msg_auth_port_state":1,"nsm_msg_macauth_port_state":1}
,"nsm_msg_auth_port_state":{"send":1}
,"port":{"authentication":1,"state":1}
,"state":{"message":1}
,"nsm_msg_macauth_port_state":{"send":1}
}
;Search.control.loadWordPairs(pairs);
