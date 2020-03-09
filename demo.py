from .server import ServerInstance, LoadBalancer, LoadBalancerServer, Handler
from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = 'localhost' 
PORT = 8000

if __name__ == '__main__':
    # List of nodes to distribute load
    servers = [ServerInstance('', ''), ServerInstance('', '')]
    load_balancer = LoadBalancer(servers)
    http_server = LoadBalancerServer((HOST, PORT), Handler)
    # Set load balancer for our custom implementation of socketserver.TCPServer 
    http_server.set_load_balancer = load_balancer
    with http_server:
        http_server.serve_forever()
