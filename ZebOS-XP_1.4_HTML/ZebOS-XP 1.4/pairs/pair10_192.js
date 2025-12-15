var pairs =
{
"definition":{"struct":1}
,"struct":{"mpls_nh_fwd":1,"pal_in4_addr":1,"pal_in6_addr":1}
,"mpls_nh_fwd":{"{u_char":1}
,"{u_char":{"afi":1,"key":1}
,"afi":{"union":1}
,"union":{"{u_char":1}
,"key":{"struct":1}
,"pal_in4_addr":{"ipv4":1}
,"ipv4":{"ifdef":1}
,"ifdef":{"have_ipv6":1}
,"have_ipv6":{"struct":1}
,"pal_in6_addr":{"ipv6":1}
,"ipv6":{"endif":1}
}
;Search.control.loadWordPairs(pairs);
