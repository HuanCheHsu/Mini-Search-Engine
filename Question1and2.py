import os
import requests

#Question 1

countries = [
    "Canada",
    "United_States",
    "Mexico",
    "United_Kingdom",
    "France",
    "Germany",
    "China",
    "Japan",
    "India",
    "Brazil"
]

output_dir = 'country_html_files'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def save_country_html(country_name):
    url = f"https://en.wikipedia.org/wiki/{country_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        file_path = os.path.join(output_dir, f"{country_name}.html")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Saved {country_name} page successfully.")
    else:
        print(f"Failed to retrieve page for {country_name}")

for country in countries:
    save_country_html(country)



#Question 2

import os
from bs4 import BeautifulSoup
import nltk

# Directory containing the HTML files
input_dir = 'country_html_files'

def extract_descriptive_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    content_div = soup.find('div', class_='mw-parser-output')
    
    paragraphs = content_div.find_all('p', recursive=False)
    descriptive_content = ' '.join([para.get_text() for para in paragraphs[:2]])  # Extract first two paragraphs
    
    return descriptive_content

def tokenize_content(content):
    sentences = nltk.sent_tokenize(content)
    words = [nltk.word_tokenize(sentence) for sentence in sentences]
    return words

def process_country_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    descriptive_content = extract_descriptive_content(html_content)
    tokenized_words = tokenize_content(descriptive_content)
    
    return tokenized_words

# Process each HTML file in the directory
for filename in os.listdir(input_dir):
    if filename.endswith('.html'):
        file_path = os.path.join(input_dir, filename)
        country_name = filename.replace('.html', '')
        
        tokenized_words = process_country_html(file_path)
        
        # Print or save the tokenized words as needed
        print(f"Tokenized words for {country_name}:")
        for sentence in tokenized_words:
            print(sentence)
