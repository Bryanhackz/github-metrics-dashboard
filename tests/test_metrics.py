import unittest
from wsgiref.util import setup_testing_defaults
from router import application

class RouterTests(unittest.TestCase):
    def _make_request(self, path: str) -> tuple[str, bytes]:
        environ = {}
        setup_testing_defaults(environ)
        environ["PATH_INFO"] = path
        
        status_holder = {}
        def start_response(status, headers):
            status_holder["status"] = status
            
        response = application(environ, start_response)
        return status_holder["status"], response[0]

    def test_health_endpoint(self):
        status, body = self._make_request("/health")
        self.assertEqual(status, "200 OK")
        self.assertEqual(body, b'{"ok": true}')

    def test_api_invalid_format(self):
        status, body = self._make_request("/api/metrics/invalid")
        self.assertEqual(status, "400 Bad Request")

if __name__ == "__main__":
    unittest.main()