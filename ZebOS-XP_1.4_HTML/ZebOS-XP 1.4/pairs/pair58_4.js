var pairs =
{
"snmp":{"restart":1,"connectivity":1}
,"restart":{"cfm":1,"snmp":1}
,"cfm":{"command":1,"parameters":1}
,"command":{"restart":1,"syntax":1,"mode":1}
,"connectivity":{"fault":1}
,"fault":{"management":1}
,"management":{"(cfm)":1}
,"(cfm)":{"command":1}
,"syntax":{"snmp":1}
,"parameters":{"none":1}
,"none":{"command":1}
,"mode":{"configure":1,"examples":1}
,"configure":{"mode":1}
,"examples":{"snmp":1}
}
;Search.control.loadWordPairs(pairs);
