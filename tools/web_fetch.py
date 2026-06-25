"""
Web Fetch tool executor — fetches URL content and extracts text.
Works with all API providers (Anthropic, DeepSeek, OpenRouter, etc.).
"""

import html.parser
import socket
import ssl
import urllib.error
import urllib.request


class _HTMLTextExtractor(html.parser.HTMLParser):
    """Extract visible text from HTML, skipping script/style blocks."""

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip = 0
        self._skip_tags = {"script", "style", "noscript", "head", "title"}

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self._skip_tags:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag.lower() in self._skip_tags and self.skip > 0:
            self.skip -= 1

    def handle_data(self, data):
        if self.skip == 0:
            text = data.strip()
            if text:
                self.text_parts.append(text)


_MAX_BYTES = 1 * 1024 * 1024  # 1MB


def run_web_fetch(url, timeout=15, verify_ssl=True):
    """Fetch a URL and return extracted text content.

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.
        verify_ssl: Whether to verify SSL certificates.

    Returns:
        str: Extracted text content or error message.
    """
    if not url or not isinstance(url, str):
        return "Error: Invalid URL."

    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Claudette/1.0"},
        )

        if verify_ssl:
            ssl_context = ssl.create_default_context()
        else:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(
            req, context=ssl_context, timeout=timeout
        ) as response:
            content_type = response.headers.get("Content-Type", "").lower()

            raw = response.read(_MAX_BYTES)
            truncated = len(raw) >= _MAX_BYTES

            try:
                charset = response.headers.get_content_charset() or "utf-8"
                html = raw.decode(charset, errors="replace")
            except (UnicodeDecodeError, LookupError):
                html = raw.decode("utf-8", errors="replace")

            if "text/html" in content_type:
                extractor = _HTMLTextExtractor()
                try:
                    extractor.feed(html)
                except Exception:
                    pass
                text = "\n".join(extractor.text_parts)
            elif "text/" in content_type:
                text = html
            else:
                return (
                    "Error: Cannot fetch this content type ({0}). "
                    "Only text and HTML pages are supported.".format(
                        content_type.split(";")[0]
                    )
                )

            if truncated:
                text += "\n\n[Content truncated at 1 MB]"

            if not text.strip():
                return "Error: No readable text found on this page."

            # Limit total returned text to avoid blowing up context
            if len(text) > 80000:
                text = text[:80000] + "\n\n[Content truncated at 80,000 characters]"

            return text

    except urllib.error.HTTPError as e:
        return "Error: HTTP {0} — {1}".format(e.code, e.reason)
    except urllib.error.URLError as e:
        return "Error: Could not connect — {0}".format(e.reason)
    except socket.timeout:
        return "Error: Request timed out after {0} seconds.".format(timeout)
    except Exception as e:
        return "Error: {0}".format(str(e))
