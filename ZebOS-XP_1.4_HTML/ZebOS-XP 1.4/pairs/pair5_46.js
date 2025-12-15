var pairs =
{
"intra-confederation":{"ebgp":1}
,"ebgp":{"ibgp":1,"peering":1}
,"ibgp":{"peering":1}
,"peering":{"zebos-xp":1,"considered":1,"terms":1}
,"zebos-xp":{"bgp_info_cmp":1}
,"bgp_info_cmp":{"ensures":1}
,"ensures":{"intra-confederation":1}
,"considered":{"ibgp":1}
,"terms":{"handling":1}
,"handling":{"local-prefix":1}
,"local-prefix":{"med":1}
,"med":{"next_hop":1}
}
;Search.control.loadWordPairs(pairs);
