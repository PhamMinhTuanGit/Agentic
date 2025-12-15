var pairs =
{
"bind":{"customer":1}
,"customer":{"interface":1}
,"interface":{"attach":1,"layer":1}
,"attach":{"customer":1}
,"layer":{"vcs":1,"interfaces":1}
,"vcs":{"bound":1}
,"bound":{"layer":1}
,"interfaces":{"encapsulation":1}
,"encapsulation":{"ethernet":1}
,"ethernet":{"(default)":1}
,"(default)":{"vlan":1}
,"vlan":{"hdlc":1}
,"hdlc":{"ppp":1}
}
;Search.control.loadWordPairs(pairs);
