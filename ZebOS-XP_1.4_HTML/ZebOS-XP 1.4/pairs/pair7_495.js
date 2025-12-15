var pairs =
{
"leave":{"lsr":1}
,"lsr":{"command":1}
,"command":{"switch":1,"syntax":1,"mode":1}
,"switch":{"back":1}
,"back":{"default":1}
,"default":{"lsr":1}
,"syntax":{"leave":1}
,"mode":{"configure":1,"example":1}
,"configure":{"mode":1}
,"example":{"leave":1}
}
;Search.control.loadWordPairs(pairs);
