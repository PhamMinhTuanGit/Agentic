var pairs =
{
"zebos-xp":{"diffserv-te":1}
,"diffserv-te":{"implementation":1}
,"implementation":{"zebos-xp":1,"involves":1}
,"involves":{"nsm":1}
,"nsm":{"rsvp-te":1}
,"rsvp-te":{"cspf":1}
,"cspf":{"ospf":1}
}
;Search.control.loadWordPairs(pairs);
