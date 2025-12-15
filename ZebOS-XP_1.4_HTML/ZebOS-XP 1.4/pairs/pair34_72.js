var pairs =
{
"copy":{"startup-config":1,"start-up":1}
,"startup-config":{"running-config":1}
,"running-config":{"command":1,"parameters":1}
,"command":{"copy":1,"syntax":1,"mode":1}
,"start-up":{"configuration":1}
,"configuration":{"running":1,"command":1}
,"running":{"configuration":1}
,"syntax":{"copy":1}
,"parameters":{"none":1}
,"none":{"command":1}
,"mode":{"privileged":1,"examples":1}
,"privileged":{"exec":1}
,"exec":{"mode":1}
,"examples":{"copy":1}
}
;Search.control.loadWordPairs(pairs);
