var pairs =
{
"validation":{"show":1}
,"show":{"ethernet":1}
,"ethernet":{"cfm":1,"multicast":1}
,"cfm":{"maintenance-points":1}
,"maintenance-points":{"remote":1,"local":1}
,"remote":{"show":1,"domain":1}
,"local":{"show":1}
,"domain":{"ping":1}
,"ping":{"ethernet":1}
,"multicast":{"mepid":1}
}
;Search.control.loadWordPairs(pairs);
