import asyncio
import ipaddress
import logging
import re
from urllib.parse import urlparse
from collections.abc import Mapping

from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader


logger = logging.getLogger(__name__)

MAX_CONCURRENT_LOADS = 5
REQUEST_TIMEOUT_SECONDS = 15
MIN_ARTICLE_LENGTH = 300
BLOCKED_HOSTNAMES = frozenset({"localhost", "localhost.localdomain"})


def _is_allowed_url(value: object) -> bool:
    if not isinstance(value, str):
        return False

    parsed = urlparse(value)
    hostname = parsed.hostname
    if parsed.scheme not in {"http", "https"} or not hostname or parsed.username:
        return False

    normalized_hostname = hostname.rstrip(".").lower()
    if normalized_hostname in BLOCKED_HOSTNAMES:
        return False

    try:
        address = ipaddress.ip_address(normalized_hostname)
    except ValueError:
        return True

    return not (address.is_private or address.is_loopback or address.is_link_local)


async def load_articles(search_results: list[dict]) -> list[Document]:
    """Load valid article URLs concurrently and return usable document text."""
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_LOADS)

    async def fetch_one(url: str, meta: Mapping[str, object]) -> Document | None:
        if not _is_allowed_url(url):
            logger.warning("Skipping invalid or unsafe article URL: %s", url)
            return None

        domain = urlparse(url).hostname or ""
        if domain.lower().endswith(("youtube.com", "youtu.be")):
            logger.info("Skipping non-article URL: %s", url)
            return None

        async with semaphore:
            try:
                loader = WebBaseLoader(
                    web_paths=(url,),
                    requests_kwargs={"timeout": REQUEST_TIMEOUT_SECONDS},
                    raise_for_status=True,
                )
                docs = await asyncio.to_thread(loader.load)

                if not docs or not docs[0].page_content:
                    logger.info("Skipping empty article: %s", url)
                    return None

                content = re.sub(r"\s+", " ", docs[0].page_content).strip()
                if len(content) < MIN_ARTICLE_LENGTH:
                    logger.info("Skipping short article: %s", url)
                    return None

                docs[0].page_content = content
                docs[0].metadata.update(dict(meta))
                logger.info("Loaded article: url=%s characters=%d", url, len(content))
                return docs[0]
            except Exception:
                logger.exception("Could not load article: %s", url)
        return None

    tasks = []
    for result in search_results:
        url = result.get("url") if isinstance(result, Mapping) else None
        if isinstance(url, str):
            tasks.append(fetch_one(url, result))
        else:
            logger.warning("Skipping search result without a valid URL")

    results = await asyncio.gather(*tasks)
    articles = [a for a in results if a is not None]
    logger.info("Finished loading articles: count=%d", len(articles))
    return articles
