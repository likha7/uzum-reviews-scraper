from playwright.sync_api import sync_playwright
import json

URL = 'https://uzum.uz/uz/product/iphone-17-propro-1983388/reviews'

def scrape_page(page):
    reviews = []
    users = page.locator('div.wrap').all()

    if len(users) == 0:
        return None

    for user in users:
        try:
            name = user.locator('div.wrapper > span.BodyMRegular.name').inner_text()
            date = user.locator('div.wrapper > span.BodyMRegular-Long.date').inner_text()
            rating = len(user.locator('div.star-rating.rating > svg.star.filled-start').all())

            pros_el = user.locator('[data-test-id="pros_review"] span.BodyMRegular')
            pros = pros_el.inner_text() if pros_el.count() > 0 else ""

            cons_el = user.locator('[data-test-id="cons_review"] span.BodyMRegular')
            cons = cons_el.inner_text() if cons_el.count() > 0 else ""

            comment_el = user.locator('span[itemprop="reviewBody"]:not([data-test-id])')
            comment = comment_el.inner_text() if comment_el.count() > 0 else ""

            reviews.append({
                'name': name,
                'date': date,
                'rating': rating,
                'pros': pros,
                'cons': cons,
                'comment': comment
            })

        except Exception as e:
            print(f"Skipped: {e}")
            continue

    return reviews


def scrape_all_reviews():
    all_reviews = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()
        page.set_extra_http_headers({
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "Accept-Language": "uz-UZ,uz;q=0.9,en;q=0.8",
        })

        page.goto(URL)
        page.wait_for_load_state('domcontentloaded')
        page.wait_for_timeout(2000)

        while True:
            load_more = page.locator('button.u-button.more')
            if load_more.count() == 0:
                break


            load_more.click()
            page.wait_for_timeout(2000)

        print(f"Total reviews: {page.locator('div.wrap').count()}")
        print("Scraping....")
        reviews = scrape_page(page)
        print("Scraping Finished!!!")
        all_reviews.extend(reviews)
        browser.close()
    
    with open('reviews.json', 'w', encoding='utf-8') as file:
        json.dump(all_reviews, file, indent = 2, ensure_ascii=False)
    
if __name__ == '__main__':
    scrape_all_reviews()