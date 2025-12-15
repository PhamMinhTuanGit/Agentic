var pairs =
{
"creating":{"state":1}
,"state":{"state":1,"created":1}
,"created":{"following":1,"join":1}
,"following":{"becomes":1}
,"becomes":{"true":1}
,"true":{"state":1}
,"join":{"received":1}
,"received":{"local":1,"(*,*":1}
,"local":{"membership":1}
,"membership":{"non-nullr":1}
,"non-nullr":{"assert":1}
,"assert":{"received":1}
,"(*,*":{"rp)":1}
,"rp)":{"state":1}
}
;Search.control.loadWordPairs(pairs);
