from salary_exploration import browser


class FakeFirefox:
    """Stands in for webdriver.Firefox so the test needs no real browser."""

    def __init__(self):
        self.visited = []

    def get(self, url):
        self.visited.append(url)


def test_open_browser_visits_the_url(monkeypatch):
    monkeypatch.setattr(browser.time, "sleep", lambda seconds: None)
    monkeypatch.setattr(browser.webdriver, "Firefox", FakeFirefox)

    opened = browser.open_browser("https://example.com/")

    assert isinstance(opened, FakeFirefox)
    assert opened.visited == ["https://example.com/"]
