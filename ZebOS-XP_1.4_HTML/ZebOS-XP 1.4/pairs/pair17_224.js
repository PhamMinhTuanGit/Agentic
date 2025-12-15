var pairs =
{
"host":{"configure":1}
,"configure":{"terminal":1,"mode":1,"address":1}
,"terminal":{"enter":1}
,"enter":{"configure":1,"interface":1}
,"mode":{"(config)":1,"eth1":1}
,"(config)":{"interface":1}
,"interface":{"eth1":1,"mode":1}
,"eth1":{"enter":1,"(config-if)":1,"network":1}
,"(config-if)":{"address":1}
,"address":{"1.1.1.5\u002F24":1,"interface":1}
,"1.1.1.5\u002F24":{"configure":1}
}
;Search.control.loadWordPairs(pairs);
