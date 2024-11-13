import socket
from zeroconf import Zeroconf, ServiceBrowser, ServiceStateChange, ServiceInfo
import threading
import time


class HueDiscovery:
    def __init__(self, service_type="_hue._tcp.local."):
        self.service_type = service_type
        self.zeroconf = Zeroconf()
        self.services = {}
        self.browser = None

    def on_service_state_change(self, zeroconf, service_type, name, state_change):
        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            if info:
                service_details = {
                    'name': name,
                    'hostname': info.server,
                    'port': info.port,
                    'properties': info.properties,
                    'addresses': [socket.inet_ntoa(addr) for addr in info.addresses]
                }
                self.services[name] = service_details
                print(f"Service added: {name}")
                print(f"  Hostname: {info.server}")
                print(f"  Addresses: {service_details['addresses']}")
                print(f"  Port: {info.port}")
                print(f"  Properties: {info.properties}")

    def browse_services(self, timeout=5):
        print(f"Browsing for services of type {self.service_type}...")
        self.browser = ServiceBrowser(self.zeroconf, self.service_type, handlers=[self.on_service_state_change])
        # Wait for services to be discovered
        time.sleep(timeout)

    def lookup_service(self, instance_name):
        full_name = f"{instance_name}.{self.service_type}"
        info = self.zeroconf.get_service_info(self.service_type, full_name)
        if info:
            service_details = {
                'name': instance_name,
                'hostname': info.server,
                'port': info.port,
                'properties': info.properties,
                'addresses': [socket.inet_ntoa(addr) for addr in info.addresses]
            }
            return service_details
        else:
            print(f"Service {instance_name} not found.")
            return None

    def resolve_hostname(self, hostname):
        try:
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except socket.gaierror as e:
            print(f"Error resolving hostname {hostname}: {e}")
            return None

    def close(self):
        self.zeroconf.close()
