import socket
from zeroconf import Zeroconf, ServiceBrowser, ServiceStateChange, ServiceInfo
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

def main():
    hue = HueDiscovery()
    try:
        # Step 1: Browse for Hue Bridge services
        hue.browse_services(timeout=5)

        if not hue.services:
            print("No Hue Bridges found on the network.")
            return

        # List discovered services
        print("\nDiscovered Hue Bridges:")
        for idx, (name, details) in enumerate(hue.services.items(), start=1):
            print(f"{idx}. {name}")
            print(f"   Hostname: {details['hostname']}")
            print(f"   IP Addresses: {details['addresses']}")
            print(f"   Port: {details['port']}")
            print(f"   Properties: {details['properties']}")

        # Step 2: Lookup a specific service (e.g., the first one)
        first_service_name = list(hue.services.keys())[0].replace(f".{hue.service_type}", "")
        service_details = hue.lookup_service(first_service_name)
        if service_details:
            print(f"\nDetails of service '{first_service_name}':")
            print(f"Hostname: {service_details['hostname']}")
            print(f"Port: {service_details['port']}")
            print(f"Properties: {service_details['properties']}")
            print(f"Addresses: {service_details['addresses']}")

            # Step 3: Resolve hostname to IP address
            hostname = service_details['hostname']
            ip_address = hue.resolve_hostname(hostname)
            if ip_address:
                print(f"\nIP Address of {hostname}: {ip_address}")
            else:
                print(f"Could not resolve IP address for {hostname}.")
    finally:
        hue.close()

if __name__ == "__main__":
    main()
