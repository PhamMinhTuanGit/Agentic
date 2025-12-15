var pairs =
{
"multicast":{"route":1,"routing":1,"groups":1}
,"route":{"table":1}
,"table":{"table":1,"contains":1}
,"contains":{"multicast":1}
,"routing":{"information":1}
,"information":{"datagrams":1}
,"datagrams":{"sent":1}
,"sent":{"particular":1}
,"particular":{"sources":1}
,"sources":{"multicast":1}
,"groups":{"known":1}
,"known":{"router":1}
}
;Search.control.loadWordPairs(pairs);
