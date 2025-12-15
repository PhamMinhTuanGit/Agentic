var pairs =
{
"interaction":{"signaling":1}
,"signaling":{"protocol":1}
,"protocol":{"signaling":1,"case":1}
,"case":{"rsvp-te":1}
,"rsvp-te":{"either":1}
,"either":{"initiator":1}
,"initiator":{"request":1}
,"request":{"recipient":1}
,"recipient":{"updates":1}
}
;Search.control.loadWordPairs(pairs);
