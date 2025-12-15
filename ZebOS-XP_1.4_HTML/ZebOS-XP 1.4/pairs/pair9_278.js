var pairs =
{
"platform":{"abstraction":1}
,"abstraction":{"layer":1}
,"layer":{"interface":1,"(pal)":1}
,"interface":{"platform":1,"rip":1,"tcp\u002Fip":1}
,"(pal)":{"interface":1}
,"rip":{"interface":1}
,"tcp\u002Fip":{"stack":1}
,"stack":{"send":1}
,"send":{"receive":1}
,"receive":{"control":1}
,"control":{"packets":1}
}
;Search.control.loadWordPairs(pairs);
