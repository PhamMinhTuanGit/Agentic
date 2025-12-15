var pairs =
{
"mpls-tp":{"routing":1,"rib":1}
,"routing":{"information":1}
,"information":{"base":1}
,"base":{"mpls-tp":1,"(rib)":1}
,"(rib)":{"infrastructure":1}
,"infrastructure":{"defines":1}
,"defines":{"forward":1}
,"forward":{"\u002Freverse":1}
,"\u002Freverse":{"path":1}
,"path":{"forwarding":1}
,"forwarding":{"entities":1}
,"entities":{"mpls-tp":1}
,"rib":{"tables":1}
}
;Search.control.loadWordPairs(pairs);
