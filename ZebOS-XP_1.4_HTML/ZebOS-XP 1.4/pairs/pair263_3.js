var pairs =
{
"neighbor":{"adjacent":1}
,"adjacent":{"system":1,"device":1}
,"system":{"reachable":1}
,"reachable":{"traversing":1}
,"traversing":{"single":1}
,"single":{"subnetwork":1}
,"subnetwork":{"immediately":1}
,"immediately":{"adjacent":1}
,"device":{"called":1}
,"called":{"peer":1}
,"peer":{"adjacency":1}
}
;Search.control.loadWordPairs(pairs);
