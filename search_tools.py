import os
from tavily import TavilyClient
from dotenv import load_dotenv
import arxiv


load_dotenv()


#Tavily web search
def web_search(query: str, max_results: int = 5):


   api_key = os.getenv("TAVILY_API_KEY")


   if not api_key:
       raise ValueError("TAVILY_API_KEY not found in .env")


   client = TavilyClient(api_key=api_key)


   try:
       response = client.search(
           query=query,
           max_results=max_results,
           search_depth="advanced"
       )
   except Exception as e:
       print(f"Tavily error: {e}")
       return {"web_results": []}


   results = response.get("results", []) or []


   formatted_results = []


   for r in results:
       if not isinstance(r, dict):
           continue


       formatted_results.append({
           "title": r.get("title") or "No title",
           "url": r.get("url") or "",
           "content": r.get("content") or "",
           "full_content": (r.get("raw_content") or "")[:3000]
       })


   return {"web_results": formatted_results}


#arXiv paper search
def arxiv_search(query: str, max_results: int = 5):


   try:
       search = arxiv.Search(
           query=query,
           max_results=max_results,
           sort_by=arxiv.SortCriterion.Relevance
       )


       papers = []


       for paper in search.results():
           papers.append({
               "title": paper.title or "No title",
               "authors": ", ".join([a.name for a in paper.authors]) if paper.authors else "",
               "summary": (paper.summary or "")[:2000],
               "url": paper.entry_id or "",
               "published": str(paper.published.date()) if paper.published else ""
           })


       return {"papers": papers}


   except Exception as e:
       print(f"arXiv error: {e}")
       return {"papers": []}
