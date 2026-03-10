import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def scrape_movies(driver):

    url = "https://www.imdb.com/chart/top/"
    driver.get(url)

    time.sleep(5)

    movies = driver.find_elements(By.XPATH, '//li[contains(@class,"ipc-metadata-list-summary-item")]')

    movie_data = []

    for index, movie in enumerate(movies, start=1):

        try:
            title = movie.find_element(By.XPATH, './/h3').text

            metadata = movie.find_elements(By.XPATH, './/span[contains(@class,"cli-title-metadata-item")]')

            year = metadata[0].text if len(metadata) > 0 else "N/A"

            rating = movie.find_element(By.XPATH, './/span[contains(@class,"ipc-rating-star")]').text

            movie_data.append({
                "Rank": index,
                "Title": title,
                "Year": year,
                "IMDb Rating": rating
            })

        except Exception as e:
            print("Error extracting movie:", e)

    return movie_data


def main():

    chrome_options = Options()

    # Headless mode (no browser window)
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    print("Starting IMDb Top 250 Scraper...")

    data = scrape_movies(driver)

    driver.quit()

    df = pd.DataFrame(data)

    df.to_csv("imdb_top_250_movies.csv", index=False)

    df.to_excel("imdb_top_250_movies.xlsx", index=False)

    print("Scraping completed successfully!")
    print("Files saved:")
    print("imdb_top_250_movies.csv")
    print("imdb_top_250_movies.xlsx")


if __name__ == "__main__":
    main()
