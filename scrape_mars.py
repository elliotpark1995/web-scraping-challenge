from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "C:/chromedriver/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

## Mars News

    browser = init_browser()

    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    html = browser.html

    news_soup = bs(html, "html.parser")

    news_title = news_soup.find("div", class_="content_title").find('a').text
    news_paragraph = news_soup.find("div", class_="article_teaser_body").get_text()

    browser.quit()

    print(f'Title: {news_title}\nText: {news_paragraph}')

 ## JPL Mars Space Images - Featured Image 

    browser = init_browser()

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    browser.click_link_by_partial_text("FULL IMAGE")

    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    html = browser.html

    image_soup = bs(html, "html.parser")

    image_url = image_soup.find("figure", class_="lede").a["href"]

    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'

    browser.quit()

    print(featured_image_url)

## Mars Weather 

    browser = init_browser()

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    html = browser.html

    weather_soup = bs(html, "html.parser")

    tweets = weather_soup.find_all('ol', class_='stream-items')
    for tweet in tweets:
        mars_weather = tweet.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        if 'InSight' in tweet:
            break
        else:
            continue

    browser.quit()

    mars_weather = mars_weather.split('pic')[0]

    mars_weather = mars_weather.replace('\n', ' ')

    print(mars_weather)

## Mars Facts 

    facts_url = "https://space-facts.com/mars/"

    facts_tables = pd.read_html(facts_url)

    df_mars_facts = facts_tables[1]

    df_mars_facts.columns = ['Description', 'Value']

    df_mars_facts.set_index('Description', inplace=True)

    mars_facts = df_mars_facts.to_html(header=True, index=True)

## Mars Hemispheres 

    browser = init_browser()

    astrogeo_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astrogeo_url)

    html = browser.html

    astrogeo_soup = bs(html, "html.parser")

    main_astrogeo_url = "https://astrogeology.usgs.gov"

    hems_url = astrogeo_soup.find_all("div", class_="item")

    hemis_url = []

    for hem in hems_url:
        hem_url = hem.find('a')['href']
        hemis_url.append(hem_url)

    browser.quit()

    hemisphere_image_urls = []
    for hemi in hemis_url:
        hem_astrogeo_url = main_astrogeo_url + hemi
        print(hem_astrogeo_url)
        
        browser = init_browser()
        browser.visit(hem_astrogeo_url)
        
        html = browser.html

        hemi_soup = bs(html, "html.parser")

        raw_title = hemi_soup.find("h2", class_="title").text
        
        title = raw_title.split(' Enhanced')[0]
        
        img_url = hemi_soup.find("li").a['href']
        
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        
        browser.quit()

    print(hemisphere_image_urls)

## Mars Data Dictionary - MongoDB 

    mars_data = {}

    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph

    mars_data['featured_image_url'] = featured_image_url

    mars_data['mars_weather'] = mars_weather

    mars_data['mars_facts'] = mars_facts

    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    print("Scrape Complete")

    return mars_data