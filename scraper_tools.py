import httpx
from bs4 import BeautifulSoup


def scrape_url(url: str) -> dict:
   #scrape text content from a given URL
   try:
       headers = {"User-Agent": "Mozilla/5.0 (ResearchBot/1.0)"}
       response = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
       soup = BeautifulSoup(response.text, "html.parser")


       # Remove scripts and styles
       for tag in soup(["script", "style", "nav", "footer"]):
           tag.decompose()


       title = soup.title.string if soup.title else "No title"
       text = soup.get_text(separator="\n", strip=True)


       # Limit to first 3000 chars to avoid overloading the LLM
       return {
           "url": url,
           "title": title,
           "content": text[:3000]
       }
   except Exception as e:
       return {"url": url, "title": "Error", "content": f"Failed to scrape: {e}"}
