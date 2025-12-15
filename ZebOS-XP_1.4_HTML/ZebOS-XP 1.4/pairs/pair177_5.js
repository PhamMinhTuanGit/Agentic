var pairs =
{
"hello":{"packet":1,"packets":1}
,"packet":{"multicast":1,"used":1}
,"multicast":{"packet":1}
,"used":{"protocols":1}
,"protocols":{"neighbor":1}
,"neighbor":{"discovery":1}
,"discovery":{"recovery":1}
,"recovery":{"hello":1}
,"packets":{"indicate":1}
,"indicate":{"client":1}
,"client":{"operating":1}
,"operating":{"network-ready":1}
}
;Search.control.loadWordPairs(pairs);
