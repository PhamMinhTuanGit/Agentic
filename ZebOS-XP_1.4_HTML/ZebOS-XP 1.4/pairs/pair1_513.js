var pairs =
{
"snmp":{"api":1,"tables":1,"functions":1}
,"api":{"chapter":1,"snmp":1}
,"chapter":{"contains":1}
,"contains":{"rip":1}
,"rip":{"snmp":1}
,"tables":{"api":1}
,"functions":{"apply":1,"ripng":1}
,"apply":{"rip":1}
}
;Search.control.loadWordPairs(pairs);
