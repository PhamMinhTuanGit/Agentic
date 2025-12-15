var pairs =
{
"rbridge2":{"write":1}
,"write":{"script":1}
,"script":{"code":1}
,"code":{"generate":1}
,"generate":{"hellos":1}
,"hellos":{"rb1":1}
,"rb1":{"vlan":1}
,"vlan":{"rb2":1}
,"rb2":{"hello":1,"rb1":1}
,"hello":{"send":1}
,"send":{"rb2":1}
}
;Search.control.loadWordPairs(pairs);
