var pairs =
{
"ospf":{"bfd":1}
,"bfd":{"single-hop":1}
,"single-hop":{"session":1,"ospf":1}
,"session":{"section":1}
,"section":{"provides":1}
,"provides":{"steps":1}
,"steps":{"configuring":1}
,"configuring":{"bfd":1}
}
;Search.control.loadWordPairs(pairs);
