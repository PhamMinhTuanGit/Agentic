var pairs =
{
"topology":{"network":1,"source":1}
,"network":{"topology":1}
,"source":{"address":1}
,"address":{"172.31.1.52":1,"224.0.1.3":1}
,"172.31.1.52":{"group":1}
,"group":{"address":1}
,"224.0.1.3":{"pim":1}
,"pim":{"ecmp":1}
,"ecmp":{"redirect":1}
,"redirect":{"topology":1}
}
;Search.control.loadWordPairs(pairs);
