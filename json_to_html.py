import json
import os

# Path to the combined JSON file and where to save the generated HTML files
json_file_path = "/Users/Ivy/Desktop/scripts/content.json"
output_folder = "/Users/Ivy/Desktop/docxfilesnov/html_output"

# Check output folder
os.makedirs(output_folder, exist_ok=True)

# This is the HTML template/structure meant to be adhered to
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{title}}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
<div class="container-fluid">
  <div class="row">
    <div class="col-xl-12">
      <img class="img-fluid" src="imgs/logo.png" width="100px" height="auto" alt="logo" style="margin-bottom: 35px;"/>
    </div>
  </div>
</div>
<div class="container">
  <div class="row">
    <div class="col-xl-2">
      <div class="contents">Contents</div>
      {{contents_links}}
    </div>
    <div class="col-xl-10">
      <div class="pageTitke">{{title}}</div>
      <div class="fromWiki">From Wikipedia, the free encyclopedia</div>
      <div class="infoBox">
        <div class="infoBoxTitle">{{title}}</div>
        {{infobox_content}}
      </div>
      <div class="bodyText">{{body_content}}</div>
      {{sections}}
    </div>
  </div>
</div>
<div class="copyright">Wikipedia - wikipedia.org | Chief Beef and the DOJO crew 2024.</div>
</body>
</html>"""

def generate_html_from_json(content):
    for page in content:
        title = page.get("title", "Untitled")
        infobox_content = ""
        body_content = ""
        sections_html = ""
        contents_links = ""

        # Process infobox content if available
        if "infobox" in page:
            for item in page["infobox"]:
                key = item.get("key", "")
                value = item.get("value", "")
                infobox_content += f'<div class="infoBoxInfo"><strong>{key}</strong>: {value}</div>\n'

        # Process main body into text
        if "intro" in page:
            body_content = f"<p>{page['intro']}</p>"

        # Generate sidebar contents links and main sections IAW the document given
        for section in page.get("sections", []):
            section_header = section.get("header", "")
            section_content = section.get("content", "")
            section_id = section_header.lower().replace(" ", "_")
            contents_links += f'<div class="sectionLinks">&#8250; <a href="#{section_id}">{section_header}</a></div>\n'
            sections_html += f'<div id="{section_id}" class="sectionTitles">{section_header}</div>\n'
            sections_html += f'<div class="bodyText"><p>{section_content}</p></div>\n'

            # Process subsections if present
            for subsection in section.get("subsections", []):
                subsection_header = subsection.get("header", "")
                subsection_content = subsection.get("content", "")
                subsection_id = subsection_header.lower().replace(" ", "_")
                contents_links += f'<div class="subSectionLinks"><a href="#{subsection_id}">{subsection_header}</a></div>\n'
                sections_html += f'<div id="{subsection_id}" class="subSectionTitles">{subsection_header}</div>\n'
                sections_html += f'<div class="bodyText"><p>{subsection_content}</p></div>\n'

        # Replace template placeholders with actual content
        html_content = html_template.replace("{{title}}", title)
        html_content = html_content.replace("{{infobox_content}}", infobox_content)
        html_content = html_content.replace("{{body_content}}", body_content)
        html_content = html_content.replace("{{contents_links}}", contents_links)
        html_content = html_content.replace("{{sections}}", sections_html)

        # Define output path and write with UTF-8 encoding
        output_file_path = os.path.join(output_folder, title.replace(" ", "_") + ".html")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"Generated HTML for {title}")

# Read combined JSON content and generate HTML files IAW above
with open(json_file_path, "r", encoding="utf-8") as f:
    content = json.load(f)

generate_html_from_json(content)
