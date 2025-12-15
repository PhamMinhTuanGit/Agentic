var pairs =
{
"forwarding":{"command":1,"parameter":1,"forwarding":1,"parameters":1}
,"command":{"turn":1,"syntax":1,"mode":1}
,"turn":{"forwarding":1}
,"parameter":{"command":1}
,"syntax":{"forwarding":1}
,"parameters":{"none":1}
,"none":{"command":1}
,"mode":{"configure":1,"examples":1}
,"configure":{"mode":1,"terminal":1}
,"examples":{"configure":1}
,"terminal":{"(config)":1}
,"(config)":{"forwarding":1}
}
;Search.control.loadWordPairs(pairs);
