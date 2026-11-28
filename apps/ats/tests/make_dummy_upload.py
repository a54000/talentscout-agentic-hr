"""Make a dummy bulk-upload batch: spreadsheet + fake CVs (.docx) + a fake JD. Synthetic data only.

Usage:
  python tests/make_dummy_upload.py --rows 50 --title "TEST - Dummy Cloud Architect" --out dummy_upload

Every candidate email ends in @example.com (a reserved test domain), so the test rows are easy
to find and remove afterwards. Create a Requirement with exactly the --title first.
"""
import argparse
import csv
import io
import os
import random
import zipfile

FIRST = ["Aarav", "Vivaan", "Aditya", "Ishaan", "Kabir", "Ananya", "Diya", "Saanvi", "Meera", "Riya",
         "Arjun", "Rohan", "Kavya", "Nisha", "Pooja", "Rahul", "Sneha", "Varun", "Tanvi", "Neel"]
LAST = ["Testwala", "Dummyraj", "Sampleton", "Fakeman", "Mockkar", "Demosingh", "Trialdas", "Placeholdr"]
COMPANIES = ["Example Tech", "Sample Cloud Ltd", "Demo Systems", "Placeholder Infra", "Mock Analytics"]
SKILLS = ["AWS", "Terraform", "Kubernetes", "Networking", "Security", "Cloud Migration", "Disaster Recovery",
          "Python", "Docker", "CI/CD"]
CITIES = ["Gurgaon", "Noida", "Bengaluru", "Pune", "Hyderabad"]


def docx_bytes(lines):
    body = "".join(f"<w:p><w:r><w:t xml:space=\"preserve\">{line}</w:t></w:r></w:p>" for line in lines)
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                f"<w:body>{body}</w:body></w:document>")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8"?>'
                   '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/word/document.xml" '
                   'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                   '</Types>')
        z.writestr("word/document.xml", document)
    return buf.getvalue()


def pdf_bytes(lines, pages):
    """A multi-page text PDF like a real CV (needs reportlab, which the ATS already uses)."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    buf = io.BytesIO()
    pdf = canvas.Canvas(buf, pagesize=A4)
    filler = ("Led cloud migration and platform work: designed landing zones, automated infrastructure with Terraform, "
              "ran Kubernetes clusters, improved security posture and disaster recovery. ")
    for page in range(pages):
        y = 800
        for line in (lines if page == 0 else []) + [f"Project {page}.{n}: " + filler for n in range(12)]:
            for start in range(0, len(line), 95):
                pdf.drawString(40, y, line[start:start + 95])
                y -= 14
                if y < 60:
                    break
        pdf.showPage()
    pdf.save()
    return buf.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=20)
    parser.add_argument("--title", default="TEST - Dummy Cloud Architect")
    parser.add_argument("--out", default="dummy_upload")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--format", choices=["docx", "pdf"], default="docx",
                        help="pdf makes realistic multi-page CVs (needs reportlab)")
    parser.add_argument("--pages", type=int, default=3, help="pages per PDF CV")
    args = parser.parse_args()
    rng = random.Random(args.seed)
    tag = f"{rng.randrange(16**4):04x}"
    os.makedirs(os.path.join(args.out, "cvs"), exist_ok=True)

    header = ["Candidate Name", "Email", "Phone", "Current Company", "Current Role", "Experience (Years)",
              "Key Skills", "Notice Period", "Current Salary", "Expected Salary", "Current Location",
              "Preferred Location", "Requirement"]
    rows = []
    for i in range(args.rows):
        name = f"{rng.choice(FIRST)} {rng.choice(LAST)}{i}"
        email = f"dummy.{tag}.{i}@example.com"
        phone = f"9{rng.randrange(10**9):09d}"
        company = rng.choice(COMPANIES)
        years = rng.randint(8, 18)
        skills = ", ".join(rng.sample(SKILLS, 5))
        city = rng.choice(CITIES)
        notice = rng.choice(["15 days", "30 days", "60 days", "Serving notice"])
        ctc, ectc = rng.randint(25, 45), rng.randint(35, 55)
        rows.append([name, email, phone, company, "Cloud Architect", years, skills, notice, ctc, ectc, city,
                     "Gurgaon", args.title])
        cv = [name, f"Email: {email}", f"Phone: {phone}", f"Location: {city}",
              f"Cloud Architect at {company} ({years} years of experience)",
              f"Skills: {skills}",
              "DUMMY CV for testing only - not a real person."]
        ext = args.format
        with open(os.path.join(args.out, "cvs", f"{name.replace(' ', '_')}.{ext}"), "wb") as f:
            f.write(pdf_bytes(cv, args.pages) if ext == "pdf" else docx_bytes(cv))

    with open(os.path.join(args.out, "candidates.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    with open(os.path.join(args.out, f"{args.title}.docx"), "wb") as f:
        f.write(docx_bytes([args.title, "DUMMY JD for testing only.",
                            "Experience: 12-18 years. Location: Gurgaon. Notice: 30 days max.",
                            "Must have: AWS, Terraform, Kubernetes, networking, security, cloud migration, disaster recovery."]))
    print(f"Wrote {args.rows} dummy candidates (emails dummy.{tag}.*@example.com) to {args.out}/")


if __name__ == "__main__":
    main()
