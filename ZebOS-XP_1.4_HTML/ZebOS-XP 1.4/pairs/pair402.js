var pairs =
{
"virtual":{"private":1}
,"private":{"network":1}
,"network":{"(vpn)":1,"service":1,"runs":1,"infrastructure":1}
,"(vpn)":{"network":1}
,"service":{"uses":1}
,"uses":{"encryption":1}
,"encryption":{"tunneling":1}
,"tunneling":{"provide":1}
,"provide":{"subscriber":1}
,"subscriber":{"secure":1}
,"secure":{"private":1}
,"runs":{"public":1}
,"public":{"network":1}
}
;Search.control.loadWordPairs(pairs);
