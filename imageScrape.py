from selenium import webdriver
import time
import urllib
from webdriver_manager.chrome import ChromeDriverManager
from optparse import OptionParser
import sys
import boto3
from flask_api import FlaskAPI

app = FlaskAPI(__name__)


@app.route('/thumbnail/<string:cocktailName>', strict_slashes=False, methods=['GET'])
def getCocktail(textInput):
    browser = None
    try:
        cocktail = textInput + ' cocktail'
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_argument('headless')
        manager = ChromeDriverManager()
        
        #browser = webdriver.Chrome(ChromeDriverManager.install())
        browser = webdriver.Chrome(executable_path=manager.install(),chrome_options=chrome_options)
        #browser = webdriver.Chrome(chrome_options=chrome_options)

        browser.get('https://www.google.com/advanced_image_search')


        searchElem = browser.find_element_by_id('mSoczb') #search by word
        searchElem.clear()
        searchElem.send_keys(cocktail) # Search entry

        #Image Size element
        sizeElem = browser.find_element_by_id('imgsz_button')
        sizeElem.click()
        time.sleep(0.2)
        medSizeElem = browser.find_element_by_id(':78')
        medSizeElem.click()

        time.sleep(0.2)
        #Setting Aspect Ratio
        aspectElem = browser.find_element_by_id('imgar_button')
        aspectElem.click()
        time.sleep(0.2)
        squareElem = browser.find_element_by_id(':7r')
        squareElem.click()
        time.sleep(0.2)

        #Search button
        advanceSearchButton = browser.find_element_by_xpath("//input[@class='jfk-button jfk-button-action dUBGpe']")
        advanceSearchButton.click()
        time.sleep(2)
        #first picture element
        firstPic = browser.find_element_by_xpath("//div[@id='rg_s']//div[1]//a[1]//img[1]").get_attribute('src')

        urllib.request.urlretrieve(firstPic, textInput + '.jpg')

        print('Uploading: ' + textInput + '.jpg')
        s3_client = boto3.client('s3')
        response = s3_client.upload_file(textInput + '.jpg', 'barbot-data', textInput + '.jpg')

        browser.close()
        return True
    except Exception as e:
        print(e)
        browser.close()
        return False


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
