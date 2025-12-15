var pairs =
{
"topology":{"configure":1,"asbr":1}
,"configure":{"routers":1}
,"routers":{"routers":1,"asbr":1}
,"asbr":{"according":1,"asbrs":1}
,"according":{"topology":1}
,"asbrs":{"ebgp":1}
}
;Search.control.loadWordPairs(pairs);
