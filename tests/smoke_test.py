"""
hiSHtory Container Smoke & Integration Tests
Validates Nginx path routing, Ingress API endpoints, and Web UI Basic Authentication.
"""

import time
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
TEST_USER = "testadmin"
TEST_PASS = "testsecretpass"


def test_container_readiness():
    """Poll the /healthcheck endpoint until container is ready."""
    max_retries = 30
    for _ in range(max_retries):
        try:
            resp = requests.get(f"{BASE_URL}/healthcheck", timeout=2)
            if resp.status_code == 200:
                return
        except requests.RequestException:
            pass
        time.sleep(1)
    pytest.fail(f"Container failed to become healthy at {BASE_URL}/healthcheck within 30s")


def test_ingress_healthcheck_endpoint():
    """Verify that /healthcheck returns HTTP 200 without requiring auth."""
    resp = requests.get(f"{BASE_URL}/healthcheck", timeout=5)
    assert resp.status_code == 200


def test_ingress_api_routing():
    """Verify that /api/ requests are proxied to Ingress backend without basic auth."""
    resp = requests.get(f"{BASE_URL}/api/v1/health", timeout=5)
    # Backend responds with 200, 404, or 400 depending on route, but NOT 401 (Nginx basic auth)
    assert resp.status_code != 401


def test_web_ui_unauthorized():
    """Verify that Web UI root (/) challenges unauthorized access with 401."""
    resp = requests.get(f"{BASE_URL}/", timeout=5)
    assert resp.status_code == 401
    assert "Basic realm=" in resp.headers.get("WWW-Authenticate", "")


def test_web_ui_invalid_credentials():
    """Verify that wrong credentials receive 401 Unauthorized."""
    resp = requests.get(f"{BASE_URL}/", auth=("wronguser", "badpassword"), timeout=5)
    assert resp.status_code == 401


def test_web_ui_authorized():
    """Verify that correct credentials successfully authenticate into Web UI."""
    resp = requests.get(f"{BASE_URL}/", auth=(TEST_USER, TEST_PASS), timeout=10)
    # Expect 200 OK or redirect
    assert resp.status_code in (200, 302, 304)
