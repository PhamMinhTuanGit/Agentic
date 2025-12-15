var pairs =
{
"redistribute":{"routes":1}
,"routes":{"is-is":1,"imported":1,"is-isv6":1}
,"is-is":{"example":1,"routing":1}
,"example":{"configuration":1}
,"configuration":{"causes":1}
,"causes":{"bgp":1}
,"bgp":{"routes":1}
,"imported":{"is-is":1}
,"routing":{"table":1}
,"table":{"advertised":1}
,"advertised":{"ipi":1}
,"ipi":{"instance":1}
,"instance":{"redistribute":1}
}
;Search.control.loadWordPairs(pairs);
