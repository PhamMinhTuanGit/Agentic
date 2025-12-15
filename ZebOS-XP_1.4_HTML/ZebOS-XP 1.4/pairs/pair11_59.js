var pairs =
{
"maintenance":{"entity":1,"association":1}
,"entity":{"maintenance":1,"(me)":1}
,"(me)":{"point-to-point":1}
,"point-to-point":{"relationship":1}
,"relationship":{"two":1}
,"two":{"mips":1}
,"mips":{"within":1}
,"within":{"single":1}
,"single":{"maintenance":1}
}
;Search.control.loadWordPairs(pairs);
