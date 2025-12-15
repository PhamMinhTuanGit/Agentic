var pairs =
{
"maintenance":{"domain":1}
,"domain":{"(md)":1}
,"(md)":{"connectivity":1}
,"connectivity":{"fault":1,"managed":1}
,"fault":{"management":1}
,"management":{"(cfm)":1}
,"(cfm)":{"network":1}
,"network":{"part":1,"faults":1}
,"part":{"network":1}
,"faults":{"connectivity":1}
}
;Search.control.loadWordPairs(pairs);
