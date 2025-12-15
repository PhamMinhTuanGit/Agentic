var pairs =
{
"clear":{"rbridge":1}
,"rbridge":{"trill":1}
,"trill":{"counter":1,"counters":1}
,"counter":{"command":1,"parameters":1}
,"command":{"reset":1,"syntax":1,"mode":1}
,"reset":{"trill":1}
,"counters":{"command":1}
,"syntax":{"clear":1}
,"parameters":{"none":1}
,"none":{"command":1}
,"mode":{"exec":1,"privilege":1,"examples":1}
,"exec":{"mode":1}
,"privilege":{"exec":1}
,"examples":{"clear":1}
}
;Search.control.loadWordPairs(pairs);
