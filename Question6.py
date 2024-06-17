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

def edit_distance(str1, str2):
    len1, len2 = len(str1), len(str2)
    
    # Create a matrix to store distances
    dp = [[0 for _ in range(len2 + 1)] for _ in range(len1 + 1)]
    
    # Initialize the matrix
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j
    
    # Compute the edit distance
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],    # Deletion
                                   dp[i][j - 1],    # Insertion
                                   dp[i - 1][j - 1])  # Substitution
    
    return dp[len1][len2]

def country_search(keyword):
    keyword = keyword.lower()
    if keyword in inverted_index:
        documents = inverted_index[keyword].keys()
        return list(documents)
    else:
        return []

def fuzzy_search(keyword):
    keyword = keyword.lower()
    min_distance = float('inf')
    closest_word = None
    
    for word in inverted_index.keys():
        distance = edit_distance(keyword, word)
        if distance < min_distance:
            min_distance = distance
            closest_word = word
    
    if closest_word:
        return list(inverted_index[closest_word].keys())
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

# Test the fuzzy_search function
search_keyword = 'Toronta'
result = fuzzy_search(search_keyword)
print(f"Documents containing similar word to '{search_keyword}': {result}")
