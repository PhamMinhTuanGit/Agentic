var pairs =
{
"reset":{"log":1,"current":1}
,"log":{"file":1}
,"file":{"command":1,"parameters":1}
,"command":{"reset":1,"syntax":1,"mode":1}
,"current":{"open":1}
,"open":{"log":1}
,"syntax":{"reset":1}
,"parameters":{"none":1}
,"none":{"command":1}
,"mode":{"privileged":1,"example":1}
,"privileged":{"exec":1}
,"exec":{"mode":1}
,"example":{"enable":1}
,"enable":{"reset":1}
}
;Search.control.loadWordPairs(pairs);
