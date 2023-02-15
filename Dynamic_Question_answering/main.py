from transformers import pipeline
import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from googlesearch import search
import wikipedia
import re


# Load the question-answering pipeline
nlp = pipeline("question-answering")


# Download the required resources for the chatbot
nltk.download("punkt")
nltk.download("stopwords")

# Define the chatbot's responses to different user inputs
responses = {
    "hi": "Hello, how can I help you?",
    "bye": "Goodbye!",
}


# Define a function that searches the web for the query and returns the top result
def nlu(query):
    # Send a GET request to Google's search engine with the query


    url = 'http://localhost:5005/model/parse'
    payload = {"text": query}


    x = requests.post(url, json=payload)
    # print(x.json(), flush=True)
    topic = ''

    for y in x.json()["entities"]:
        if y["entity"] == 'topic':
            topic = y["value"]


    if topic != '' :

        print("Searching for : ", topic)

    # print(search_results[0])

    return topic


# Define a function that extracts relevant text from a webpage
def extract_text(topic):
    # Send a GET request to the webpage
    response = requests.get("https://en.wikipedia.org/wiki/"+topic)


    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Remove the HTML tags and extract the text


    paras = []
    for paragraph in soup.find_all('p'):
        paras.append(str(paragraph.text))




    # Interleave paragraphs & headers
    text = ' '.join(paras)

    # Drop footnote superscripts in brackets
    text = re.sub(r"\[.*?\]+", '', text)

    # Replace '\n' (a new line) with '' and end the string at $1000.
    text = text.replace('\n', '')[:-11]
    # Tokenize the text into sentences and remove stop words

    # print(text)
    # stop_words = set(stopwords.words("english"))
    # sentences = sent_tokenize(text)
    # filtered_sentences = []
    # for sentence in sentences:
    #     print(sentence)
    #     words = word_tokenize(sentence)
    #     filtered_words = [word.lower() for word in words if word.lower() not in stop_words]
    #     filtered_sentence = " ".join(filtered_words)
    #     if filtered_sentence:
    #         filtered_sentences.append(filtered_sentence)

    return text



# Start the chatbot
print("Hello, how can I help you?")
while True:
    user_input = input("You: ").lower()

    # Check if the user said "bye" to end the conversation
    if user_input == "bye":
        print(responses[user_input])
        break

    # Check if the user said "hi" to greet the chatbot
    if user_input in responses:
        print(responses[user_input])
        continue

    # If the user didn't say "hi" or "bye", search the web for the query
    topic  = nlu(user_input)
    if topic  != '':
        # Extract relevant text from the webpage

        relevant_text = extract_text(topic)

        if relevant_text != "":
            # print(relevant_text)
            if relevant_text:
                result = nlp(question=user_input, context=relevant_text)

                print(f"I found this information for you: {result['answer']}")
            else:
                print("Sorry, I couldn't find any relevant information.")

    else:
        print("Sorry, I couldn't find any results.")

