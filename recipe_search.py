import requests
from pprint import pprint


# Function for user to input an ingredient
def get_ingredient():
    ingredient = input("Enter an ingredient >> ")
    return ingredient


# Function to configure url
def configure_url():
    url_info = {'APP_ID': '1f256ae9', 'APP_KEY': 'f1daa87c3e0273c6a71f97718be79f01',
                'INGREDIENT': get_ingredient()}
    # url with interpolated parameters
    url = 'https://api.edamam.com/search?q=' + url_info['INGREDIENT'] + '&app_id=' + url_info[
        'APP_ID'] + '&app_key=' + url_info['APP_KEY']
    return url


list_of_recipes = []


# configure_url()


def get_api_response():
    url = configure_url()
    response = requests.get(url)
    return response


# Method to print retrieved recipe names and check for invalid input
def get_recipes():
    response = get_api_response()
    recipes = response.json()

    status_code = response.status_code
    while status_code != 200:
        print("Sorry, an error has occurred. Try again.")
        get_ingredient()
        response = get_api_response()
        recipes = response.json()
        status_code = response.status_code

    hit_list = recipes['hits']
    while len(hit_list) <= 0:
        print("Sorry, there are no recipes for that ingredient. Try again.")
        response = get_api_response()
        recipes = response.json()
        status_code = response.status_code
        while status_code != 200:
            print("Sorry, an error has occurred. Try again.")
            get_ingredient()
            response = get_api_response()
            recipes = response.json()
            status_code = response.status_code

    hit_list = recipes['hits']

    print("The following recipe(s) contain your chosen ingredient: ")
    for item in hit_list:
        dictionary_of_details = item['recipe']
        recipe_names = (dictionary_of_details['label'])
        recipe_url = (dictionary_of_details['url'])
        recipe_display = recipe_names + " " + recipe_url
        pprint(recipe_display)


get_recipes()


# save recipe function, writes chosen recipe to text file
def save_recipe(rec):
    list_of_recipes.append(rec)
    with open('recipe.txt', 'w+') as text_file:
        for recipe in list_of_recipes:
            text_file.write(recipe + '\n')


# Check if user would like to save a recipe (write it to a file)
answer = input("Would you like to save a recipe? y/n >> ")
while answer == 'y':
    chosen_recipe = input("Which recipe would you like to save? >> ")
    save_recipe(chosen_recipe)
    answer = input("Would you like to save another recipe? y/n >> ")
    if answer == 'n':
        print("Thank you for using recipe search.")
