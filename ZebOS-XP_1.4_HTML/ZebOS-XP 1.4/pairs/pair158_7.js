var pairs =
{
"flapping":{"condition":1}
,"condition":{"network":1}
,"network":{"instability":1}
,"instability":{"route":1}
,"route":{"announced":1,"flapping":1}
,"announced":{"withdrawn":1}
,"withdrawn":{"repeatedly":1}
,"repeatedly":{"usually":1}
,"usually":{"result":1}
,"result":{"intermittently":1}
,"intermittently":{"failing":1}
,"failing":{"link":1}
,"link":{"called":1}
,"called":{"route":1}
}
;Search.control.loadWordPairs(pairs);
