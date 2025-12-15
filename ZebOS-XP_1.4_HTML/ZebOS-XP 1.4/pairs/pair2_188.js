var pairs =
{
"hal":{"initialization":1}
,"initialization":{"messages":1,"message":1}
,"messages":{"message":1}
,"message":{"message":1,"hal_msg_init":1,"hal_msg_deinit":1}
,"hal_msg_init":{"global":1}
,"global":{"hardware":1}
,"hardware":{"sdk":1}
,"sdk":{"initialization":1,"deinitialization":1}
,"hal_msg_deinit":{"global":1}
,"deinitialization":{"message":1}
}
;Search.control.loadWordPairs(pairs);
