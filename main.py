import os
from dotenv import load_dotenv
from agents.web_search_agent import run_web_search_agent
from agents.paper_search_agent import run_paper_search_agent
from agents.report_compiler import compile_report
from utils.report_writer import save_report

load_dotenv()

def run_research_engine(topic: str):
   print(f"\n{'='*50}")
   print(f"  Agentic Research Engine")
   print(f"  Topic: {topic}")
   print(f"{'='*50}\n")

   #run agents
   web_data = run_web_search_agent(topic)
   paper_data = run_paper_search_agent(topic)

   #compile report
   report_content = compile_report(
       topic=topic,
       web_results=web_data["web_results"],
       papers=paper_data["papers"]
   )

   #save
   output_path = save_report(topic, report_content)

   print(f"\nDone! Report saved to: {output_path}")
   print("\n--- REPORT PREVIEW ---")
   print(report_content[:1000])
   print("...")

if __name__ == "__main__":
   topic = input("Enter a research topic: ")
   run_research_engine(topic)
