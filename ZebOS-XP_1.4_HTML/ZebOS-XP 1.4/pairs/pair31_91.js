var pairs =
{
"configure":{"is-is":1}
,"is-is":{"ipv6":1,"administrative":1}
,"ipv6":{"distance":1,"address":1}
,"distance":{"administrative":1,"configured":1,"ipv6":1}
,"administrative":{"distance":1}
,"configured":{"is-is":1}
,"address":{"family":1}
,"family":{"example":1,"is-isv6":1}
,"example":{"shows":1}
,"shows":{"configuring":1}
,"configuring":{"is-is":1}
,"is-isv6":{"distance":1}
}
;Search.control.loadWordPairs(pairs);
