var pairs =
{
"node-protecting":{"type":1}
,"type":{"path":1}
,"path":{"bypasses":1}
,"bypasses":{"primary-path":1}
,"primary-path":{"gateway":1}
,"gateway":{"router":1}
,"router":{"protect":1,"next":1}
,"protect":{"router":1}
,"next":{"hop":1}
,"hop":{"primary":1}
,"primary":{"path":1}
}
;Search.control.loadWordPairs(pairs);
