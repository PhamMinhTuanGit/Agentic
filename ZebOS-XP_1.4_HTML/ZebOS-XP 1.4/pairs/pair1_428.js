var pairs =
{
"tunneling":{"commands":1,"interface":1}
,"commands":{"chapter":1,"tunneling":1}
,"chapter":{"contains":1}
,"contains":{"commands":1}
,"interface":{"tunnel":1}
,"tunnel":{"tunnel":1,"checksum":1,"destination":1,"dmac":1,"mode":1,"path-mtu-discovery":1,"source":1,"tos":1,"ttl":1}
,"checksum":{"tunnel":1}
,"destination":{"tunnel":1}
,"dmac":{"tunnel":1}
,"mode":{"tunnel":1,"ipv6ip":1}
,"ipv6ip":{"tunnel":1}
,"path-mtu-discovery":{"tunnel":1}
,"source":{"tunnel":1}
,"tos":{"tunnel":1}
}
;Search.control.loadWordPairs(pairs);
