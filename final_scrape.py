import requests
from bs4 import BeautifulSoup
import json

def tool_category_identify(URL):
    parts = URL.split('/')
    tool_category = parts[-1]
    return tool_category

def data_collector(category, page, URL=None):
    if not URL:
        URL = f"https://www.futurepedia.io/ai-tools/{category}?page={page}"
    
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')

    tool_containers = soup.find_all('div', class_='flex flex-col items-start')
    tool_list = []

    for container in tool_containers:
        tool_name_tag = container.find('p', class_='m-0 line-clamp-2 overflow-hidden text-xl font-semibold text-slate-700')
        tool_name = tool_name_tag.text.strip() if tool_name_tag else None

        link_tag = container.find('a', href=True)
        link = f"https://www.futurepedia.io{link_tag['href']}" if link_tag else None

        description_tag = container.find_next('p', class_='text-muted-foreground my-2 line-clamp-2 overflow-hidden overflow-ellipsis px-6 text-base')
        description = description_tag.text.strip() if description_tag else None

        # Extract the pricing model
        pricing_model = None
        pricing_container = container.find_next('div', class_='px-6')
        if pricing_container:
            pricing_div = pricing_container.find('div', class_='flex justify-between text-lg')
            if pricing_div:
                pricing_span = pricing_div.find('span')
                if pricing_span:
                    pricing_model = pricing_span.text.strip()

        # Debug output for the extracted values
        print(f"Tool: {tool_name}, Link: {link}, Description: {description}, Pricing: {pricing_model}")

        if tool_name and link and description and pricing_model:
            tool_list.append({
                "name": tool_name,
                "link": link,
                "description": description,
                "pricing_model": pricing_model,
                "category": category
            })

    return tool_list

def main():
    categories = ['marketing']
    tool_lists = []
    for category in categories:
        for page in range(1, 3):  # Loop through the first 2 pages
            tools = data_collector(category=category, page=page)
            tool_lists.extend(tools)  # Flatten the list of lists

    # Convert the tool list to JSON format and print it
    json_output = json.dumps(tool_lists, indent=4)
    print(json_output)

if __name__ == "__main__":
    main()
