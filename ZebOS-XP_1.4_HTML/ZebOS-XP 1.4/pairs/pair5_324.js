var pairs =
{
"configure":{"pim":1,"terminal":1,"mode":1}
,"pim":{"router-id":1,"routers":1,"domain":1}
,"router-id":{"configure":1,"pim":1,"1.1.1.1":1,"(config)":1}
,"routers":{"inside":1}
,"inside":{"pim":1}
,"domain":{"configure":1}
,"terminal":{"enter":1}
,"enter":{"configure":1}
,"mode":{"(config)":1}
,"(config)":{"pim":1,"exit":1}
,"1.1.1.1":{"configure":1}
,"exit":{"exit":1,"configure":1}
}
;Search.control.loadWordPairs(pairs);
