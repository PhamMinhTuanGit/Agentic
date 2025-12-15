var pairs =
{
"bundling":{"uni":1,"cvlan":1,"multiple":1}
,"uni":{"configuration":1,"configured":1,"topology":1}
,"configuration":{"topology":1}
,"topology":{"uni":1}
,"configured":{"bundling":1}
,"cvlan":{"registration":1}
,"registration":{"table":1}
,"table":{"svlan":1}
,"svlan":{"supported":1,"bundling":1}
,"supported":{"uni":1}
,"multiple":{"cvlans":1}
,"cvlans":{"mapped":1}
,"mapped":{"svlan":1}
}
;Search.control.loadWordPairs(pairs);
