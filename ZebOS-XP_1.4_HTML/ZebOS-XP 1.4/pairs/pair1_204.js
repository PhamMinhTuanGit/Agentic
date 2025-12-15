var pairs =
{
"vlog":{"commands":1,"show":1,"clients":1,"terminals":1,"virtual-routers":1}
,"commands":{"chapter":1,"reset":1}
,"chapter":{"describes":1}
,"describes":{"virtual":1}
,"virtual":{"router":1}
,"router":{"log":1}
,"log":{"(vlog)":1,"file":1}
,"(vlog)":{"commands":1}
,"reset":{"log":1}
,"file":{"show":1}
,"show":{"vlog":1}
,"clients":{"show":1}
,"terminals":{"show":1}
}
;Search.control.loadWordPairs(pairs);
