var pairs =
{
"network":{"segment":1,"separated":1,"device":1}
,"segment":{"portion":1,"contain":1}
,"portion":{"computer":1}
,"computer":{"network":1}
,"separated":{"rest":1}
,"rest":{"network":1}
,"device":{"router":1}
,"router":{"switch":1}
,"switch":{"segment":1}
,"contain":{"hosts":1}
}
;Search.control.loadWordPairs(pairs);
