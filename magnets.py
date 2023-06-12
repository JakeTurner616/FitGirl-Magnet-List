import requests
import sys
from bs4 import BeautifulSoup

# Set the encoding to UTF-8 for printing
sys.stdout.reconfigure(encoding="utf-8")

# Base URL
base_url = "https://fitgirl-repacks.site/all-my-repacks-a-z/"

# Iterate over pages 1 to 71
for page_num in range(1, 72):
    # Update the URL with the current page number
    url = base_url + f"?lcp_page0={page_num}#lcp_instance_0"

    # Send a GET request to the website and retrieve the HTML content
    response = requests.get(url)
    html_content = response.text

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the <ul> element with class "lcp_catlist" and id "lcp_instance_0"
    ul_element = soup.find("ul", class_="lcp_catlist", id="lcp_instance_0")

    # Check if the ul_element is None
    if ul_element is not None:
        # Iterate over each <li> element within the <ul> element
        for li_element in ul_element.find_all("li"):
            # Find the <a> element within the <li> element
            a_element = li_element.find("a")
            if a_element:
                # Extract the href attribute value (link)
                link = a_element["href"]
                print("Link:", link)

                # Extract the text (title) within the <a> element
                title = a_element.text

                # Handle encoding errors by replacing problematic characters
                try:
                    print("Title:", title)
                except UnicodeEncodeError:
                    print("Title:", title.encode("utf-8", errors="replace").decode())

                # Send a GET request to the linked page and retrieve the HTML content
                linked_page_response = requests.get(link)
                linked_page_html_content = linked_page_response.text

                # Create another BeautifulSoup object to parse the linked page's HTML
                linked_page_soup = BeautifulSoup(linked_page_html_content, "html.parser")

                # Find the <a> element with href starting with "magnet:"
                magnet_link = linked_page_soup.find("a", href=lambda href: href and href.startswith("magnet:"))
                if magnet_link:
                    # Extract the href attribute value (magnet link)
                    magnet = magnet_link["href"]

                    # Handle encoding errors by replacing problematic characters
                    try:
                        print("Magnet:", magnet)
                    except UnicodeEncodeError:
                        print("Magnet:", magnet.encode("utf-8", errors="replace").decode())

                print("--------------------")
    else:
        print(f"Could not find the <ul> element with class 'lcp_catlist' and id 'lcp_instance_0' on page {page_num}")
