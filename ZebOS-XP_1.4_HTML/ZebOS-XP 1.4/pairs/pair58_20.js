var pairs =
{
"snmp":{"restart":1,"label":1}
,"restart":{"ldp":1,"snmp":1}
,"ldp":{"command":1,"parameters":1}
,"command":{"restart":1,"syntax":1,"mode":1}
,"label":{"distribution":1}
,"distribution":{"protocol":1}
,"protocol":{"(ldp)":1}
,"(ldp)":{"command":1}
,"syntax":{"snmp":1}
,"parameters":{"none":1}
,"none":{"command":1}
,"mode":{"configure":1,"examples":1}
,"configure":{"mode":1}
,"examples":{"snmp":1}
}
;Search.control.loadWordPairs(pairs);
