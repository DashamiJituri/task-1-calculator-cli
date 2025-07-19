import requests
from bs4 import BeautifulSoup

# Target news website (you can change this to any reliable news source)
url = 'https://www.bbc.com/news'

# Add user-agent to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0'
}

# Send a GET request to fetch the HTML content
response = requests.get(url, headers=headers)

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all h1 and h2 headline tags
headline_tags = soup.find_all(['h1', 'h2'])

# Extract and write the text of each headline to a .txt file
with open('headlines.txt', 'w', encoding='utf-8') as file:
    for tag in headline_tags:
        headline = tag.get_text(strip=True)
        if headline:
            file.write(headline + '\n')

print("✅ Headlines saved to headlines.txt")
