import os
from bs4 import BeautifulSoup
import nltk
from collections import defaultdict

nltk.download('punkt')

input_dir = 'country_html_files'

def extract_descriptive_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    content_div = soup.find('div', class_='mw-parser-output')
    
    if content_div:
        paragraphs = content_div.find_all('p', recursive=False)
        descriptive_content = ' '.join([para.get_text() for para in paragraphs[:2]])  # Extract first two paragraphs
        return descriptive_content
    else:
        return ""

def tokenize_content(content):
    words_with_positions = []
    sentences = nltk.sent_tokenize(content)
    position = 0
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        for word in words:
            words_with_positions.append((word.lower(), position))
            position += 1
    return words_with_positions

def process_country_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    descriptive_content = extract_descriptive_content(html_content)
    tokenized_words_with_positions = tokenize_content(descriptive_content)
    
    return tokenized_words_with_positions

def create_inverted_index(countries):
    inverted_index = defaultdict(lambda: defaultdict(list))
    
    for country in countries:
        file_path = os.path.join(input_dir, f"{country}.html")
        tokenized_words_with_positions = process_country_html(file_path)
        
        for word, position in tokenized_words_with_positions:
            inverted_index[word][country].append(position)
    
    return inverted_index

#Question 4 keyword search
def country_search(keyword):
    keyword = keyword.lower()
    if keyword in inverted_index:
        documents = inverted_index[keyword].keys()
        return list(documents)
    else:
        return []

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

inverted_index = create_inverted_index(countries)

for word, postings in inverted_index.items():
    print(f"Word: {word}")
    for country, positions in postings.items():
        print(f"  {country}: {len(positions)} occurrences at positions {positions}")

#Keyword example
search_keyword = 'Toronto'
result = country_search(search_keyword)
print(f"Documents containing '{search_keyword}': {result}")