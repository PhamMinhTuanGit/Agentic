var pairs =
{
"clear":{"clns":1}
,"clns":{"neighbors":1,"neighbor":1}
,"neighbors":{"command":1,"parameters":1}
,"command":{"clear":1,"syntax":1,"mode":1}
,"neighbor":{"adjacencies":1}
,"adjacencies":{"command":1}
,"syntax":{"clear":1}
,"parameters":{"none":1}
,"none":{"command":1}
,"mode":{"exec":1,"privileged":1,"example":1}
,"exec":{"mode":1}
,"privileged":{"exec":1}
,"example":{"ena":1}
,"ena":{"clear":1}
}
;Search.control.loadWordPairs(pairs);
