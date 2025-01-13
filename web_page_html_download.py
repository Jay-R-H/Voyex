import requests
from bs4 import BeautifulSoup

URL = "https://www.futurepedia.io/ai-tools/design-generators"

def tool_category_identify(URL):
    parts = URL.split('/')
    tool_category = parts[-1]

    return tool_category

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
    categories = ['design-generators', 'video-generators']

    for category in categories:
        tools_list = data_collector(category=category)
        with open(f'{category}.json', 'w') as f:
            f.write(str(tools_list))

if __name__ == "__main__":
    main()