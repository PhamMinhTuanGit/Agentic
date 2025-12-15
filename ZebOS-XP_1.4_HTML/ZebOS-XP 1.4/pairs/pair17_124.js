var pairs =
{
"redirect":{"modifier":1,"\u002Fvar\u002Fframe.txt":1}
,"modifier":{"redirect":1,"writes":1}
,"writes":{"output":1}
,"output":{"file":1,"displayed":1,"redirection":1}
,"file":{"output":1}
,"displayed":{"show":1}
,"show":{"history":1}
,"history":{"redirect":1,">\u002Fvar\u002Fframe.txt":1}
,"\u002Fvar\u002Fframe.txt":{"output":1}
,"redirection":{"token":1}
,"token":{"(>)":1}
,"(>)":{"thing":1}
,"thing":{"show":1}
}
;Search.control.loadWordPairs(pairs);
