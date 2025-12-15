var pairs =
{
"stop":{"debugging":1}
,"debugging":{"turn":1,"debug":1,"stopped":1,"parameter":1}
,"turn":{"debugging":1}
,"debug":{"undebug":1,"bgp":1}
,"undebug":{"command":1,"commands":1}
,"command":{"protocol":1}
,"protocol":{"specified":1,"stop":1}
,"specified":{"debug":1,"protocol":1}
,"commands":{"debugging":1,"(config)":1}
,"stopped":{"specified":1}
,"parameter":{"commands":1}
,"(config)":{"debug":1}
,"bgp":{"events":1}
,"events":{"undebug":1}
}
;Search.control.loadWordPairs(pairs);
