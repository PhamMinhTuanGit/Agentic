var pairs =
{
"topology":{"bidirectional":1}
,"bidirectional":{"tunnel":1}
,"tunnel":{"primary":1,"path":1}
,"primary":{"tunnel":1}
,"path":{"pe1":1}
,"pe1":{"(eth1)-------(e1)":1,"(eth0)-------(e2)":1}
,"(eth1)-------(e1)":{"(e3)-----(e3)":1}
,"(e3)-----(e3)":{"(e1)----(e1)":1}
,"(e1)----(e1)":{"pe2":1}
,"pe2":{"secondary":1}
,"secondary":{"tunnel":1}
,"(eth0)-------(e2)":{"(e4)-----(e4)":1}
,"(e4)-----(e4)":{"(e2)----(e2)":1}
,"(e2)----(e2)":{"pe2":1}
}
;Search.control.loadWordPairs(pairs);
