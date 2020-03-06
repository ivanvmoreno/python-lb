import random
from typing import List, NamedTuple, Dict, Callable, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler

class Node(NamedTuple):
    fqdn: str
    weight: int

class Handler(BaseHTTPRequestHandler):
    def __init__(self, servers: Dict, load_balancer: Callable, random_seed: Optional[int]) -> None:
        self.servers = servers
        self._lb = load_balancer
        if random_seed: random.seed(random_seed)

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
        self.send_header('Location', self._lb(self.servers))
        self.end_headers()

class LoadBalancer:
    def __init__(self, listen_port: int, servers: List[Node]) -> None:
        self.listen_port = listen_port
        self.servers = self.map_servers(servers)
    
    def map_servers(servers: List[Node]) -> Dict:
        """
        Returns a dictionary with the accumulated weight as keys and
        the destination servers fqdn as values
        """
        map = {}
        for server in servers:
            index: int = reduce(lambda acc, val: acc + val, list(map)) + server.weight
            map[index] = server.fqdn
        return map

    def get_destination_server(seed: , servers_map: Dict) -> str:
        """
        Generates a random number between 1 and the total amount of servers
        and matches it with a server using their relative accumulated weight
        """
        accumulated_weights: List[int] = list(servers_map)
        random: int = random.randint(1, len(accumulated_weights))
        for acc_weight in accumulated_weights:
            if random < acc_weight: return servers_map[acc_weight]


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
