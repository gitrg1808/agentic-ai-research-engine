from dotenv import load_dotenv
load_dotenv()


import streamlit as st
import os
import time
from agents.web_search_agent import run_web_search_agent
from agents.paper_search_agent import run_paper_search_agent
from agents.report_compiler import compile_report
from utils.report_writer import save_report


#page configuration
st.set_page_config(
   page_title="AI Research Engine",
   page_icon="🔬",
   layout="wide"
)


st.title("🔬 Agentic AI Research Engine")
st.caption("Searches the web, finds research papers, and compiles a full report — automatically.")


#sidebar
with st.sidebar:
   st.header("⚙️ Settings")
   max_web   = st.slider("Web results to fetch", 3, 10, 5)
   max_paper = st.slider("Research papers to fetch", 3, 10, 5)
   st.divider()
   st.markdown("**Free APIs used:**")
   st.markdown("- 🔍 Tavily (web search)")
   st.markdown("- 📄 arXiv (research papers)")
   st.markdown("- 🤖 Gemini Flash-Lite (report generation)")
   st.divider()
   st.info("Reports are saved to the `reports/` folder.")


#main input
topic = st.text_input(
   "Enter a research topic:",
   placeholder="e.g. Quantum computing, Large language models, CRISPR gene editing..."
)


run_btn = st.button("🚀 Generate Report", type="primary", use_container_width=True)


#run pipeline
if run_btn and topic.strip():
   st.divider()


   #progress display
   progress = st.progress(0, text="Starting research engine...")
   status   = st.status("Running agents...", expanded=True)


   with status:
       #step 1: web search
       st.write("🔍 Searching the web with Tavily...")
       progress.progress(15, text="Searching the web...")
       web_data = run_web_search_agent(topic)
       st.write(f"✅ Found {len(web_data['web_results'])} web sources")


       #step 2: paper search
       st.write("📄 Searching arXiv for research papers...")
       progress.progress(40, text="Fetching research papers...")
       paper_data = run_paper_search_agent(topic)
       st.write(f"✅ Found {len(paper_data['papers'])} research papers")


       #step 3: compile report
       st.write("🤖 Compiling report with Gemini...")
       progress.progress(70, text="Generating report...")
       report_content = compile_report(
           topic=topic,
           web_results=web_data["web_results"],
           papers=paper_data["papers"]
       )


       #step 4: save files
       st.write("💾 Saving report files...")
       progress.progress(90, text="Saving files...")
       md_path, pdf_path = save_report(topic, report_content)


       progress.progress(100, text="Done!")
       status.update(label="✅ Research complete!", state="complete")


   st.success(f"Report generated for: **{topic}**")
   st.divider()


   #display report
   col1, col2 = st.columns([3, 1])


   with col1:
       st.subheader("📋 Report Preview")
       st.markdown(report_content)


   with col2:
       st.subheader("📥 Downloads")


       #PDF download
       with open(pdf_path, "rb") as f:
           st.download_button(
               label="⬇️ Download PDF",
               data=f,
               file_name=os.path.basename(pdf_path),
               mime="application/pdf",
               use_container_width=True
           )


       #markdown download
       with open(md_path, "r", encoding="utf-8") as f:
           st.download_button(
               label="⬇️ Download Markdown",
               data=f,
               file_name=os.path.basename(md_path),
               mime="text/markdown",
               use_container_width=True
           )


       st.divider()
       st.subheader("🗂 Sources Found")
       st.markdown(f"**Web sources:** {len(web_data['web_results'])}")
       for r in web_data["web_results"]:
           st.markdown(f"- [{r['title'][:50]}...]({r['url']})")


       st.divider()
       st.markdown(f"**Research papers:** {len(paper_data['papers'])}")
       for p in paper_data["papers"]:
           st.markdown(f"- [{p['title'][:50]}...]({p['url']})")


elif run_btn and not topic.strip():
   st.warning("Please enter a research topic first.")
