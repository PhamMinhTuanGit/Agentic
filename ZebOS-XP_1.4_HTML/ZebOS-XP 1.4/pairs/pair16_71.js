var pairs =
{
"interface":{"table":1,"information":1}
,"table":{"interface":1,"belongs":1}
,"information":{"stored":1}
,"stored":{"is-is":1,"table":1}
,"is-is":{"interface":1,"instance":1,"enabled":1}
,"belongs":{"is-is":1}
,"instance":{"is-is":1}
,"enabled":{"interfaces":1}
,"interfaces":{"stored":1}
}
;Search.control.loadWordPairs(pairs);
