var pairs =
{
"mpls-tp":{"label":1}
,"label":{"switched":1}
,"switched":{"path":1}
,"path":{"tunnel":1,"(lsp)":1}
,"tunnel":{"contain":1}
,"contain":{"primary":1,"following":1}
,"primary":{"label":1}
,"(lsp)":{"(backup":1}
,"(backup":{"lsps":1}
,"lsps":{"supported":1,"contain":1}
,"supported":{"future":1}
,"future":{"release.)":1}
,"release.)":{"lsps":1}
,"following":{"information":1}
}
;Search.control.loadWordPairs(pairs);
