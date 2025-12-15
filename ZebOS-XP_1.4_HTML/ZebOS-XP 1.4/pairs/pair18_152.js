var pairs =
{
"creating":{"(*,*":1}
,"(*,*":{"rp)":1}
,"rp)":{"state":1,"existing":1}
,"state":{"(*,*":1,"created":1,"exist":1}
,"created":{"following":1}
,"following":{"occurs":1}
,"occurs":{"state":1}
,"exist":{"zebos-xp":1}
,"zebos-xp":{"receives":1}
,"receives":{"join":1}
,"join":{"rp)":1}
}
;Search.control.loadWordPairs(pairs);
