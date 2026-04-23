from tools.search_tools import web_search


def run_web_search_agent(topic: str, max_results: int = 5):


   search_results = web_search(topic, max_results=max_results)


   results = search_results.get("web_results", []) if isinstance(search_results, dict) else []


   cleaned_results = []


   for r in results:
       if not isinstance(r, dict):
           continue


       cleaned_results.append({
           "title": r.get("title") or "No title",
           "url": r.get("url") or "",
           "content": r.get("content") or "",
           "full_content": r.get("full_content") or ""
       })


   return {"web_results": cleaned_results}
