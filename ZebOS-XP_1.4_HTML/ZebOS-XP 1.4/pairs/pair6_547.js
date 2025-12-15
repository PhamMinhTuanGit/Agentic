var pairs =
{
"log":{"system":1,"send":1,"syslog":1}
,"system":{"log":1,"logging":1}
,"send":{"debugging":1}
,"debugging":{"output":1}
,"output":{"syslog":1}
,"syslog":{"log":1,"command":1,"form":1}
,"command":{"(config)":1,"turn":1}
,"(config)":{"log":1}
,"form":{"command":1}
,"turn":{"system":1}
,"logging":{"(config)":1}
}
;Search.control.loadWordPairs(pairs);
