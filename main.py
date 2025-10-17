from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
import click
import time, questionary
import requests 

URL = "https://moviebox.ph/web/movie"
driver_options = None


@click.group(help="Download movies from Moviebox to your device")
def cli():
    pass 


def handle_options(head: bool): 
    if driver_options is None:
        click.echo(click.style("Driver not set!", fg="red"))
        return

    #driver_options.add_argument("--disable-features=ExternalProtocolDialog")
    #driver_options.add_argument("--no-default-browser-check")
    #driver_options.add_argument("--disable-external-intent-requests")
    click.echo(f"headless: {not head}")
    if not head:
        driver_options.add_argument("--headless")
        #driver_options.add_argument("--window-size=1920,1080")


@cli.command(help="Find any potential issues preventing the script from executing successfully")
def audit():
    click.echo("Running check...")
    t0 = time.perf_counter()
    try:
        query = requests.get(URL, timeout=6)
        if query.status_code == 200:
            click.echo(f"Response: {click.style('SUCCESSFUL(200)', fg='green')}")
        else:
            click.echo(f"Response: {click.style(f'BAD({query.status_code})', fg='green')}")
   
    except:
        click.echo(click.style("Request failed terribly! this is most likely a network issue, are you connected to the internet?", fg='red'))
    t1 = time.perf_counter()

    tn = t1 - t0 
    click.echo(f"Request speed: {tn}")

    if tn > 6:
        click.echo(f"Network speed: {click.style('BAD', fg='red')}")
    elif tn > 3:
        click.echo(f"Network speed: {click.style('SLOW', fg='yellow')}")
    else:
        click.echo(f"Network speed: {click.style('OK', fg='green')}")

    
@cli.command(help="Find movie to download")
@click.option("-s", "--search", default="", help="Show to search for")
@click.option("--browser-id", default=0, help="Set browser by ID, 0 for chrome 1 for firefox")
@click.option("-t", "--timeout", default=3, help="Set length of wait intervals")
@click.option("-h", "--head", is_flag=True, help="Use to Show the browser")
def find(search, browser_id, timeout, head):
    global driver_options
    driver = None
    match browser_id:
        case 0:
            click.echo("Driver: Chrome")
            driver_options = ChromeOptions()
            handle_options(head)
            driver = webdriver.Chrome(options=driver_options)
        case 1:
            click.echo("Driver: Firefox")
            driver_options = FireFoxOptions()
            handle_options(head)
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
        

        command = questionary.text("Enter movie index: ").ask()
        item = items[int(command)]
        click.echo(f"You chose {item.find_element(By.CLASS_NAME, 'card-title').text}")
        time.sleep(timeout)
        item.find_element(By.CLASS_NAME, "card-btn").click()
        time.sleep(timeout)
        driver.find_element(By.CLASS_NAME, "watch-btn").click() 
        time.sleep(timeout)
        driver.find_element(By.CLASS_NAME, "download-btn-hover").click()
        click.echo("Looking for available quality...")
        time.sleep(timeout)
        
        modal_div_download_modal = WebDriverWait(driver, timeout).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "download-option")))
        quality_list = modal_div_download_modal.find_element(By.CLASS_NAME, "quality-list")

        quality_items = quality_list.find_elements(By.CLASS_NAME, "itm")
        count = 0
        for item in quality_items:
            click.echo(f"{click.style(count, fg="green")}. {item.text}")
            count += 1

    except Exception as e:
        click.echo(e, err=True)
    time.sleep(timeout)
    print("Program finished!")


def main():
    cli()

if __name__ == "__main__":
    main()

