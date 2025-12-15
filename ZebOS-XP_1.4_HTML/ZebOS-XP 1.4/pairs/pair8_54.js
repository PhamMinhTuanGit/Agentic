var pairs =
{
"show":{"physical-ring":1}
,"physical-ring":{"rtr1":1,"bridge":1}
,"rtr1":{"g8032":1}
,"g8032":{"physical-ring":1}
,"bridge":{"ring":1}
,"ring":{"==========bridge":1}
,"==========bridge":{"east":1}
,"east":{"eth1":1}
,"eth1":{"west":1}
,"west":{"eth2":1}
,"eth2":{"erp":1}
,"erp":{"inst":1}
,"inst":{":major":1}
}
;Search.control.loadWordPairs(pairs);
