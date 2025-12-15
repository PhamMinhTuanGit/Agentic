var pairs =
{
"protection":{"group":1}
,"group":{"protection":1,"consists":1}
,"consists":{"pair":1}
,"pair":{"point-to-point":1,"beb":1}
,"point-to-point":{"tesi":1}
,"tesi":{"terminating":1}
,"terminating":{"pair":1}
,"beb":{"cbps":1}
,"cbps":{"service":1}
,"service":{"instance":1}
,"instance":{"used":1}
,"used":{"carry":1}
,"carry":{"traffic":1}
,"traffic":{"time":1}
}
;Search.control.loadWordPairs(pairs);
