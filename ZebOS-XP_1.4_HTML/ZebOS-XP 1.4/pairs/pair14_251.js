var pairs =
{
"redistribute":{"routes":1}
,"routes":{"ospfv3":1,"imported":1}
,"ospfv3":{"example":1,"redistribute":1}
,"example":{"bgp":1}
,"bgp":{"routes":1}
,"imported":{"ospf":1}
,"ospf":{"routing":1}
,"routing":{"table":1}
,"table":{"advertised":1}
,"advertised":{"type":1}
,"type":{"external":1}
,"external":{"lsas":1}
,"lsas":{"area":1}
,"area":{"ospfv3":1}
}
;Search.control.loadWordPairs(pairs);
