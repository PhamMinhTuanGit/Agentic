var pairs =
{
"stopping":{"zebos-xp":1}
,"zebos-xp":{"daemons":1,"daemon":1}
,"daemons":{"stop":1}
,"stop":{"zebos-xp":1}
,"daemon":{"terminating":1,"example":1,"stopped":1}
,"terminating":{"process":1}
,"process":{"daemon":1,"running":1}
,"example":{"kill":1}
,"kill":{"<pid>":1}
,"<pid>":{"<pid>":1,"process":1}
,"stopped":{"command":1}
,"command":{"find":1}
,"find":{"process":1}
,"running":{"daemon":1}
}
;Search.control.loadWordPairs(pairs);
