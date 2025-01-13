import requests
from bs4 import BeautifulSoup

def data_collector(category, URL=None):
    if not URL:
        URL = f"https://www.futurepedia.io/ai-tools/{category}"
    
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    divs = soup.find_all('div', class_='px-6 mt-auto flex items-center justify-between pb-4')

    tool_list = []

    for div in divs:
        a_tag = div.find('a', {'data-tool-name': True})
        if a_tag:
            tool_name = a_tag['data-tool-name']
            href = a_tag.get('href', '')
            tool_list.append({tool_name: href})
        
    return tool_list

def main():
    categories = ['marketing']
    tools = data_collector(categories)

    print(tools)

def lambda_handler(event, context):
    print("The main function is being called")

    main()


