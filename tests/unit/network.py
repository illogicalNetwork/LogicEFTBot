## Utility function
from typing import Dict

__MOCKED_URL_RESPONSES: Dict[str, str] = {}


def mock_url_get(url: str, response: str) -> None:
    """
    Mock the following URL to return <response>.
    """
    __MOCKED_URL_RESPONSES[url] = response


def mock_url_reset() -> None:
    global __MOCKED_URL_RESPONSES
    __MOCKED_URL_RESPONSES = {}


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, data, status_code):
            self.data = data
            self.status_code = status_code
            self.text = data
            self.content = data

    url = args[0]
    for u in __MOCKED_URL_RESPONSES:
        if url.startswith(u):
            return MockResponse(__MOCKED_URL_RESPONSES[u], 200)
    else:
        # Unmocked Network Request In Test
        return MockResponse(None, 404)
