var pairs =
{
"(config)":{"exit":1}
,"exit":{"exit":1,"configure":1}
,"configure":{"mode":1}
,"mode":{"login":1}
,"login":{"virtual-router":1}
,"virtual-router":{"vr1":1}
,"vr1":{"log":1,"enable":1}
,"log":{"virtual-router":1}
,"enable":{"ping":1}
,"ping":{"2.2.2.1":1}
}
;Search.control.loadWordPairs(pairs);
