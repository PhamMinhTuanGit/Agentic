var pairs =
{
"mpls":{"layer-3":1}
,"layer-3":{"vpn":1,"virtual":1}
,"vpn":{"configurations":1}
,"configurations":{"chapter":1,"mpls":1}
,"chapter":{"contains":1}
,"contains":{"configurations":1}
,"virtual":{"private":1}
,"private":{"networks":1}
,"networks":{"(vpns)":1}
}
;Search.control.loadWordPairs(pairs);
