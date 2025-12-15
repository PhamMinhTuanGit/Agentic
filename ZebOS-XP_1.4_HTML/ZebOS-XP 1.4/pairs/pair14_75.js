var pairs =
{
"802.1x":{"messages":1,"authentication":1}
,"messages":{"message":1}
,"message":{"message":1,"hal_msg_8021x_init":1}
,"hal_msg_8021x_init":{"initialize":1}
,"initialize":{"802.1x":1}
,"authentication":{"hal_msg_8021x_deinit":1,"hal_msg_8021x_port_state":1}
,"hal_msg_8021x_deinit":{"de-initialize":1}
,"de-initialize":{"802.1x":1}
,"hal_msg_8021x_port_state":{"port":1}
,"port":{"state":1}
,"state":{"(blocked\u002Fblocked":1}
,"(blocked\u002Fblocked":{"in\u002Fauthenticated)":1}
}
;Search.control.loadWordPairs(pairs);
