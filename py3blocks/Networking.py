import contextlib
import socket

class Networking():

    def has_dual_stack():
        try:
            socket.AF_INET6
            socket.IPPROTO_IPV6
            socket.IPV6_V6ONLY
        except AttributeError:
            return False
        try:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            with contextlib.closing(sock):
                sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, False)
                return True
        except socket.error:
            pass
        return False


    def create_server_sock(address,
                           queue_size=5,
                           has_dualstack=has_dual_stack()):
        AF_INET6 = getattr(socket, 'AF_INET6', 0)
        host, port = address
        if host is None:
            host = "localhost"
        err = None
        info = socket.getaddrinfo(host,
                                  port,
                                  socket.AF_UNSPEC,
                                  socket.SOCK_STREAM,
                                  0,
                                  socket.AI_PASSIVE)
        for res in info:
            af, socktype, proto, canonname, sa = res
            sock = None
            try:
                sock = socket.socket(af, socktype, proto)
                if af == AF_INET6:
                    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, (0 if has_dualstack else 1))
                sock.bind(sa)
                sock.listen(queue_size)
                return sock
            except socket.error as e:
                err = e
                if sock is not None:
                    sock.close()
        if err is not None:
            raise err
        else:
            raise socket.error('no info returned by getaddrinfo')
