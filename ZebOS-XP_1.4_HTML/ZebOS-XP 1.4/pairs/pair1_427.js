var pairs =
{
"control":{"adjacency":1}
,"adjacency":{"commands":1,"mode":1}
,"commands":{"commands":1,"chapter":1,"control-adjacency":1}
,"chapter":{"issued":1}
,"issued":{"control":1}
,"mode":{"includes":1}
,"includes":{"following":1}
,"following":{"commands":1}
,"control-adjacency":{"description":1,"show":1,"te-link":1}
,"description":{"show":1}
,"show":{"control-adjacency":1,"running-config":1}
,"running-config":{"control-adjacency":1}
}
;Search.control.loadWordPairs(pairs);
