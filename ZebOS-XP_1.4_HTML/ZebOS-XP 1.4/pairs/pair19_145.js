var pairs =
{
"deleting":{"(*,*":1}
,"(*,*":{"rp)":1}
,"rp)":{"state":1,"becomes":1}
,"state":{"(*,*":1,"deleted":1}
,"deleted":{"following":1}
,"following":{"occurs":1}
,"occurs":{"joindesired":1}
,"joindesired":{"rp)":1}
,"becomes":{"false":1}
,"false":{"new":1}
}
;Search.control.loadWordPairs(pairs);
