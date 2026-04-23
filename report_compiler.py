import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()


def compile_report(topic, web_results, papers):


   genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


   model = genai.GenerativeModel("gemini-2.5-flash-lite")


   #web context
   web_context = ""
   for i, w in enumerate(web_results, 1):
       if not isinstance(w, dict):
           continue


       web_context += f"\n--- Web Source {i}: {w.get('title')} ---\n"
       web_context += f"{w.get('content')}\n"


   #paper context
   paper_context = ""
   for i, p in enumerate(papers, 1):
       if not isinstance(p, dict):
           continue


       paper_context += f"\n--- Paper {i}: {p.get('title')} ({p.get('published')}) ---\n"
       paper_context += f"{p.get('summary')}\n"


   #prompt
   prompt = f"""
   Write a detailed research report on: {topic}


   Use the following sources:


   WEB SOURCES:
   {web_context}


   RESEARCH PAPERS:
   {paper_context}


   The report should include:
   - Introduction
   - Key Concepts
   - Recent Developments
   - Applications
   - Conclusion
   """


   try:
       response = model.generate_content(prompt)
       return response.text
   except Exception as e:
       return f"Error generating report: {e}"
