from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen

# launch chromedriver
driver = webdriver.Chrome('../driver/chromedriver')
driver.get('https://www.rottentomatoes.com/top/')   # rotten tomatoes url

# entering best movies by year
xpath = """//*[@id="main_container"]/div[3]/div[1]/section/div/div/a/p"""
driver.find_element_by_xpath(xpath).click()

# get year list
data = []
year_raw = driver.find_element_by_xpath("""//*[@id="top_movies_main"]/div/div[2]/ul""")
year = year_raw.find_elements_by_tag_name("a")
year_list = [link.get_attribute("href") for link in year]

# Crawling movie data
for i in year_list[:]:

    driver.get(i)
    html = urlopen(driver.current_url)
    soup = BeautifulSoup(html, 'html.parser')
    movie_count = len(soup.find('table', 'table').find_all('tr')) - 1

    for j in range(movie_count):
        try:
            xpath = """//*[@id="top_movies_main"]/div/table/tbody/tr[""" + str(j + 1) + """]/td[3]/a"""
            driver.find_element_by_xpath(xpath).click()

            html = urlopen(driver.current_url)
            soup = BeautifulSoup(html, 'html.parser')

            tmp = []
            for value in soup.find_all('div', 'meta-value'):
                tmp.append(value.get_text().strip())
            score = soup.find_all('span', "mop-ratings-wrap__percentage")

            # get attributes
            title = soup.find('h1', "mop-ratings-wrap__title mop-ratings-wrap__title--top").get_text()
            genre = ','.join([i.strip() for i in tmp[1].split(',')])
            director = ','.join([i.strip() for i in tmp[2].split(',')])
            released_year = i[-4:]
            studio = tmp[-1]
            rotten_score = score[0].get_text().strip()[:-1]
            audience_score = score[1].get_text().strip()[:-1]

            data.append([title, genre, director, released_year, studio, rotten_score, audience_score])
            print(title, '\t', released_year)

        except:
            pass

        driver.get(i)