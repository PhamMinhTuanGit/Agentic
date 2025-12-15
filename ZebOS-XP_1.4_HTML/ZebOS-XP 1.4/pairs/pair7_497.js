var pairs =
{
"vrma":{"gma":1}
,"gma":{"interaction":1,"resides":1}
,"interaction":{"gma":1}
,"resides":{"router":1}
,"router":{"provides":1}
,"provides":{"services":1}
,"services":{"management":1}
,"management":{"authority":1}
,"authority":{"(vrma)":1}
,"(vrma)":{"communicate":1}
,"communicate":{"resources":1}
,"resources":{"outside":1}
,"outside":{"router":1}
}
;Search.control.loadWordPairs(pairs);
