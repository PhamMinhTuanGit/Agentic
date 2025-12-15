var pairs =
{
"multi-area":{"adjacency":1}
,"adjacency":{"multi-area":1,"provides":1}
,"provides":{"support":1}
,"support":{"multiple":1}
,"multiple":{"ospf":1}
,"ospf":{"areas":1}
,"areas":{"single":1}
,"single":{"interface":1}
}
;Search.control.loadWordPairs(pairs);
