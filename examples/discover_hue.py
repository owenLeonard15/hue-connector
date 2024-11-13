from hue_discovery import HueDiscovery

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
