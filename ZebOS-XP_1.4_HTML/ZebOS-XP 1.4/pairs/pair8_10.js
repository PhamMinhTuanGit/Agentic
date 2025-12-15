var pairs =
{
"ospfv3":{"bfd":1,"multi-hop":1}
,"bfd":{"multi-hop":1,"ospfv3":1}
,"multi-hop":{"sessions":1}
,"sessions":{"section":1}
,"section":{"provides":1}
,"provides":{"steps":1}
,"steps":{"configuring":1}
,"configuring":{"bfd":1}
}
;Search.control.loadWordPairs(pairs);
