var pairs =
{
"messages":{"following":1,"exchanged":1}
,"following":{"messages":1}
,"exchanged":{"bfd":1}
,"bfd":{"client":1,"is-is":1}
,"client":{"bfd":1}
,"is-is":{"management":1}
,"management":{"interface":1}
,"interface":{"bfd_msg_session_add":1}
,"bfd_msg_session_add":{"bfd_msg_session_delete":1}
,"bfd_msg_session_delete":{"bfd_msg_session_up":1}
,"bfd_msg_session_up":{"bfd_msg_session_down":1}
,"bfd_msg_session_down":{"bfd_msg_session_error":1}
,"bfd_msg_session_error":{"bfd_msg_session_attr_update":1}
}
;Search.control.loadWordPairs(pairs);
