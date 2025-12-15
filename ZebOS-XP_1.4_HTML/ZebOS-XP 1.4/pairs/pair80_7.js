var pairs =
{
"snmp":{"restart":1,"intermediate":1}
,"restart":{"isis":1,"snmp":1}
,"isis":{"command":1,"parameters":1}
,"command":{"restart":1,"syntax":1,"mode":1}
,"intermediate":{"system":1}
,"system":{"intermediate":1,"(is-is)":1}
,"(is-is)":{"command":1}
,"syntax":{"snmp":1}
,"parameters":{"none":1}
,"none":{"command":1}
,"mode":{"configure":1,"examples":1}
,"configure":{"mode":1}
,"examples":{"snmp":1}
}
;Search.control.loadWordPairs(pairs);
