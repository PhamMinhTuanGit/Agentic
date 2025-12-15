var pairs =
{
"disabling":{"master":1}
,"master":{"configure":1}
,"configure":{"terminal":1,"mode":1}
,"terminal":{"enter":1}
,"enter":{"configure":1,"interface":1}
,"mode":{"(config)":1,"eth0":1}
,"(config)":{"interface":1}
,"interface":{"eth0":1,"mode":1}
,"eth0":{"enter":1,"(config-router)":1}
,"(config-router)":{"shutdown":1}
,"shutdown":{"shut":1}
,"shut":{"down":1}
,"down":{"interface":1}
}
;Search.control.loadWordPairs(pairs);
