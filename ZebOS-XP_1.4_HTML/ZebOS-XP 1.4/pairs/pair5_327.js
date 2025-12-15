var pairs =
{
"msdp":{"default":1,"peers":1}
,"default":{"peer":1}
,"peer":{"msdp":1,"used":1,"rpf":1}
,"used":{"msdp":1}
,"peers":{"bgp":1,"messages":1}
,"bgp":{"peers":1}
,"messages":{"coming":1}
,"coming":{"default":1}
,"rpf":{"check":1}
,"check":{"always":1}
,"always":{"accepted":1}
}
;Search.control.loadWordPairs(pairs);
