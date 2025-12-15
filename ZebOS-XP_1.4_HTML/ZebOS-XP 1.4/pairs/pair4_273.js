var pairs =
{
"on-demand":{"loss":1}
,"loss":{"measurement":1}
,"measurement":{"pe1":1,"session":1}
,"pe1":{"-oam":1}
,"-oam":{"mpls-tp":1}
,"mpls-tp":{"loss-measurement":1}
,"loss-measurement":{"meg-name":1}
,"meg-name":{"meg1":1}
,"meg1":{"me-name":1,"me1":1}
,"me-name":{"me1":1}
,"me1":{"initiate":1}
,"initiate":{"on-demand":1}
,"session":{"meg1":1}
}
;Search.control.loadWordPairs(pairs);
