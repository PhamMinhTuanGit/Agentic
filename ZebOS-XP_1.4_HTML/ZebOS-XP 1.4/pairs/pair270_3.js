var pairs =
{
"network":{"element":1,"host":1}
,"element":{"(ne)":1}
,"(ne)":{"device":1}
,"device":{"network":1}
,"host":{"router":1}
,"router":{"switch":1}
,"switch":{"firewall":1}
,"firewall":{"performs":1}
,"performs":{"service":1}
,"service":{"function":1}
,"function":{"network":1}
}
;Search.control.loadWordPairs(pairs);
