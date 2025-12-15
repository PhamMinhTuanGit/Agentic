var pairs =
{
"two":{"backup":1}
,"backup":{"routers":1}
,"routers":{"configuration":1,"gateway":1}
,"configuration":{"host":1}
,"host":{"gateway":1}
,"gateway":{"router":1}
,"router":{"interface":1,"run":1}
,"interface":{"eth1":1}
,"eth1":{"routers":1}
,"run":{"igp":1}
,"igp":{"protocol":1}
,"protocol":{"configuring":1}
,"configuring":{"vrrp":1}
,"vrrp":{"two":1}
}
;Search.control.loadWordPairs(pairs);
