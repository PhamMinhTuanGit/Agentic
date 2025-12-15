var pairs =
{
"application":{"protocol":1,"protocols":1}
,"protocol":{"interface":1}
,"interface":{"elmi":1,"(api)":1,"application":1}
,"elmi":{"application":1}
,"(api)":{"provides":1}
,"provides":{"interface":1}
,"protocols":{"requiring":1}
,"requiring":{"forwarding":1}
,"forwarding":{"plane":1}
,"plane":{"liveliness":1}
,"liveliness":{"detection":1}
}
;Search.control.loadWordPairs(pairs);
