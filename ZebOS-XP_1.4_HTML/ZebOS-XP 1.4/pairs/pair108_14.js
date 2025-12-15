var pairs =
{
"customer":{"vlan":1}
,"vlan":{"(c-vlan)":1,"service":1,"(s-vlan)":1}
,"(c-vlan)":{"provider":1}
,"provider":{"bridging":1}
,"bridging":{"(pb)":1}
,"(pb)":{"frame":1}
,"frame":{"field":1}
,"field":{"identifies":1}
,"identifies":{"customer":1}
,"service":{"vlan":1}
,"(s-vlan)":{"called":1}
,"called":{"c-tag":1}
}
;Search.control.loadWordPairs(pairs);
