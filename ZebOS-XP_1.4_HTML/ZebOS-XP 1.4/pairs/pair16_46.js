var pairs =
{
"rooted-multipoint":{"evc":1,"services":1}
,"evc":{"rooted-multipoint":1,"unis":1,"leaf":1}
,"unis":{"designated":1}
,"designated":{"root":1,"leaf":1}
,"root":{"unis":1,"uni":1,"rooted-multipoint":1}
,"leaf":{"root":1,"uni":1}
,"uni":{"send":1}
,"send":{"service":1,"receive":1}
,"service":{"frames":1}
,"frames":{"points":1,"root":1}
,"points":{"evc":1}
,"receive":{"service":1}
}
;Search.control.loadWordPairs(pairs);
