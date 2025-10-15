from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import click
import time, sys  

URL = "https://moviebox.ph/"
chrome_options = ChromeOptions()

def handle_headless(is_headless: bool): 
    click.echo(f"headless: {is_headless}")
    if is_headless:
        chrome_options.add_argument("--headless")

@click.command()
@click.option("-s", "--search", default="", help="Show to search for")
@click.option("--browser-id", default=0, help="Set browser by ID, 0 for chrome 1 for firefox")
@click.option("-t", "--timeout", default=3, help="Set length of wait intervals")
@click.option("-h", "--headless", is_flag=True, help="Use to hide the browser")
def visit_site(search, browser_id, timeout, headless):
    driver = None
    match browser_id:
        case 0:
            click.echo("Using Chrome...")
            handle_headless(headless)
            driver = webdriver.Chrome(options=chrome_options)
        case 1:
            click.echo("Using Firefox...")
            driver = webdriver.Firefox()

    if driver is None:
        click.echo(click.style("You must select a valid driver! use --help to see more information.", fg="red"), err=True, )
        return 

    try:
        print("Process started.")
        driver.get(URL)
        time.sleep(timeout)
        search_input = driver.find_element(By.ID, "realInput")
        search_input.send_keys(search)
        search_input.send_keys(Keys.ENTER)
        time.sleep(timeout)
        click.echo("Result text: {}".format(driver.find_element(By.CLASS_NAME, "search-result-page-h1").text))
        
        movie_container = driver.find_element(By.CLASS_NAME, "main")
        items = movie_container.find_elements(By.CLASS_NAME, "item")
        for item in items:
            click.echo(item.find_element(By.CLASS_NAME, "card-title").text)
        
        click.echo("Done!")
    except Exception as e:
        click.echo(e, err=True)
    time.sleep(timeout)
    print("Program finished!")


def main():
    visit_site()
if __name__ == "__main__":
    main()

