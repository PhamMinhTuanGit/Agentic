var pairs =
{
"mesh":{"physical":1,"devices":1}
,"physical":{"logical":1}
,"logical":{"network":1}
,"network":{"topology":1,"connection":1}
,"topology":{"devices":1}
,"devices":{"redundant":1,"network":1,"partial":1,"connection":1}
,"redundant":{"interconnections":1}
,"interconnections":{"full":1}
,"full":{"mesh":1}
,"connection":{"devices":1}
,"partial":{"mesh":1}
}
;Search.control.loadWordPairs(pairs);
