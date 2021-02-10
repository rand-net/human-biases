import requests
import csv
from bs4 import BeautifulSoup


def rm_brackets(string):
    new_string = ""
    for sub_string in string.split("["):
        if "]" in sub_string:
            l = sub_string.split("]")
            for s in l[1:]:
                new_string += s
        else:
            new_string += sub_string
    return new_string


def build_tables():
    tables = {}
    page_url = "https://en.wikipedia.org/wiki/List_of_cognitive_biases"
    page_source = requests.get(page_url).text
    soup = BeautifulSoup(page_source, "lxml")
    for t in soup.select(".wikitable"):
        heading = t.find_previous("h2").text[:-6]
        # Scrape columns based on header
        if heading == "Memory":
            rows = []
            for row in t.find_all("tr"):
                parts = row.find_all("td")
                if parts:
                    name = rm_brackets(parts[0].text)
                    desc = rm_brackets(parts[1].text)
                    category = "Uncategorized"
                    rows.append((name, category, desc))
            tables[heading] = rows
        else:
            rows = []
            for row in t.find_all("tr"):
                parts = row.find_all("td")
                if parts:
                    name = rm_brackets(parts[0].text)
                    category = rm_brackets(parts[1].text)
                    desc = rm_brackets(parts[2].text)
                    rows.append((name, category, desc))
            tables[heading] = rows
    return tables


def main():
    csv_file = open("data/biases.csv", "w")
    csv_writer = csv.writer(csv_file)
    tables = build_tables()
    for table in tables.keys():
        for name, category, desc in tables[table]:
            name.replace("\n", "")
            category.replace("\n", "")
            desc.replace("\n", "")
            # Assigns Uncategorized if no category is present
            if not category.strip():
                category = "Uncategorized"
            csv_writer.writerow([table, name, category, desc])
    csv_file.close()


if __name__ == "__main__":
    main()
