var pairs =
{
"asbrs":{"configuration":1,"using":1}
,"configuration":{"steps":1}
,"steps":{"asbr":1}
,"asbr":{"asbrs":1,"configured":1}
,"using":{"ebgp":1}
,"ebgp":{"except":1}
,"except":{"asbr":1}
,"configured":{"igbp":1}
,"igbp":{"peer":1}
,"peer":{"instead":1}
}
;Search.control.loadWordPairs(pairs);
