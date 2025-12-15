var pairs =
{
"configure":{"bgp4":1}
,"bgp4":{"distance":1}
,"distance":{"administrative":1,"bgp":1,"ipv6":1}
,"administrative":{"distance":1}
,"bgp":{"configured":1,"administrative":1}
,"configured":{"specific":1}
,"specific":{"address":1}
,"address":{"family":1}
,"family":{"example":1,"bgp4":1}
,"example":{"shows":1}
,"shows":{"configuring":1}
,"configuring":{"bgp":1}
,"ipv6":{"address":1}
}
;Search.control.loadWordPairs(pairs);
