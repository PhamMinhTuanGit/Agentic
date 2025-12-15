var pairs =
{
"ldp":{"graceful":1,"reduces":1,"module":1}
,"graceful":{"restart":1}
,"restart":{"zebos-xp":1,"feature":1,"ldp":1}
,"zebos-xp":{"graceful":1}
,"feature":{"ldp":1}
,"reduces":{"impact":1}
,"impact":{"mpls":1}
,"mpls":{"forwarding":1}
,"forwarding":{"due":1}
,"due":{"restart":1}
}
;Search.control.loadWordPairs(pairs);
