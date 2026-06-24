import requests
from bs4 import BeautifulSoup


def scrape_job(url):
    """
    Downloads a webpage and extracts useful text.
    Returns:
        title (str)
        description (str)
    """

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

    except Exception as e:
        return None, f"Error while opening URL:\n{e}"

    soup = BeautifulSoup(response.text, "html.parser")

    # ------------------------
    # Page Title
    # ------------------------

    title = ""

    if soup.title:
        title = soup.title.get_text(strip=True)

    # ------------------------
    # Remove unwanted tags
    # ------------------------

    for tag in soup([
        "script",
        "style",
        "noscript",
        "header",
        "footer",
        "nav"
    ]):
        tag.decompose()

    # ------------------------
    # Extract text
    # ------------------------

    text = soup.get_text(separator=" ")

    text = " ".join(text.split())

    return title, text