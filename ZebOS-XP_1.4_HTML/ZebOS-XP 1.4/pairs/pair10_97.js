var pairs =
{
"igmp":{"snooping":1}
,"snooping":{"messages":1,"hal_msg_igmp_snooping_deinit":1,"hal_msg_igmp_snooping_enable":1,"port":1}
,"messages":{"message":1}
,"message":{"message":1,"hal_msg_igmp_snooping_init":1}
,"hal_msg_igmp_snooping_init":{"initialize":1}
,"initialize":{"igmp":1}
,"hal_msg_igmp_snooping_deinit":{"de-initialize":1}
,"de-initialize":{"igmp":1}
,"hal_msg_igmp_snooping_enable":{"enable":1}
,"enable":{"igmp":1}
,"port":{"hal_msg_igmp_snooping_disable":1}
,"hal_msg_igmp_snooping_disable":{"disable":1}
,"disable":{"igmp":1}
}
;Search.control.loadWordPairs(pairs);
