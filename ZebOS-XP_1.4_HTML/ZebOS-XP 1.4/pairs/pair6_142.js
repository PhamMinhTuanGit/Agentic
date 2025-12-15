var pairs =
{
"mstp":{"messages":1,"bridge":1}
,"messages":{"message":1}
,"message":{"message":1,"hal_msg_bridge_add_instance":1}
,"hal_msg_bridge_add_instance":{"add":1}
,"add":{"mstp":1,"vlan":1}
,"bridge":{"instance":1}
,"instance":{"hal_msg_bridge_delete_instance":1,"hal_msg_bridge_add_vlan_to_instance":1,"hal_msg_bridge_delete_vlan_from_instance":1}
,"hal_msg_bridge_delete_instance":{"remove":1}
,"remove":{"mstp":1,"vlan":1}
,"hal_msg_bridge_add_vlan_to_instance":{"add":1}
,"vlan":{"instance":1}
,"hal_msg_bridge_delete_vlan_from_instance":{"remove":1}
}
;Search.control.loadWordPairs(pairs);
