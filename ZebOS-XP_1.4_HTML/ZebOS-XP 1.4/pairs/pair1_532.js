var pairs =
{
"network":{"services":1}
,"services":{"module":1}
,"module":{"network":1,"(nsm)":1,"messages":1}
,"(nsm)":{"sends":1}
,"sends":{"unsolicited":1}
,"unsolicited":{"messages":1}
,"messages":{"receives":1,"qos":1,"structures":1}
,"receives":{"unsolicited":1}
,"qos":{"(quality":1}
,"(quality":{"service)":1}
,"service)":{"module":1}
,"structures":{"discussed":1}
,"discussed":{"below":1}
}
;Search.control.loadWordPairs(pairs);
