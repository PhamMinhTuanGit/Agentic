var pairs =
{
"validation":{"show":1}
,"show":{"virtual-router":1}
,"virtual-router":{"virtual":1}
,"virtual":{"router":1}
,"router":{"vr1":1}
,"vr1":{"description":1,"customer-a":1}
,"description":{"vr1":1}
,"customer-a":{"loaded":1}
,"loaded":{"protocols":1}
,"protocols":{"vr-id":1}
,"vr-id":{"router-id":1}
,"router-id":{"unset":1}
,"unset":{"interfaces":1}
}
;Search.control.loadWordPairs(pairs);
