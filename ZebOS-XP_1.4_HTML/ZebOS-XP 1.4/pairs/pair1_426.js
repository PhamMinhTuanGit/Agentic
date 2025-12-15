var pairs =
{
"control":{"channel":1}
,"channel":{"mode":1}
,"mode":{"commands":1,"includes":1}
,"commands":{"commands":1,"chapter":1,"control-channel":1}
,"chapter":{"issued":1}
,"issued":{"nsm":1}
,"nsm":{"control":1}
,"includes":{"following":1}
,"following":{"commands":1}
,"control-channel":{"description":1,"show":1,"shutdown":1}
,"description":{"show":1}
,"show":{"control-channel":1,"running-config":1}
,"running-config":{"control-channel":1}
}
;Search.control.loadWordPairs(pairs);
