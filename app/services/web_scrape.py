from playwright.async_api import async_playwright
from lxml import etree
import re
import json

def short_url(link):
    match = re.search(r"(.+?\/dp\/.+?\/)", link)
    if match:
        return (match.group(1))
    else:
        return link

def format_number(s):
    s = s.strip().upper().replace('+', '')
    match = re.match(r"([\d.]+)\s*([KMBT]?)", s)
    if not match:
        raise ValueError(f"Invalid format: {s}")
    number, suffix = match.groups()
    number = float(number)
    multiplier = {'': 1,'K': 1_000, 'M': 1_000_000,}.get(suffix, 1)
    return number * multiplier

async def fetch_title(url: str):
    async with async_playwright() as p:
        browsers = [
            lambda: p.firefox.launch(headless=True),
            lambda: p.chromium.launch(headless=True),
            lambda: p.webkit.launch(headless=True)
        ]

        browser_index = 0
        retries = 0
        max_retries = 3
        while True:
            browser = await browsers[browser_index % len(browsers)]()
            page = await browser.new_page()
            try:
                await page.goto(url)
                html = await page.content()
                error1 = "Sorry, we just need to make sure you're not a robot"
                error2 = "Sorry! Something went wrong!"
                if error1 in html or error2 in html:
                    retries += 1
                    if retries >= max_retries:
                        await browser.close()
                        browser_index += 1
                        retries = 0
                    continue
                else:
                    await browser.close()
                    return html
            except Exception as e:
                print(f"Exception in browser fetch: {e}")
                await browser.close()
                retries += 1
                if retries >= max_retries:
                    browser_index += 1
                    retries = 0

async def run(url):
    result = await fetch_title(url)
    return result

def list_to_str(list_element):
    try:
        if list_element:
            return list_element[0]
        return ""
    except Exception:
        return ""

async def scrape(json_query):
    result = []
    name = json_query["query"]
    sponsored = json_query["sponsored"]
    limit = json_query["limit"]
    stars = json_query["stars"]

    name_format = '+'.join(name.split())
    url = f"https://www.amazon.com/s?k={name_format}"
    html = await run(url)
    et = etree.HTML(html)
    elements = et.xpath('//div[@role="listitem" and @data-asin]')

    if not elements:
        return []

    for element in elements:
        try:
            html_str = etree.tostring(element, encoding='unicode', pretty_print=True)
            reviews_str = list_to_str(element.xpath(".//span[contains(@class, 's-underline-text')]/text()"))
            reviews = int(reviews_str.replace(",", "")) if reviews_str else ""
            brand = list_to_str(element.xpath(".//h2[contains(@class,'a-size-mini')]//span/text()"))
            skuname = list_to_str(element.xpath(".//h2[contains(@class,'a-size-base-plus') or contains(@class,'a-size-medium')]//span/text()"))
            skurl = short_url(list_to_str(element.xpath(".//a[contains(@class, 'a-link-normal')]/@href")))
            rating = list_to_str(element.xpath(".//span[contains(@class, 'a-icon-alt')]/text()"))
            past_month = list_to_str(element.xpath(".//div[contains(@class, 'a-size-base')]//span[contains(@class, 'a-color-secondary')]/text()"))

            if past_month:
                match = re.search(r'\d+(?:[Kk]\+?|[Mm]\+?)?', past_month)
                past_month = match.group(0) if match else ""

            if rating:
                match = re.search(r"(\d+\.\d+)", rating)
                rating = float(match.group(1)) if match else None
            else:
                rating = None

            price = list_to_str(element.xpath(".//span[contains(@class, 'a-price')]//span[contains(@class, 'a-offscreen')]/text()"))

            item = {
                "Brand": brand,
                "SkuName": f"{brand} {skuname}".strip(),
                "SkuUrl": "https://www.amazon.com" + skurl,
                "ImageUrl": list_to_str(element.xpath(".//img[contains(@class, 's-image')]/@src")),
                "SalePrice": price if price else None ,
                "Reviews": reviews,
                "Rating": rating,
                "PastMonthsales": format_number(past_month) if past_month else "",
                "sponsored": bool("sspa" in skurl),
            }

            result.append(item)

        except Exception as e:
            print(f"Error in element: {e}")
            continue

    with open("result.json", "w") as f:
        json.dump(result, f, indent=4)

    return result



