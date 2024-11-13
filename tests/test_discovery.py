import unittest
from hue_discovery.discovery import HueDiscovery

class TestHueDiscovery(unittest.TestCase):
    def test_browse_services(self):
        hue = HueDiscovery()
        try:
            hue.browse_services(timeout=5)
            # Since network services can vary, we just check that the method runs without error
            self.assertIsInstance(hue.services, dict)
        finally:
            hue.close()

    def test_lookup_service(self):
        hue = HueDiscovery()
        try:
            hue.browse_services(timeout=5)
            if hue.services:
                first_service_name = list(hue.services.keys())[0].replace(f".{hue.service_type}", "")
                service_details = hue.lookup_service(first_service_name)
                self.assertIsNotNone(service_details)
                self.assertIn('hostname', service_details)
            else:
                self.skipTest("No services discovered to test lookup.")
        finally:
            hue.close()

    def test_resolve_hostname(self):
        hue = HueDiscovery()
        try:
            ip = hue.resolve_hostname("localhost")
            self.assertEqual(ip, "127.0.0.1")
        finally:
            hue.close()

if __name__ == '__main__':
    unittest.main()
