var pairs =
{
"ospf":{"bfd":1,"multi-hop":1}
,"bfd":{"multi-hop":1,"ospf":1}
,"multi-hop":{"session":1,"sessions":1}
,"session":{"section":1}
,"section":{"provides":1}
,"provides":{"steps":1}
,"steps":{"configuring":1}
,"configuring":{"bfd":1}
}
;Search.control.loadWordPairs(pairs);
