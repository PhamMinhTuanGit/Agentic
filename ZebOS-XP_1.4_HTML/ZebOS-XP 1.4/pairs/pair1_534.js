var pairs =
{
"quality":{"service":1}
,"service":{"quality":1,"(qos)":1}
,"(qos)":{"module":1}
,"module":{"interacts":1}
,"interacts":{"nsm":1}
,"nsm":{"signaling":1}
,"signaling":{"protocol":1}
,"protocol":{"(rsvp-te)":1}
,"(rsvp-te)":{"mpls":1}
,"mpls":{"forwarder":1}
}
;Search.control.loadWordPairs(pairs);
