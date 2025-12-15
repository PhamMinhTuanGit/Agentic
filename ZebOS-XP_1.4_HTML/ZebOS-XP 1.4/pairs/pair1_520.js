var pairs =
{
"refresh":{"reduction":1}
,"reduction":{"commands":1}
,"commands":{"chapter":1,"ack-wait-timeout":1}
,"chapter":{"describes":1}
,"describes":{"rsvp-te":1}
,"rsvp-te":{"refresh":1}
,"ack-wait-timeout":{"message-ack":1,"rsvp":1}
,"message-ack":{"refresh-reduction":1,"rsvp":1}
,"refresh-reduction":{"rsvp":1}
,"rsvp":{"ack-wait-timeout":1,"message-ack":1,"refresh-reduction":1}
}
;Search.control.loadWordPairs(pairs);
