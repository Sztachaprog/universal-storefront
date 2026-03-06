import requests
import pytest
from playwright.sync_api import sync_playwright

def test_environment_ready():
    print("\n[CONFIRMED] Ecosystem is alive!")
    print(f"Requests version: {requests.__version__}")