var pairs =
{
"interface-disjoint":{"type":1}
,"type":{"path":1}
,"path":{"point-to-point":1}
,"point-to-point":{"interface":1}
,"interface":{"alternate":1}
,"alternate":{"next":1}
,"next":{"hop":1}
,"hop":{"rerouting":1}
,"rerouting":{"primary":1}
,"primary":{"gateway":1}
,"gateway":{"fails":1}
,"fails":{"thus":1}
,"thus":{"protecting":1}
,"protecting":{"interface":1}
}
;Search.control.loadWordPairs(pairs);
