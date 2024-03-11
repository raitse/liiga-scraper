#!/home/raitse/dev/python/liiga-scraper/venv/bin/python3

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    get_html_from_source()


def get_html_from_source():
    url = "https://liiga.fi/fi/ohjelma"
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    parse_html(page_source)


def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    print(soup)
    root_div = soup.find("div", id="root")
    if root_div:
        match_results = soup.find_all("div", class_="_shedCardContainerThree_69wmc_376")
        for result in match_results:
            game_score = "N/A"
            home_team_elements = result.find_all(
                "div", class_="_gameCardTeamNameLeftAlign_69wmc_537"
            )
            for team_element in home_team_elements:
                team_name_element = team_element.find(
                    "div", class_="_teamName_69wmc_555"
                )
                home_team = team_name_element.text.strip()

            away_team_elements = result.find_all(
                "div", class_="_gameCardTeamNameRightAlign_69wmc_538"
            )
            for team_element in away_team_elements:
                team_name_element = team_element.find(
                    "div", class_="_teamName_69wmc_555"
                )
                away_team = team_name_element.text.strip()

            game_score_element = result.find("div", class_="_gameCardScore_69wmc_530")
            if game_score_element:
                game_score = game_score_element.text.strip()

            printer(home_team, away_team, game_score)


def printer(home_team, away_team, score):
    print(f"{home_team} vs. {away_team} : {score}")


if __name__ == "__main__":
    main()
