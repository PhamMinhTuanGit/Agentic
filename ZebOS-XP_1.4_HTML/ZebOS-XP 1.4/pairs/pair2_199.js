var pairs =
{
"command":{"rename":1,"syntax":1,"mode":1}
,"rename":{"(move)":1}
,"(move)":{"file":1}
,"file":{"command":1,"names":1}
,"syntax":{"line":1}
,"line":{"parameters":1,"source":1}
,"parameters":{"line":1}
,"source":{"destination":1}
,"destination":{"file":1}
,"names":{"command":1}
,"mode":{"exec":1,"examples":1}
,"exec":{"mode":1}
,"examples":{"old-name":1}
,"old-name":{"new-name":1}
}
;Search.control.loadWordPairs(pairs);
