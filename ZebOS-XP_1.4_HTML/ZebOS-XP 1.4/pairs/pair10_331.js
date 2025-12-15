var pairs =
{
"area":{"border":1,"interface":1,"ospf":1}
,"border":{"router":1}
,"router":{"example":1,"area":1,"(abr)":1}
,"example":{"shows":1}
,"shows":{"configuration":1}
,"configuration":{"area":1}
,"(abr)":{"interface":1}
,"interface":{"eth0":1,"eth1":1}
,"eth0":{"area":1}
,"eth1":{"area":1}
,"ospf":{"abr":1}
,"abr":{"topology":1}
}
;Search.control.loadWordPairs(pairs);
