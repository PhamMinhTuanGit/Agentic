var pairs =
{
"data":{"terminal":1,"communications":1}
,"terminal":{"equipment":1}
,"equipment":{"(dte)":1,"(dce)":1}
,"(dte)":{"device":1}
,"device":{"host":1}
,"host":{"router":1}
,"router":{"switch":1}
,"switch":{"connected":1}
,"connected":{"network":1}
,"network":{"dte":1,"data":1}
,"dte":{"connects":1}
,"connects":{"network":1}
,"communications":{"equipment":1}
}
;Search.control.loadWordPairs(pairs);
