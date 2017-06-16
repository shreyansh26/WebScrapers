"""
 Usage in terminal: python wikiTopWords.py batman yes / python wikiTopWords.py batman
                      ( For removing stop words)        (For not removing stop words)
"""

# Dependencies
import requests
from bs4 import BeautifulSoup
import re
import operator
import json  # to parse json
from tabulate import tabulate # make a nice table
import sys
from stop_words import get_stop_words

# get the words
def getWordList(url):
	word_list = []
	#raw_data
	source_code = requests.get(url)
	#convert to text
	plain_text = source_code.text
	#lxml format
	soup = BeautifulSoup(plain_text, 'lxml')

	#find the words in paragraph tag
	for text in soup.findAll('p'):
		if text.text is None:
			continue
		# content
		content = text.text
		# lowercase and split into array
		words = content.lower().split()
		# For each word
		for word in words:
			#remove non-chars
			cleaned_word = clean_word(word)
			#if there is still something there
			if(len(cleaned_word)>0):
				word_list.append(cleaned_word)

	return word_list


# Clean word
def clean_word(word):
	cleaned_word = re.sub('[^a-zA-Z]+', '', word)
	return cleaned_word

def createFrequencyTable(word_list):
	# word count
	word_count = {}
	for word in word_list:
		if word in word_count:
			word_count[word] += 1
		else:
			word_count[word] = 1

	return word_count

# Remove stop words
def remove_stop_words(frequency_list):
	stop_words = get_stop_words('en')

	temp_list = []
	for key,value in frequency_list:
		if key not in stop_words:
			temp_list.append([key, value])

	return temp_list

# Get data from Wikipedia
wikipedia_api_link = "https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch="
wikipedia_link = "https://en.wikipedia.org/wiki/"

if (len(sys.argv) < 2):
	print('Enter a valid string!')
	exit()

# Get the search word
string_query = sys.argv[1]

if(len(sys.argv) > 2):
	search_mode = True
else:
	search_mode = False

# Create our URL
url = wikipedia_api_link + string_query

try:
	response = requests.get(url)
	# Format the data
	data = json.loads(response.content.decode('utf-8'))

	wikipedia_page_tag = data['query']['search'][0]['title']

	# create new url
	url = wikipedia_link + wikipedia_page_tag
	page_word_list = getWordList(url)

	# create table of word counts
	page_word_count = createFrequencyTable(page_word_list)

	sorted_word_frequency_list = sorted(page_word_count.items(), key=operator.itemgetter(1), reverse=True)

	# Remove stop words
	if(search_mode):
		sorted_word_frequency_list = remove_stop_words(sorted_word_frequency_list)

	# Sum total words to calculate frequencies
	total_words_sum = 0
	for key, value in sorted_word_frequency_list:
		total_words_sum += value

	# Get the top 20 words
	if(len(sorted_word_frequency_list)>20):
		sorted_word_frequency_list = sorted_word_frequency_list[:20]

	# Create our final list
	final_list = []
	for key, value in sorted_word_frequency_list:
		percentage_value = float(value*100)/total_words_sum
		final_list.append([key, value, round(percentage_value, 4)])

	print_headers = ['Word', 'Frequency', 'Frequency Percentage']

	# Print table with tabulate
	print(tabulate(final_list, headers=print_headers, tablefmt='orgtbl'))

except requests.exceptions.Timeout:
	print("The server did not respond. Please try again!")
