var pairs =
{
"architecture":{"p2mp":1}
,"p2mp":{"lsp":1,"tunnel":1}
,"lsp":{"processing":1,"source-to-leaf":1}
,"processing":{"transport":1}
,"transport":{"path":1}
,"path":{"hierarchy":1}
,"hierarchy":{"p2mp":1}
,"tunnel":{"p2mp":1}
,"source-to-leaf":{"(s2l)":1}
,"(s2l)":{"sub-lsp":1}
}
;Search.control.loadWordPairs(pairs);
