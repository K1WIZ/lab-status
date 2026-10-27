"""Behavior tests: run with python3 -m unittest discover -s tests -v."""

import json
import os
import unittest
from unittest.mock import patch
from wsgiref.util import setup_testing_defaults

from app import application


def request(path, method="GET"):
    environ = {}
    setup_testing_defaults(environ)
    environ.update(PATH_INFO=path, REQUEST_METHOD=method)
    result = {}

    def start_response(status, headers):
        result.update(status=status, headers=dict(headers))

    result["body"] = b"".join(application(environ, start_response))
    return result


class AppTests(unittest.TestCase):
    def setUp(self):
        # Tests must not depend on the developer's shell environment.
        self.environment = patch.dict(os.environ, {}, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def test_home_shows_default_message(self):
        response = request("/")
        self.assertEqual(response["status"], "200 OK")
        self.assertIn(b"Hello from my home lab!", response["body"])

    def test_message_can_be_configured(self):
        with patch.dict(os.environ, {"APP_MESSAGE": "John's lab"}):
            self.assertIn(b"John&#x27;s lab", request("/")["body"])

    def test_message_is_escaped_as_text(self):
        with patch.dict(os.environ, {"APP_MESSAGE": "<script>alert(1)</script>"}):
            body = request("/")["body"]
        self.assertNotIn(b"<script>", body)
        self.assertIn(b"&lt;script&gt;", body)

    def test_health_contract(self):
        response = request("/health")
        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(json.loads(response["body"]), {"status": "ok"})
        self.assertIn("application/json", response["headers"]["Content-Type"])

    def test_version_without_build_metadata(self):
        data = json.loads(request("/version")["body"])
        self.assertEqual(data, {"version": "0.1.0", "commit": "unknown"})

    def test_version_reports_supplied_commit(self):
        with patch.dict(os.environ, {"GIT_COMMIT": "abc123"}):
            self.assertEqual(json.loads(request("/version")["body"])["commit"], "abc123")

    def test_unknown_route_returns_404(self):
        self.assertEqual(request("/missing")["status"], "404 Not Found")

    def test_post_is_not_allowed(self):
        response = request("/health", "POST")
        self.assertEqual(response["status"], "405 Method Not Allowed")
        self.assertEqual(response["headers"]["Allow"], "GET, HEAD")

    def test_head_has_headers_but_no_body(self):
        response = request("/", "HEAD")
        self.assertEqual(response["status"], "200 OK")
        self.assertEqual(response["body"], b"")
        self.assertEqual(response["headers"]["Content-Length"], str(len(request("/")["body"])))


if __name__ == "__main__":
    unittest.main()
