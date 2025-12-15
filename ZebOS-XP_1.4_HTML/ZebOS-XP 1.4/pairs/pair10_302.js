var pairs =
{
"show":{"snmp":1}
,"snmp":{"host":1,"trap":1}
,"host":{"command":1,"parameters":1}
,"command":{"display":1,"syntax":1,"mode":1}
,"display":{"snmp":1}
,"trap":{"hosts":1}
,"hosts":{"command":1}
,"syntax":{"show":1}
,"parameters":{"none":1}
,"none":{"command":1}
,"mode":{"exec":1,"examples":1}
,"exec":{"mode":1}
,"examples":{"show":1}
}
;Search.control.loadWordPairs(pairs);
