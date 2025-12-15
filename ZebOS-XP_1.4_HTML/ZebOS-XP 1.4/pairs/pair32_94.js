var pairs =
{
"address":{"resolution":1,"entity":1,"domain":1}
,"resolution":{"process":1,"protocol":1}
,"process":{"translating":1}
,"translating":{"address":1}
,"entity":{"system":1}
,"system":{"equivalent":1,"instance":1}
,"equivalent":{"address":1}
,"instance":{"translating":1}
,"domain":{"name":1}
,"name":{"service":1,"address":1}
,"service":{"(dns)":1}
,"(dns)":{"name":1}
,"protocol":{"(arp)":1}
}
;Search.control.loadWordPairs(pairs);
