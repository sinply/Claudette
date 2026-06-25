"""
Client-side Web Search tool executor using DuckDuckGo or SearXNG.
Works with all API providers (Anthropic, DeepSeek, OpenRouter, etc.).
"""

import html.parser
import json
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request


_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


def _ssl_context(verify_ssl):
    if verify_ssl:
        return ssl.create_default_context()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


class _ResultExtractor(html.parser.HTMLParser):
    """Pull result links and snippets out of DuckDuckGo's HTML search page."""

    def __init__(self):
        super().__init__()
        self.results = []
        self._in_link = False
        self._in_snippet = False
        self._current_url = ""
        self._current_title = ""
        self._current_snippet = ""

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == "a" and attrs_d.get("class", "").startswith("result__a"):
            href = attrs_d.get("href", "")
            self._current_url = self._unwrap_ddg_redirect(href)
            self._current_title = ""
            self._in_link = True
        elif tag == "a" and attrs_d.get("class", "") == "result__snippet":
            self._in_snippet = True

    def handle_endtag(self, tag):
        if tag == "a" and self._in_link:
            self._in_link = False
        if tag == "a" and self._in_snippet:
            self._in_snippet = False
            if self._current_url and self._current_title:
                self.results.append(
                    {
                        "title": self._current_title.strip(),
                        "url": self._current_url,
                        "snippet": self._current_snippet.strip(),
                    }
                )
            self._current_url = ""
            self._current_title = ""
            self._current_snippet = ""

    def handle_data(self, data):
        if self._in_link:
            self._current_title += data
        if self._in_snippet:
            self._current_snippet += data

    @staticmethod
    def _unwrap_ddg_redirect(href):
        # DDG HTML results link through //duckduckgo.com/l/?uddg=<encoded url>
        if "uddg=" in href:
            parsed = urllib.parse.urlparse(href)
            params = urllib.parse.parse_qs(parsed.query)
            if "uddg" in params:
                return urllib.parse.unquote(params["uddg"][0])
        return href


def _search_duckduckgo_html(query, timeout, verify_ssl):
    """Scrape DuckDuckGo's HTML endpoint for general web results."""
    params = urllib.parse.urlencode({"q": query, "kl": "us-en"})
    url = "https://html.duckduckgo.com/html/?" + params

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": _USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )

    with urllib.request.urlopen(
        req, context=_ssl_context(verify_ssl), timeout=timeout
    ) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        html_text = response.read().decode(charset, errors="replace")

    parser = _ResultExtractor()
    try:
        parser.feed(html_text)
    except Exception:
        pass

    if not parser.results:
        return ""

    lines = []
    for i, r in enumerate(parser.results[:10], 1):
        title = r["title"] or r["url"]
        lines.append(
            "{0}. **{1}**\n   {2}  \n   {3}".format(
                i, title, r["url"], r["snippet"]
            )
        )
    return "\n\n".join(lines)


def _search_duckduckgo_instant(query, timeout, verify_ssl):
    """Search using DuckDuckGo Instant Answer API (free, no API key)."""
    params = urllib.parse.urlencode({"q": query, "format": "json"})
    url = "https://api.duckduckgo.com/?" + params

    req = urllib.request.Request(
        url, headers={"User-Agent": _USER_AGENT}
    )

    with urllib.request.urlopen(
        req, context=_ssl_context(verify_ssl), timeout=timeout
    ) as response:
        raw = response.read().decode("utf-8")
        if not raw.strip():
            return ""
        data = json.loads(raw)

    parts = []
    heading = data.get("Heading", "")
    if heading:
        parts.append("**{0}**".format(heading))

    abstract = data.get("Abstract", "")
    abstract_url = data.get("AbstractURL", "")
    if abstract:
        parts.append(abstract)
        if abstract_url:
            parts.append("Source: {0}".format(abstract_url))

    answer = data.get("Answer", "")
    if answer:
        parts.append("**Answer**: {0}".format(answer))
        atype = data.get("AnswerType", "")
        if atype:
            parts.append("Type: {0}".format(atype))

    definition = data.get("Definition", "")
    if definition:
        parts.append("**Definition**: {0}".format(definition))

    topics = data.get("RelatedTopics", [])
    result_lines = []
    for topic in topics:
        if not isinstance(topic, dict):
            continue
        if "Topics" in topic:
            for subtopic in topic.get("Topics", []):
                if isinstance(subtopic, dict):
                    t = subtopic.get("Text", "")
                    u = subtopic.get("FirstURL", "")
                    if t and u:
                        result_lines.append("- [{0}]({1})".format(t, u))
        else:
            t = topic.get("Text", "")
            u = topic.get("FirstURL", "")
            if t and u:
                result_lines.append("- [{0}]({1})".format(t, u))

    if result_lines:
        parts.append(
            "### Related Topics\n\n{0}".format("\n".join(result_lines[:15]))
        )

    if not parts:
        return ""

    return "\n\n".join(parts)


def _search_duckduckgo(query, timeout, verify_ssl):
    """Search DuckDuckGo: try HTML endpoint first, fall back to Instant Answer.

    The Instant Answer API only returns curated answers for a narrow set of
    queries. The HTML endpoint returns general search results for any query.
    """
    try:
        html_result = _search_duckduckgo_html(query, timeout, verify_ssl)
        if html_result:
            return html_result
    except (urllib.error.URLError, socket.timeout, Exception) as e:
        print("[Claudette] DuckDuckGo HTML search failed: {0}".format(e))

    try:
        instant_result = _search_duckduckgo_instant(
            query, timeout, verify_ssl
        )
        if instant_result:
            return instant_result
    except (urllib.error.URLError, socket.timeout, Exception) as e:
        print("[Claudette] DuckDuckGo Instant Answer failed: {0}".format(e))

    return 'No results found for "{0}".'.format(query)


def _search_searxng(query, instance_url, timeout, verify_ssl):
    """Search using a SearXNG instance (free, open source)."""
    params = urllib.parse.urlencode({"q": query, "format": "json"})
    url = instance_url.rstrip("/") + "/search?" + params

    req = urllib.request.Request(
        url, headers={"User-Agent": _USER_AGENT}
    )

    with urllib.request.urlopen(
        req, context=_ssl_context(verify_ssl), timeout=timeout
    ) as response:
        data = json.loads(response.read().decode("utf-8"))

    results = data.get("results", [])
    if not results:
        return 'No results found for "{0}".'.format(query)

    lines = []
    for i, r in enumerate(results[:10], 1):
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content") or r.get("snippet", "")
        lines.append(
            "{0}. **{1}**\n   {2}  \n   {3}".format(i, title, url, snippet)
        )

    return "\n\n".join(lines)


def run_web_search(
    query,
    backend="duckduckgo",
    searxng_instance=None,
    timeout=20,
    verify_ssl=True,
):
    """Search the web and return formatted results.

    Args:
        query: Search query string.
        backend: "duckduckgo" or "searxng".
        searxng_instance: URL of SearXNG instance (for searxng backend).
        timeout: Request timeout in seconds.
        verify_ssl: Whether to verify SSL certificates.

    Returns:
        str: Formatted search results or error message starting with "Error".
    """
    if not query or not isinstance(query, str) or not query.strip():
        return "Error: Empty search query."

    query = query.strip()

    try:
        if backend == "searxng":
            instance = searxng_instance or "https://searx.be"
            return _search_searxng(query, instance, timeout, verify_ssl)
        else:
            return _search_duckduckgo(query, timeout, verify_ssl)

    except urllib.error.HTTPError as e:
        return "Error: HTTP {0} — {1}".format(e.code, e.reason)
    except urllib.error.URLError as e:
        return "Error: Could not connect — {0}".format(e.reason)
    except socket.timeout:
        return "Error: Request timed out."
    except Exception as e:
        return "Error: {0}".format(str(e))
