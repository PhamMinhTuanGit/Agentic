var pairs =
{
"bfd":{"mpls":1,"configuration":1}
,"mpls":{"lsps":1}
,"lsps":{"chapter":1}
,"chapter":{"provides":1}
,"provides":{"bfd":1}
,"configuration":{"information":1}
,"information":{"multi-protocol":1}
,"multi-protocol":{"label":1}
,"label":{"switched":1}
,"switched":{"(mpls)":1,"paths":1}
,"(mpls)":{"label":1}
,"paths":{"(lsps)":1}
}
;Search.control.loadWordPairs(pairs);
