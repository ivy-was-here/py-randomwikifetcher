import requests
import os
import re

# Paths for directories and files
output_dir = "generated_pages"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

css_path = "css/style.css"
logo_path = "imgs/logo.png"

CATEGORY_API_URL = "https://en.wikipedia.org/w/api.php"

# Function to sanitize filenames
def sanitize_filename(title):
    return re.sub(r'[\\/*?:"<>|]', "", title.replace(" ", "_"))

# Function to fetch articles by category
def fetch_articles_by_category(category):
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmlimit": 1  # Fetch only one article at a time
    }
    response = requests.get(CATEGORY_API_URL, params=params)
    try:
        response.raise_for_status()
        data = response.json()
        print(data)  # Debugging: Print the API response
        if "query" in data and "categorymembers" in data["query"] and data["query"]["categorymembers"]:
            first_result = data["query"]["categorymembers"][0]
            title = first_result["title"]
            return fetch_article_summary_by_title(title)
        else:
            print(f"No articles found in the category: {category}")
            return None
    except Exception as e:
        print(f"Error fetching category members: {e}")
        return None

# Function to fetch article summaries by title
def fetch_article_summary_by_title(title):
    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    response = requests.get(summary_url)
    if response.status_code == 200:
        data = response.json()
        return {
            "title": data.get("title", "Untitled"),
            "content": data.get("extract", "No content available."),
        }
    else:
        print(f"Error fetching article summary for {title}.")
        return None

# Function to create an HTML page
def create_html_page(title, content):
    sanitized_title = sanitize_filename(title)
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{css_path}">
</head>
<body>
<div class="container-fluid">
  <div class="row">
    <div class="col-xl-12">
      <img class="img-fluid" src="{logo_path}" width="100px" height="auto" alt="logo" style="margin-bottom: 35px;"/>
    </div>
  </div>
</div>
<div class="container">
  <div class="row">
    <div class="col-xl-2">
      <div class="contents">Contents</div>
    </div>
    <div class="col-xl-10">
      <div class="pageTitle">{title}</div>
      <div class="fromWiki">From Wikipedia, the free encyclopedia</div>
      <div class="infoBox">
        <div class="infoBoxTitle">{title} Overview</div>
      </div>
      <div class="bodyText">
        <p>{content}</p><br>
      </div>
    </div>
  </div>
</div>
<div class="copyright">Wikipedia - wikipedia.org | Chief Beef and the DOJO crew 2024.</div>
</body>
</html>"""

    # Save the HTML file
    file_name = f"{sanitized_title}.html"
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_template)
    print(f"Generated HTML page for '{title}' at {file_path}")

# Main function
def main():
    category = input("Enter the Wikipedia category (e.g., Geography_of_Donovia): ")
    article = fetch_articles_by_category(category)
    if article:
        title = article["title"]
        content = article["content"]
        create_html_page(title, content)

# Run the script
if __name__ == "__main__":
    main()
