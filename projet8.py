import requests
from bs4 import BeautifulSoup


def get_wikipedia_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Erreur lors de la récupération de la page")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    def extract_title(soup):
        title = soup.find("h1").text
        return title

    def extract_paragraphs(soup):
        paragraphs = {}
        for header in soup.find_all(["h2", "h3"]):
            title = header.text.strip()
            next_node = header.find_next_sibling()
            content = []
            while next_node and next_node.name not in ["h2", "h3"]:
                if next_node.name == "p":
                    content.append(next_node.text)
                next_node = next_node.find_next_sibling()
            paragraphs[title] = "\n".join(content)
        return paragraphs

    def extract_links(soup):
        links = set()
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("/wiki/") and ":" not in href:
                links.add("https://fr.wikipedia.org" + href)
        return links

    title = extract_title(soup)
    paragraphs = extract_paragraphs(soup)
    links = extract_links(soup)

    result = {"title": title, "paragraphs": paragraphs, "links": links}

    return result


url = "https://fr.wikipedia.org/wiki/Python_(langage)"
result = get_wikipedia_content(url)

print("Titre :", result["title"])
print("\nParagraphes :")
for title, content in result["paragraphs"].items():
    print(f"{title}:\n{content}\n")

print("Liens :")
for link in result["links"]:
    print(link)
