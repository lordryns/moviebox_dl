from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import click
import time, questionary

URL = "https://moviebox.ph/"
driver_options = None

@click.group(help="Download movies from Moviebox to your device")
def cli():
    pass 

def handle_headless(is_headless: bool): 
    if driver_options is None:
        click.echo(click.style("Driver not set!", fg="red"))
        return
    click.echo(f"headless: {is_headless}")
    if is_headless:
        driver_options.add_argument("--headless")




@cli.command(help="Find movie to download")
@click.option("-s", "--search", default="", help="Show to search for")
@click.option("--browser-id", default=0, help="Set browser by ID, 0 for chrome 1 for firefox")
@click.option("-t", "--timeout", default=3, help="Set length of wait intervals")
@click.option("-h", "--headless", is_flag=True, help="Use to hide the browser")
def find(search, browser_id, timeout, headless):
    global driver_options
    driver = None
    match browser_id:
        case 0:
            click.echo("Driver: Chrome")
            driver_options = ChromeOptions()
            handle_headless(headless)
            driver = webdriver.Chrome(options=driver_options)
        case 1:
            click.echo("Driver: Firefox")
            driver_options = FireFoxOptions()
            handle_headless(headless)
            driver = webdriver.Firefox(options=driver_options)

    if driver is None:
        click.echo(click.style("You must select a valid driver! use --help to see more information.", fg="red"), err=True, )
        return 

    try:
        print("Process started. Running...")
        driver.get(URL)
        time.sleep(timeout)
        search_input = driver.find_element(By.ID, "realInput")
        search_input.send_keys(search)
        search_input.send_keys(Keys.ENTER)
        time.sleep(timeout)
        click.echo("Result text: {}".format(driver.find_element(By.CLASS_NAME, "search-result-page-h1").text))
        
        movie_container = driver.find_element(By.CLASS_NAME, "main")
        items = movie_container.find_elements(By.CLASS_NAME, "item")
        count = 0
        for item in items:
            click.echo("{}. {}".format(click.style(count, fg="green"), item.find_element(By.CLASS_NAME, "card-title").text))
            count += 1
        
        click.echo("Done!")

        command = questionary.text("Enter movie index: ").ask()
        item = items[int(command)]
        click.echo(f"You chose {item.find_element(By.CLASS_NAME, 'card-title').text}")
        time.sleep(timeout)
        item.find_element(By.CLASS_NAME, "card-btn").click()
        time.sleep(timeout)
        
    except Exception as e:
        click.echo(e, err=True)
    time.sleep(timeout)
    print("Program finished!")


def main():
    cli()

if __name__ == "__main__":
    main()

