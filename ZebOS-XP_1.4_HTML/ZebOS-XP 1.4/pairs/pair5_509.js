var pairs =
{
"validation":{"rbridge-traceroute":1}
,"rbridge-traceroute":{"8001":1}
,"8001":{"rbridge":1,"0x0000":1}
,"rbridge":{"incoming":1}
,"incoming":{"port":1}
,"port":{"outgoing":1,"next-hop_nickname":1}
,"outgoing":{"port":1}
,"next-hop_nickname":{"8001":1}
,"0x0000":{"egress":1}
,"egress":{"****traceroute":1}
,"****traceroute":{"complete":1}
}
;Search.control.loadWordPairs(pairs);
