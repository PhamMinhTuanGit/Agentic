var pairs =
{
"port":{"mirroring":1,"monitoring":1,"hal_msg_l2_pmirror_unset":1}
,"mirroring":{"messages":1,"hal_msg_l2_pmirror_deinit":1,"hal_msg_l2_pmirror_set":1,"port":1}
,"messages":{"message":1}
,"message":{"message":1,"hal_msg_l2_pmirror_init":1}
,"hal_msg_l2_pmirror_init":{"initialize":1}
,"initialize":{"mirroring":1}
,"hal_msg_l2_pmirror_deinit":{"de-initialize":1}
,"de-initialize":{"mirroring":1}
,"hal_msg_l2_pmirror_set":{"enable":1}
,"enable":{"tx\u002Frx":1}
,"tx\u002Frx":{"mirroring":1}
,"monitoring":{"port":1}
,"hal_msg_l2_pmirror_unset":{"disable":1}
,"disable":{"tx\u002Frx":1}
}
;Search.control.loadWordPairs(pairs);
