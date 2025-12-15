var pairs =
{
"hal":{"messages":1}
,"messages":{"following":1,"sent":1}
,"following":{"list":1}
,"list":{"hal":1}
,"sent":{"hsl":1}
,"hsl":{"hal_msg_dcb_pfc_disable":1}
,"hal_msg_dcb_pfc_disable":{"hal_msg_dcb_pfc_enable":1}
,"hal_msg_dcb_pfc_enable":{"hal_msg_dcb_pfc_if_enable":1}
,"hal_msg_dcb_pfc_if_enable":{"hal_msg_dcb_pfc_select_mode":1}
}
;Search.control.loadWordPairs(pairs);
