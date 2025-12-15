var pairs =
{
"igmp":{"cache":1}
,"cache":{"mib":1,"table":1}
,"mib":{"table":1}
,"table":{"igmp":1,"contains":1}
,"contains":{"row":1}
,"row":{"multicast":1}
,"multicast":{"group":1}
,"group":{"members":1}
,"members":{"particular":1}
,"particular":{"interface":1}
}
;Search.control.loadWordPairs(pairs);
