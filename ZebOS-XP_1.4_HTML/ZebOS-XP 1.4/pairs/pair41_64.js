var pairs =
{
"is-is":{"distance":1,"configured":1,"administrative":1}
,"distance":{"administrative":1,"is-is":1,"ipv4":1,"topology":1}
,"administrative":{"distance":1}
,"configured":{"specified":1}
,"specified":{"source":1}
,"source":{"routes":1}
,"routes":{"example":1}
,"example":{"shows":1}
,"shows":{"configuring":1}
,"configuring":{"is-is":1}
,"ipv4":{"address":1}
,"address":{"family":1}
,"family":{"is-is":1}
}
;Search.control.loadWordPairs(pairs);
