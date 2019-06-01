from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pymongo
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    # NASA Mars News
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "lxml")
    news_title=soup.find('div', class_='content_title').a.text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    #JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(5)
    
    html = browser.html
    soup = bs(html, "lxml")
    img_src=soup.find("ul",class_="articles").li.find("div",class_="img").img['src']
    featured_image_url=f"https://www.jpl.nasa.gov{img_src}"
    
    #Mars Weather
    url="https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    mars_weather =soup.find("div",class_="js-tweet-text-container").p.text.rsplit(' ', 1)[0]
    
    #Mars Facts
    url="https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df_mars = tables[0]
    df_mars.columns = ['Description', 'Value']
    df_mars.set_index('Description',inplace=True)
    #df_mars.to_html('mars.html')
    facts=df_mars.to_html()
    
    #Mars Hemispheres
    hemisphere_image_urls =[]
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "lxml")
    img_divs=soup.find("div",class_="collapsible results").find_all('div',class_="item")
    for item in img_divs:
        title=item.h3.text
        browser.click_link_by_partial_text(title)
        time.sleep(3)
        html = browser.html
        soup = bs(html, 'lxml')
        image_url_full=soup.find("div",class_="downloads").a['href']
        #print(title)
        #print(image_url_full)
        hemisphere_image_urls.append({'title':title, 'img_url':image_url_full })
        browser.click_link_by_partial_text("Back")
        time.sleep(1)
    browser.quit()
    
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather":mars_weather,
        "facts":facts,
        "hemisphere":hemisphere_image_urls
    }

    # Return results
    return mars_data
