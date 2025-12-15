var pairs =
{
"route":{"redistribution":1,"leakage":1}
,"redistribution":{"protocol":1,"route":1}
,"protocol":{"learning":1,"running":1}
,"learning":{"routes":1}
,"routes":{"protocol":1}
,"running":{"device":1}
,"device":{"called":1}
,"called":{"redistribution":1}
}
;Search.control.loadWordPairs(pairs);
