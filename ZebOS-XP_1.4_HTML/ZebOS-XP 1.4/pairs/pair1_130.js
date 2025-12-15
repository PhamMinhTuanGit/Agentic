var pairs =
{
"service":{"oam":1,"networks":1}
,"oam":{"zebos-xp":1,"(soam)":1}
,"zebos-xp":{"service":1}
,"(soam)":{"provides":1}
,"provides":{"robust":1}
,"robust":{"management":1}
,"management":{"tools":1}
,"tools":{"help":1}
,"help":{"maintain":1}
,"maintain":{"ethernet":1}
,"ethernet":{"service":1}
}
;Search.control.loadWordPairs(pairs);
