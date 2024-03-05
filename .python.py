import requests
import pandas as pd
import sys

def fetch_menu_data(restaurant_id):
    """
    Fetches menu data for a given restaurant_id from Swiggy's API.

    Parameters:
    - restaurant_id: str, The unique identifier for the restaurant.

    Returns:
    - A JSON object containing the menu data.
    """
    # Constructing the API URL with the provided restaurant_id
    api_url = f"https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=18.56&lng=73.95&restaurantId={restaurant_id}"
    response = requests.get(api_url)
    # Check if the API request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data from API.")
        sys.exit(1)

def parse_menu_data(menu_data):
    """
    Parses the JSON response from the API and extracts relevant menu item details.

    Parameters:
    - menu_data: dict, The JSON response from the API.

    Returns:
    - A list of dictionaries, each containing a menu item's details.
    """
    items = []
    # Iterating through each category in the menu
    for category in menu_data['data']['menu']:
        category_name = category['name']
        # Iterating through each item in the category
        for item in category['items']:
            items.append({
                "Category": category_name,
                "Dish Name": item['name'],
                "Price": item['price'],
                "Description": item.get('description', '')
            })
    return items

def save_to_csv(items, filename="menu_data.csv"):
    """
    Saves the extracted menu data into a CSV file.

    Parameters:
    - items: list of dicts, The extracted menu items.
    - filename: str, The name of the CSV file to save the data to.
    """
    df = pd.DataFrame(items)
    df.to_csv(filename, index=False)
    print(f"Menu data saved to {filename}")

def main(restaurant_id):
    """
    Main function to fetch, parse, and save the restaurant menu data.

    Parameters:
    - restaurant_id: str, The unique identifier for the restaurant.
    """
    menu_data = fetch_menu_data(restaurant_id)
    items = parse_menu_data(menu_data)
    save_to_csv(items)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <restaurant_id>")
        sys.exit(1)
    restaurant_id = sys.argv[1]
    main(restaurant_id)
