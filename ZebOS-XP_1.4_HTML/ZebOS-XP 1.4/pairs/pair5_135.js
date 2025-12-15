var pairs =
{
"design":{"protocol":1}
,"protocol":{"module":1}
,"module":{"supports":1,"apis":1}
,"supports":{"elmi":1}
,"elmi":{"uses":1,"client":1,"base":1,"server":1}
,"uses":{"elmi":1}
,"client":{"apis":1}
,"apis":{"communicate":1,"connect":1}
,"communicate":{"elmi":1}
,"base":{"module":1}
,"connect":{"exchange":1}
,"exchange":{"information":1}
,"information":{"elmi":1}
,"server":{"module":1}
}
;Search.control.loadWordPairs(pairs);
