import socket
from dateutil import tz, parser
import sys
import pdb
import os

# class ForkablePdb(pdb.Pdb):
#     """A Pdb subclass that may be used
#     from a forked multiprocessing child
# 
#     """
#     def interaction(self, *args, **kwargs):
#         _stdin = sys.stdin
#         try:
#             sys.stdin = open('/dev/stdin')
#             pdb.Pdb.interaction(self, *args, **kwargs)
#         finally:
#             sys.stdin = _stdin

class ForkablePdb(pdb.Pdb):

    _original_stdin_fd = sys.stdin.fileno()
    _original_stdin = None

    def __init__(self):
        pdb.Pdb.__init__(self, nosigint=True)

    def _cmdloop(self):
        current_stdin = sys.stdin
        try:
            if not self._original_stdin:
                self._original_stdin = os.fdopen(self._original_stdin_fd)
            sys.stdin = self._original_stdin
            self.cmdloop()
        finally:
            sys.stdin = current_stdin

# For command line processing
def multidict(items):
    ret = {}
    for k, v in items:
        if k in ret:
            if not isinstance(ret[k], list):
                ret[k] = [ret[k]]
            ret[k].append(v)
        else:
            ret[k] = v
    return ret

def port_is_free(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("0.0.0.0", port))
        result = True
    except:
        result = False
    finally:
        sock.close()
    return result

def convert_timezone(s, from_zone, to_zone):
    """Converts a datetime iso string (datetime.isoformat()) from one zone to another"""
    if isinstance(s, str):
        s = parser.parse(s)
    s = s.replace(tzinfo=from_zone)
    return s.astimezone(to_zone).isoformat() 
    
def utc_to_local(s):
    """Converts a datetime iso string (datetime.isoformat()) from utc to local time"""
    return convert_timezone(
        s, from_zone = tz.tzutc(), to_zone = tz.tzlocal())
