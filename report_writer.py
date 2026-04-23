import os
from fpdf import FPDF


def save_report(topic, content):
   os.makedirs("reports", exist_ok=True)


   safe_topic = topic.replace(" ", "_")


   md_path = f"reports/{safe_topic}.md"
   pdf_path = f"reports/{safe_topic}.pdf"


   #save markdown
   with open(md_path, "w", encoding="utf-8") as f:
       f.write(content)


   #save PDF
   _save_pdf(topic, content, pdf_path)


   return md_path, pdf_path


def clean_text(text: str) -> str:
   replacements = {
       "•": "-",
       "–": "-",
       "—": "-",
       "’": "'",
       "“": '"',
       "”": '"',
       "\u00a0": " ",
   }


   for k, v in replacements.items():
       text = text.replace(k, v)


   return text.encode("latin-1", "ignore").decode("latin-1")


def safe_multi_cell(pdf, text, max_width=180):
   #manual line wrapping to avoid fpdf crashes
   words = text.split(" ")
   line = ""


   for word in words:
       test_line = line + (" " if line else "") + word


       if pdf.get_string_width(test_line) < max_width:
           line = test_line
       else:
           pdf.cell(0, 6, line, ln=True)
           line = word


   if line:
       pdf.cell(0, 6, line, ln=True)




#pdf generation
def _save_pdf(topic, content, path):


   pdf = FPDF()
   pdf.set_auto_page_break(auto=True, margin=15)
   pdf.add_page()


   #title
   pdf.set_font("Arial", "B", 16)
   safe_multi_cell(pdf, clean_text(topic))


   pdf.ln(5)


   #body
   pdf.set_font("Arial", size=10)


   for line in content.split("\n"):


       line = clean_text(line.strip())


       if not line:
           pdf.ln(3)
           continue


       #headings
       if line.startswith("#"):
           pdf.set_font("Arial", "B", 12)
           safe_multi_cell(pdf, line.replace("#", "").strip())
           pdf.set_font("Arial", size=10)


       #bullets
       elif line.startswith("-") or line.startswith("*"):
           clean = line[1:].strip()
           safe_multi_cell(pdf, "  -  " + clean)


       else:
           safe_multi_cell(pdf, line)


   pdf.output(path)
