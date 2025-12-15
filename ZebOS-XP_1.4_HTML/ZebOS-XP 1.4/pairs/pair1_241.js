var pairs =
{
"802.1x":{"configuration":1,"restricts":1}
,"configuration":{"ieee":1}
,"ieee":{"802.1x":1}
,"restricts":{"unauthenticated":1}
,"unauthenticated":{"devices":1}
,"devices":{"connecting":1}
,"connecting":{"switch":1}
,"switch":{"authentication":1}
,"authentication":{"successful":1}
,"successful":{"traffic":1}
,"traffic":{"allowed":1}
,"allowed":{"switch":1}
}
;Search.control.loadWordPairs(pairs);
