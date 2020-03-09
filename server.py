import random
from typing import List, NamedTuple, Dict
from http.server import BaseHTTPRequestHandler

class ServerInstance(NamedTuple):
    fqdn: str
    weight: int


class LoadBalancer:
    def __init__(self, servers: List[ServerInstance]) -> None:
        self.servers = self.map_servers(servers)
        self.accumulated_weights = [*self.servers]
    
    def map_servers(self, servers: List[ServerInstance]) -> Dict:
        """
        Returns a dictionary with the accumulated weight as keys and
        the destination servers fqdn as values
        """
        map = {}
        for server in servers:
            index: int = reduce(lambda acc, val: acc + val, list(map)) + server.weight
            map[index] = server.fqdn
        return map

    def get_destination_server(self) -> str:
        """
        Generates a random number between 1 and the total amount of servers
        and matches it with a server using their relative accumulated weight
        """
        random_num: int = random.randint(1, len(self.accumulated_weights))
        for acc_weight in self.accumulated_weights:
            if random_num < acc_weight: return self.servers[acc_weight]


class LoadBalancerServer(socketserver.TCPServer):
    def set_load_balancer(self, load_balancer: LoadBalancer) -> None:
        self.load_balancer = load_balancer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.redirect()

    def do_POST(self) -> None:
        self.redirect()

    def do_PUT(self) -> None:
        self.redirect()

    def do_DELETE(self) -> None:
        self.redirect()

    def redirect(self) -> None:
        self.send_response(307)
        self.send_header('Location', self.server.load_balancer.get_destination_server())
        self.end_headers()

