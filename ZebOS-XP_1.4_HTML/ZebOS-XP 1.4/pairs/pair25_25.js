var pairs =
{
"definition":{"struct":1}
,"struct":{"prefix_ipv4":1,"pal_in4_addr":1}
,"prefix_ipv4":{"{u_int8_t":1}
,"{u_int8_t":{"family":1}
,"family":{"u_int8_t":1}
,"u_int8_t":{"prefixlen":1,"pad1":1,"pad2":1}
,"prefixlen":{"u_int8_t":1}
,"pad1":{"u_int8_t":1}
,"pad2":{"struct":1}
,"pal_in4_addr":{"prefix":1}
}
;Search.control.loadWordPairs(pairs);
