var pairs =
{
"enable":{"mpls-te":1}
,"mpls-te":{"level-1":1,"topology":1}
,"level-1":{"level-2":1}
,"level-2":{"l1-l2":1,"router":1}
,"l1-l2":{"following":1}
,"following":{"example":1,"configuration":1}
,"example":{"router":1}
,"router":{"l1\u002Fl2":1,"enabling":1,"following":1}
,"l1\u002Fl2":{"router":1}
,"enabling":{"mpls-te":1}
,"configuration":{"given":1}
,"given":{"mpls-te":1}
}
;Search.control.loadWordPairs(pairs);
