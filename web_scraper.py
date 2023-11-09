import asyncio
from pyppeteer import launch

async def scrape_web(url):
 print(f"Sending GET request to: {url}")
 browser = await launch()
 page = await browser.newPage()
 await page.goto(url)
 # Wait for the page to load
 await asyncio.sleep(2)
 # Get the first link from the search results
 first_link = await page.evaluate('''
     () => {
         let links = Array.from(document.querySelectorAll('a[href^="/url"]'));
         return links[0] ? links[0].href : null;
     }
 ''')
 if first_link:
     # Navigate to the first link
     await page.goto(first_link)
     # Wait for the navigation to complete
     await page.waitForNavigation()
     # Get the content of the page
     content = await page.content()
     await browser.close()
     # Save the content to a .html file
     with open('output.html', 'w') as f:
         f.write(content)
     print("Scraped data successfully.")
 else:
     print("No links were found.")
     await browser.close()
     return ""

# Run the function
asyncio.get_event_loop().run_until_complete(scrape_web('https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fresults%3Fsearch_query%3Dklaviyo%2Breview%2Bofficial%2Bchannel'))
