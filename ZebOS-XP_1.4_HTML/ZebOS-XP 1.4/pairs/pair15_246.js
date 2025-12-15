var pairs =
{
"snmp":{"restart":1,"routing":1}
,"restart":{"rib":1,"snmp":1}
,"rib":{"command":1,"parameters":1}
,"command":{"restart":1,"syntax":1,"mode":1}
,"routing":{"information":1}
,"information":{"base":1}
,"base":{"(rib)":1}
,"(rib)":{"command":1}
,"syntax":{"snmp":1}
,"parameters":{"none":1}
,"none":{"command":1}
,"mode":{"configure":1,"examples":1}
,"configure":{"mode":1}
,"examples":{"snmp":1}
}
;Search.control.loadWordPairs(pairs);
