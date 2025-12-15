var pairs =
{
"bgp":{"speaker":1,"peers":1}
,"speaker":{"router":1,"explicitly":1}
,"router":{"configured":1}
,"configured":{"run":1,"bgp":1}
,"run":{"border":1}
,"border":{"gateway":1}
,"gateway":{"protocol":1}
,"protocol":{"(bgp)":1,"bgp":1}
,"(bgp)":{"routing":1}
,"routing":{"protocol":1,"information":1}
,"explicitly":{"configured":1}
,"peers":{"exchanges":1}
,"exchanges":{"routing":1}
}
;Search.control.loadWordPairs(pairs);
