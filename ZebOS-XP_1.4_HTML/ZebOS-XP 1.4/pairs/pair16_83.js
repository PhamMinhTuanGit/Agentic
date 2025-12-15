var pairs =
{
"snmp":{"restart":1,"lacp":1}
,"restart":{"lacp":1,"snmp":1}
,"lacp":{"command":1,"parameters":1}
,"command":{"restart":1,"syntax":1,"mode":1}
,"syntax":{"snmp":1}
,"parameters":{"none":1}
,"none":{"command":1}
,"mode":{"configure":1,"examples":1}
,"configure":{"mode":1}
,"examples":{"(config)":1}
,"(config)":{"snmp":1}
}
;Search.control.loadWordPairs(pairs);
