var pairs =
{
"1:1":{"co-routed":1,"bidirectional":1}
,"co-routed":{"bidirectional":1}
,"bidirectional":{"linear":1,"protection":1}
,"linear":{"protection":1}
,"protection":{"switching":1,"scheme":1}
,"switching":{"pseudowire":1}
,"pseudowire":{"ipv4":1}
,"ipv4":{"map":1}
,"map":{"route":1}
,"route":{"traffic":1}
,"traffic":{"supported":1}
,"supported":{"1:1":1}
}
;Search.control.loadWordPairs(pairs);
