var pairs =
{
"igmp":{"mib":1,"interface":1,"enabled":1}
,"mib":{"table":1}
,"table":{"igmp":1,"contains":1}
,"interface":{"table":1,"igmp":1}
,"contains":{"row":1}
,"row":{"interface":1}
}
;Search.control.loadWordPairs(pairs);
