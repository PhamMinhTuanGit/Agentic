var pairs =
{
"ip-ip":{"tunneling":1,"tunnels":1}
,"tunneling":{"mpls":1}
,"mpls":{"chapter":1,"details":1}
,"chapter":{"contains":1}
,"contains":{"configuration":1}
,"configuration":{"ip-ip":1}
,"tunnels":{"mpls":1}
,"details":{"commands":1}
,"commands":{"network":1}
,"network":{"services":1}
,"services":{"module":1}
,"module":{"command":1}
,"command":{"reference":1}
}
;Search.control.loadWordPairs(pairs);
