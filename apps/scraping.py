#!/usr/bin/env python
# coding: utf-8


#Import dependencies.
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    # Set your executable, path and initialize the chrome browser in splinter.
    browser = Browser("chrome", executable_path="chromedriver", headless=True)


    def mars_news(browser):
        # visit the mars nasa news website.
        url='https://mars.nasa.gov/news/'
        browser.visit(url)  

        # Optional delay for loading the page
        browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

        # convert the browser html to a soup object and then quit the browser.
        html = browser.html
        news_soup = BeautifulSoup(html, 'html.parser')

        # Add try/except for error handling
        try:
            slide_elem = news_soup.select_one('ul.item_list li.slide')

            slide_elem.find("div", class_='content_title')

            # Use the parent element to find the first `a` tag and save it as `news_title`
            news_title = slide_elem.find("div", class_='content_title').get_text()
            
            # Use the parent element to find the paragraph text
            news_paragraph = slide_elem.find('div', class_="article_teaser_body").get_text()
            return news_title, news_paragraph

        except AttributeError:
            return None, None

        
    # Featured Images

    def featured_image(browser):

        # Visit URL
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        # Find and click the full image button
        full_image_elem = browser.find_by_id('full_image')
        full_image_elem.click()

        # Find the more info button and click that
        browser.is_element_present_by_text('more info', wait_time=1)
        more_info_elem = browser.find_link_by_partial_text('more info')
        more_info_elem.click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')

        try:
            # Find the relative image url
            img_url_rel = img_soup.select_one('figure.lede a img').get("src")
            # Use the base URL to create an absolute URL
            img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
            return img_url

        except AttributeError:
            return None

                     

    def mars_facts():
        try:
            #using pandas to copy thr first table on mars facts website and converting it into  df.
            df = pd.read_html('http://space-facts.com/mars/')[0]
        except BaseException:
            return None
        #Assign columns and set index to description column.
        df.columns=['description', 'value']
        df.set_index('description', inplace=True)
        
        #convert the df back to html to upload it on our website.
        return df.to_html()

     # Hemisphere Titles and Images
    
    def hemisphere_data(browser):
        hemi_data=[]
        hemispheres=['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']
        #  hemisphere_data=[hemisphere_data(hemisphere) for hemisphere in hemisphere]
        # Visit URL
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        
        
        # Find the hempisphere link and click that
        for hemisphere in hemispheres:
            browser.visit(url)
            browser.is_element_present_by_text(hemisphere, wait_time=1)
            hem_info_elem = browser.find_link_by_partial_text(hemisphere)
            hem_info_elem.click()

            # Parse the resulting html with soup
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')

            try:
                # Find the hemisphere title.
                hemisphere_title = soup.find('h2', class_='title').get_text()
                # Find the hemisphere image.
                hemisphere_image = soup.find('a', text='Sample').get("href")
                hemi_dict={'title':hemisphere_title, 'img_url':hemisphere_image}
                hemi_data.append(hemi_dict)
            except AttributeError:
                print('Hemisphere not found...skipping')
        return hemi_data        

    # Set news title and paragraph variables.
    news_title, news_paragraph = mars_news(browser)
    hemi_data= hemisphere_data(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemi_data": hemi_data,
        "last_modified": dt.datetime.now()
    }
    #end the session.
    browser.quit()

    return data

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())