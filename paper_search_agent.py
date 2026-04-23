from tools.search_tools import arxiv_search


def run_paper_search_agent(topic: str, max_results: int = 5):


   search_results = arxiv_search(topic, max_results=max_results)


   papers = search_results.get("papers", []) if isinstance(search_results, dict) else []


   cleaned_papers = []


   for p in papers:
       if not isinstance(p, dict):
           continue


       cleaned_papers.append({
           "title": p.get("title") or "No title",
           "authors": p.get("authors") or "",
           "summary": p.get("summary") or "",
           "url": p.get("url") or "",
           "published": p.get("published") or ""
       })


   return {"papers": cleaned_papers}
