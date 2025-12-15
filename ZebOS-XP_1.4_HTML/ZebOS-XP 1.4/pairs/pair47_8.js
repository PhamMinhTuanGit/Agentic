var pairs =
{
"customer":{"network":1}
,"network":{"ports":1}
,"ports":{"group":1,"(cnps)":1}
,"group":{"group":1,"contains":1,"zebos-xp-specific":1}
,"contains":{"configuration":1}
,"configuration":{"settings":1}
,"settings":{"customer":1}
,"(cnps)":{"bridge":1}
,"bridge":{"group":1}
,"zebos-xp-specific":{"part":1}
,"part":{"standard":1}
}
;Search.control.loadWordPairs(pairs);
