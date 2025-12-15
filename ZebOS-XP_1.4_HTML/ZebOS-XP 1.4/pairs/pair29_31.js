var pairs =
{
"snmp":{"restart":1,"authentication":1}
,"restart":{"auth":1,"snmp":1}
,"auth":{"command":1,"parameters":1}
,"command":{"restart":1,"syntax":1,"mode":1}
,"authentication":{"command":1}
,"syntax":{"snmp":1}
,"parameters":{"none":1}
,"none":{"command":1}
,"mode":{"configure":1,"examples":1}
,"configure":{"mode":1}
,"examples":{"snmp":1}
}
;Search.control.loadWordPairs(pairs);
