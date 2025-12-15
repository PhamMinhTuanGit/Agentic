var pairs =
{
"validation":{"log":1}
,"log":{"using":1}
,"using":{"login":1}
,"login":{"virtual-router":1}
,"virtual-router":{"vr1":1}
,"vr1":{"vlan":1}
,"vlan":{"1.2":1}
,"1.2":{"address":1,"address.ping":1}
,"address":{"ping":1}
,"ping":{"vlan":1}
}
;Search.control.loadWordPairs(pairs);
