var pairs =
{
"ldp":{"traps":1,"includes":1}
,"traps":{"chapter":1,"ldp":1,"ldptrapsessionup":1}
,"chapter":{"contains":1}
,"contains":{"traps":1}
,"includes":{"following":1}
,"following":{"traps":1}
,"ldptrapsessionup":{"ldptrapsessiondown":1}
,"ldptrapsessiondown":{"ldptrapentityinitsesthreshold":1}
}
;Search.control.loadWordPairs(pairs);
