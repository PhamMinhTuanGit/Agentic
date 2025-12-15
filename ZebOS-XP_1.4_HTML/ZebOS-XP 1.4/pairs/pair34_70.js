var pairs =
{
"spb":{"enable":1,"interface":1,"disable":1}
,"enable":{"command":1,"disable":1,"spb":1,"enable":1}
,"command":{"enable":1,"syntax":1,"mode":1}
,"disable":{"spb":1,"parameters":1,"disable":1}
,"interface":{"command":1,"disable":1,"mode":1,"eth1":1}
,"syntax":{"spb":1}
,"parameters":{"enable":1}
,"mode":{"interface":1,"example":1}
,"example":{"config":1}
,"config":{"terminal":1}
,"terminal":{"(config)":1}
,"(config)":{"interface":1}
,"eth1":{"(config-if)":1}
,"(config-if)":{"spb":1}
}
;Search.control.loadWordPairs(pairs);
