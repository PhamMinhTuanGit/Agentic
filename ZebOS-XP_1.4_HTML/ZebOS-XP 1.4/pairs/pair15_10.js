var pairs =
{
"bfd":{"nsm":1,"static":1}
,"nsm":{"static":1}
,"static":{"interface":1,"route":1}
,"interface":{"bfd":1,"detects":1}
,"detects":{"static":1}
,"route":{"nexthop":1}
,"nexthop":{"data-plane":1}
,"data-plane":{"failure":1}
,"failure":{"typically":1}
,"typically":{"module":1}
,"module":{"creates":1}
,"creates":{"deletes":1}
,"deletes":{"updates":1}
,"updates":{"sessions":1}
}
;Search.control.loadWordPairs(pairs);
