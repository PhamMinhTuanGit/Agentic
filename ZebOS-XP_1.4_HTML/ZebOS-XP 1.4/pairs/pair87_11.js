var pairs =
{
"snmp":{"restart":1,"ospf":1}
,"restart":{"ospf":1,"snmp":1}
,"ospf":{"command":1,"parameter":1}
,"command":{"restart":1,"syntax":1,"mode":1}
,"syntax":{"snmp":1}
,"parameter":{"none":1}
,"none":{"command":1}
,"mode":{"configure":1,"examples":1}
,"configure":{"mode":1}
,"examples":{"snmp":1}
}
;Search.control.loadWordPairs(pairs);
