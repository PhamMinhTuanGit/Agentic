var pairs =
{
"configure":{"terminal":1,"mode":1,"ospf":1}
,"terminal":{"enter":1}
,"enter":{"configure":1}
,"mode":{"(config)":1,"return":1}
,"(config)":{"router":1}
,"router":{"ospf":1,"mode":1}
,"ospf":{"configure":1,"instance":1,"area":1}
,"instance":{"instance":1,"(config-router)":1}
,"(config-router)":{"network":1,"exit":1}
,"network":{"3.3.3.0":1}
,"3.3.3.0":{"area":1}
,"area":{"configure":1,"(config-router)":1}
,"exit":{"exit":1,"router":1}
,"return":{"configure":1}
}
;Search.control.loadWordPairs(pairs);
