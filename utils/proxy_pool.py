import random
import os
import requests
from utils.logger import logger
import utils.config  # Loads the project .env file.

# 留空 = 不用代理（最稳）
PROXIES = []

def get_random_proxy():
    if not PROXIES:
        logger.info("代理池为空，使用本地IP")
        return None
    random.shuffle(PROXIES)
    test_url = "https://movie.douban.com/robots.txt"
    timeout = 3
    for proxy in PROXIES:
        try:
            resp = requests.get(
                test_url,
                proxies=proxy,
                timeout=timeout,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"},
                verify=False
            )
            if resp.status_code == 200:
                logger.info(f"代理有效：{proxy}")
                return proxy
        except Exception:
            continue
    logger.warning("无有效代理，使用本地IP")
    return None

def load_cookies():
    """Return cookies from the optional local Cookie header value."""
    from http.cookies import SimpleCookie

    cookies = SimpleCookie()
    cookies.load(os.getenv("DOUBAN_COOKIE", ""))
    return {name: morsel.value for name, morsel in cookies.items()}
