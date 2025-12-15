var pairs =
{
"rmon":{"clear":1,"counters":1}
,"clear":{"command":1,"rmon":1,"counters":1}
,"command":{"clear":1,"syntax":1,"mode":1}
,"counters":{"command":1,"parameters":1,"clears":1}
,"syntax":{"rmon":1}
,"parameters":{"counters":1}
,"clears":{"rmon":1}
,"mode":{"interface":1,"example":1}
,"interface":{"mode":1}
,"example":{"(config-if)":1}
,"(config-if)":{"rmon":1}
}
;Search.control.loadWordPairs(pairs);
