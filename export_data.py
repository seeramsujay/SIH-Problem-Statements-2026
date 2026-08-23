import html
import json
import re
from bs4 import BeautifulSoup
import pandas as pd

ILLEGAL_CHARACTERS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
URL_PATTERN = re.compile(r"https?://[^\s<>\"\'\)]+")

def clean_cell_value(cell):
    """Clean and format cell content, parsing embedded HTML, decoding entities, and stripping illegal chars."""
    if not cell:
        return ""
    raw_html = cell.decode_contents() if hasattr(cell, "decode_contents") else str(cell)
    raw_html = html.unescape(raw_html)
    sub_soup = BeautifulSoup(raw_html, "html.parser")
    for br in sub_soup.find_all(["br", "p", "tr", "li"]):
        br.replace_with("\n" + br.text)

    text = sub_soup.get_text()
    text = html.unescape(text)
    text = (
        text.replace("â€”", "—")
        .replace("â€“", "–")
        .replace("â€™", "'")
        .replace("â€œ", '"')
        .replace("â€", '"')
        .replace("â€¢", "•")
        .replace("Â", "")
    )

    # Strip illegal control characters for Excel/openpyxl compatibility
    text = ILLEGAL_CHARACTERS_RE.sub("", text)

    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    return "\n".join(line for line in lines if line).strip()

def main():
    html_file = "website.html"
    with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    table = soup.find("table", {"id": "dataTablePS"})
    if not table:
        print("Error: dataTablePS not found in website.html")
        return

    tbody = table.find("tbody")
    rows = tbody.find_all("tr", recursive=False)
    print(f"Total rows found in dataTablePS: {len(rows)}")

    items = []
    for idx, row in enumerate(rows):
        tds = row.find_all("td", recursive=False)
        if len(tds) < 8:
            continue

        s_no = tds[0].get_text(strip=True)
        org_main = clean_cell_value(tds[1])
        category_main = tds[3].get_text(strip=True)
        ps_number = tds[4].get_text(strip=True)
        submitted_ideas = tds[5].get_text(strip=True)
        theme_main = tds[6].get_text(strip=True)
        deadline = tds[7].get_text(strip=True)

        modal = row.find("div", class_="modal")
        modal_dict = {}
        modal_links = {}
        if modal:
            modal_table = modal.find("table")
            if modal_table:
                for tr in modal_table.find_all("tr"):
                    cells = tr.find_all(["th", "td"])
                    if len(cells) >= 2:
                        k = cells[0].get_text(strip=True)
                        val = clean_cell_value(cells[1])
                        links = []
                        for a in cells[1].find_all("a"):
                            h = a.get("href", "").strip()
                            if (
                                h
                                and h not in [
                                    "#",
                                    "javascript:void(0);",
                                    "https://www.sih.gov.in/dataset/",
                                    "http://www.sih.gov.in/dataset/",
                                    "https://sih.gov.in/dataset/",
                                    "http://sih.gov.in/dataset/",
                                ]
                                and not h.rstrip("/").endswith("/dataset")
                            ):
                                links.append(h)
                        modal_dict[k] = val
                        if links:
                            modal_links[k] = links[0] if len(links) == 1 else links

        title = modal_dict.get("Problem Statement Title", "")
        if not title:
            title_link = tds[2].find("a", class_="cls_ps_title") or tds[2].find("a")
            title = clean_cell_value(title_link) if title_link else ""

        ps_id = modal_dict.get("Problem Statement ID", "")
        if not ps_id and ps_number.startswith("SIH"):
            ps_id = ps_number[3:]

        desc = modal_dict.get("Description", "")
        org = modal_dict.get("Organization", org_main)
        dept = modal_dict.get("Department", "")
        cat = modal_dict.get("Category", category_main)
        theme = modal_dict.get("Theme", theme_main)

        # Dataset details and embedded URL extraction
        raw_dataset = modal_dict.get("Dataset Link", "")
        if raw_dataset in [
            "https://www.sih.gov.in/dataset/",
            "http://www.sih.gov.in/dataset/",
            "https://sih.gov.in/dataset/",
            "http://sih.gov.in/dataset/",
        ]:
            raw_dataset = ""

        # Collect URLs from anchor tags and regex from text
        dataset_urls = []
        if modal_links.get("Dataset Link"):
            if isinstance(modal_links["Dataset Link"], list):
                dataset_urls.extend(modal_links["Dataset Link"])
            else:
                dataset_urls.append(modal_links["Dataset Link"])

        for u in URL_PATTERN.findall(raw_dataset):
            clean_u = u.rstrip(".,;)")
            if (
                clean_u not in dataset_urls
                and not clean_u.rstrip("/").endswith("/dataset")
                and clean_u not in ["https://www.sih.gov.in/dataset/", "http://www.sih.gov.in/dataset/"]
            ):
                dataset_urls.append(clean_u)

        # YouTube and contact info
        yt = modal_links.get("Youtube Link", modal_dict.get("Youtube Link", ""))
        if yt in ["#", "https://www.sih.gov.in/dataset/"]:
            yt = ""

        contact = modal_links.get("Contact info", modal_dict.get("Contact info", ""))
        if contact in ["#", "https://www.sih.gov.in/dataset/"]:
            contact = ""

        item = {
            "s_no": int(s_no) if s_no.isdigit() else s_no,
            "ps_number": ps_number,
            "ps_id": ps_id,
            "title": title,
            "organization": org,
            "department": dept,
            "category": cat,
            "theme": theme,
            "submitted_ideas_count": submitted_ideas,
            "deadline": deadline,
            "description": desc,
            "dataset_details": raw_dataset,
            "dataset_urls": dataset_urls,
            "youtube_link": yt,
            "contact_info": contact,
        }
        items.append(item)

    print(f"Successfully processed {len(items)} problem statements.")

    # Save to JSON
    json_path = "sih_problem_statements.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON to {json_path}")

    # Prepare DataFrame for CSV & Excel (convert list of URLs to string)
    df_rows = []
    for it in items:
        row_copy = dict(it)
        row_copy["dataset_urls"] = ", ".join(row_copy["dataset_urls"])
        df_rows.append(row_copy)

    df = pd.DataFrame(df_rows)
    csv_path = "sih_problem_statements.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved CSV to {csv_path}")

    excel_path = "sih_problem_statements.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"Saved Excel to {excel_path}")

if __name__ == "__main__":
    main()
