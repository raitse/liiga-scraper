#!/home/raitse/dev/python/liiga-scraper/venv/bin/python3

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from terminaltables import SingleTable


def main():
    get_html_from_source()


def get_html_from_source():
    url = "https://liiga.fi/fi/ohjelma"
    options = Options()
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    parse_html(page_source)


def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    match_results_list = []
    root_div = soup.find("div", id="root")
    if root_div:
        match_results = soup.find_all("div", class_="_shedCardContainerThree_69wmc_376")
        for result in match_results:
            game_score = "N/A"
            game_crowd = "N/A"
            game_date_element = result.find(
                "div", class_="_gameDateContainer_69wmc_392"
            )
            if game_date_element:
                game_date = game_date_element.text.strip()

            game_time_element = result.find(
                "div", class_="_gameTimeContainer_69wmc_415"
            )
            if game_time_element:
                game_time = game_time_element.text.strip()

            game_date_time = f"{game_date}, {game_time}"

            home_team_element = result.find(
                "div", class_="_gameCardTeamNameLeftAlign_69wmc_537"
            )
            if home_team_element:
                home_team = home_team_element.text.strip()

            away_team_element = result.find(
                "div", class_="_gameCardTeamNameRightAlign_69wmc_538"
            )
            if away_team_element:
                away_team = away_team_element.text.strip()

            game_score_element = result.find("div", class_="_gameCardScore_69wmc_530")
            if game_score_element:
                game_score = game_score_element.text.strip()

            game_crowd_element = result.find(
                "div", class_="_regularSpecatorCount_69wmc_608"
            )
            if game_crowd_element:
                game_crowd = game_crowd_element.text.strip()

            match_results_list.append(
                {
                    "home": home_team.strip(),
                    "away": away_team.strip(),
                    "score": game_score.strip(),
                    "date": game_date_time.strip(),
                    "crowd": game_crowd.strip(),
                }
            )
        printer(match_results_list)


def printer(match_results):
    table_data = [["Koti", "Vieras", "Tulos", "Pvm", "Yleisö"]]
    for result in match_results:
        table_data.append(
            [
                result["home"],
                result["away"],
                result["score"],
                result["date"],
                result["crowd"],
            ]
        )

    table_instance = SingleTable(table_data)
    table_instance.justify_columns[2] = "center"
    table_instance.title = "Liiga.fi tulokset 23-24"
    table_instance.inner_heading_row_border = True
    table_instance.inner_row_border = True
    table_instance.outer_border = True

    print(table_instance.table)


if __name__ == "__main__":
    main()
