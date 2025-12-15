var pairs =
{
"definition":{"struct":1}
,"struct":{"nsm_msg_header":1}
,"nsm_msg_header":{"{\u002F*vr-id":1}
,"{\u002F*vr-id":{"*\u002Fu_int32_t":1}
,"*\u002Fu_int32_t":{"vr_id":1,"vrf_id":1,"message_id":1}
,"vr_id":{"\u002F*vrf-id":1}
,"\u002F*vrf-id":{"*\u002Fu_int32_t":1}
,"vrf_id":{"\u002F*message":1}
,"\u002F*message":{"type":1,"len":1,"*\u002Fu_int32_t":1}
,"type":{"*\u002Fu_int16_t":1,"\u002F*message":1}
,"*\u002Fu_int16_t":{"type":1,"length":1}
,"len":{"*\u002Fu_int16_t":1}
,"length":{"\u002F*message":1}
}
;Search.control.loadWordPairs(pairs);
