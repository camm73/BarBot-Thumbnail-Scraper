import time
from imageScrape import getCocktail

'''
cocktailList = None

with open('cocktails.txt', 'r') as file:
    cocktailList = file.read().split('\n')

for cocktail in cocktailList:
    res = getCocktail(cocktail)
    while not res:
        res = getCocktail(cocktail)
'''

getCocktail("Tequila Sunrise")
print("Done")