"""
Website to Brochure Generator
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from scraper import fetch_website_links, fetch_website_contents
from prompts import link_system_prompt, brochure_system_prompt

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    print("Using OpenAI")
    MODEL = os.getenv("OPENAI_MODEL", "gpt-5-nano")
    openai = OpenAI(api_key=OPENAI_API_KEY)
    print(f"Using OpenAI with model: {MODEL}")
else:
    print("Using Ollama")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    openai = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')
    print(f"Using Ollama at {OLLAMA_BASE_URL} with model: {MODEL}")

def get_links_user_prompt(url):
    user_prompt = f"""
Here is the list of links on the website {url} -
Please decide which of these are relevant web links for a brochure about the company, 
respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

"""
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt

def select_relevant_links(url):
    # print(f"Selecting relevant links for {url} by calling {MODEL}")
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(url)}
        ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    links = json.loads(result)
    # print(f"Found {len(links['links'])} relevant links")
    return links

def fetch_page_and_all_relevant_links(url):
    contents = fetch_website_contents(url)
    relevant_links = select_relevant_links(url)
    result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"
    for link in relevant_links['links']:
        result += f"\n\n### Link: {link['type']}\n"
        result += fetch_website_contents(link["url"])
    return result

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"""
You are looking at a company called: {company_name}
Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.\n\n
"""
    user_prompt += fetch_page_and_all_relevant_links(url)
    user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
    return user_prompt

def create_brochure(company_name, url):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ],
    )
    result = response.choices[0].message.content
    print(result)

def stream_brochure(company_name, url):
    stream = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
          ],
        stream=True
    )
    for chunk in stream:
        print(chunk.choices[0].delta.content or '', end='', flush=True)
    print()

def main():
    """Main entry point for testing."""
    url = input("Enter a URL to use as content generate the brochure: ")
    print("\nFetching and generating...\n")
    # create_brochure("Example Company", url)
    stream_brochure("Example Company", url)

if __name__ == "__main__":
    main()