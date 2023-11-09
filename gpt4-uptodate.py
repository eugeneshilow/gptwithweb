import os
import openai
from web_scraper import scrape_web  # Import the scrape_web function
from urllib.parse import quote_plus

openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_search_query(prompt):
   response = openai.ChatCompletion.create(
       model="gpt-4-1106-preview",
       messages=[
           {"role": "system", "content": "You are a helpful assistant."},
           {"role": "user", "content": f"Create a Google search query for the following information need: {prompt}"}
       ]
   )
   search_query = response['choices'][0]['message']['content']
   print(f"Generated search query: {search_query}")
   return search_query

def generate_answer_with_data(prompt, scraped_data):
   combined_prompt = f"Based on the following information, answer the question: {prompt}\n\n{scraped_data}"
   response = openai.ChatCompletion.create(
       model="gpt-4-1106-preview",
       messages=[
           {"role": "system", "content": "You are a helpful assistant."},
           {"role": "user", "content": combined_prompt}
       ]
   )
   if response.choices:
       print("Generated answer successfully.")
       return response.choices[0].text.strip()
   else:
       print("No choices were generated.")
       return ""

original_prompt = "Find best video review of the website https://www.klaviyo.com/ Post just a link and nothing else (not additional text whatsoever - just the link). Video should be as short as possible and provide the birdseyeview of the app. Look into official youtube channel of this website if it exists. Do not ask any follow-up, clarifying questions, do best with what you have. If no information is available, give some video about Klariyo which more or less fits the description above"
search_query = generate_search_query(original_prompt)
encoded_query = quote_plus(search_query)
search_url = f"https://www.google.com/search?q={encoded_query}"
scraped_data = scrape_web(search_url)
answer = generate_answer_with_data(original_prompt, scraped_data)

print(answer)
