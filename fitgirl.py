import requests
import sys
from bs4 import BeautifulSoup
from requests.exceptions import Timeout, RequestException

# Set UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

base_url = "https://fitgirl-repacks.site/all-my-repacks-a-z/"

page_num = 1

while True:
    url = base_url + f"?lcp_page0={page_num}#lcp_instance_0"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        ul_element = soup.find("ul", class_="lcp_catlist", id="lcp_instance_0")

        # Stop if list does not exist
        if not ul_element:
            print(f"No list found on page {page_num}. Stopping.")
            break

        li_elements = ul_element.find_all("li")

        # Stop if page is empty
        if not li_elements:
            print(f"No items found on page {page_num}. Stopping.")
            break

        for li in li_elements:
            a = li.find("a")
            if not a:
                continue

            link = a.get("href")
            title = a.get_text(strip=True)

            print("Link:", link)
            print("Title:", title)

            try:
                linked_page_response = requests.get(link, timeout=10)
                linked_page_response.raise_for_status()

                linked_soup = BeautifulSoup(
                    linked_page_response.text, "html.parser"
                )

                magnet_link = linked_soup.find(
                    "a",
                    href=lambda h: h and h.startswith("magnet:")
                )

                if magnet_link:
                    print("Magnet:", magnet_link["href"])

                print("-" * 20)

            except Timeout:
                print(f"Timeout loading linked page: {link}")
            except RequestException as e:
                print(f"Request error on linked page: {e}")

        print(f"Finished processing page {page_num}")
        page_num += 1

    except Timeout:
        print(f"Timeout on page {page_num}. Skipping.")
        page_num += 1
    except RequestException as e:
        print(f"Request error on page {page_num}: {e}")
        page_num += 1

