import json
import random

import arrow
import requests


def lambda_handler(event, context):
    ELEMENTARY_MENU_ID = "31373"
    MIDDLE_MENU_ID = "31376"

    menu_id = ELEMENTARY_MENU_ID

    try:
        school_type = event.get("queryStringParameters").get("school_type")
    except (AttributeError, KeyError) as e:
        school_type = "ELEMENTARY"

    if school_type == "MIDDLE":
        menu_id = MIDDLE_MENU_ID

    output = None
    entrees = list()

    district_id = "1294"

    menu_url = f"https://www.myschoolmenus.com/api/public/menus/{menu_id}"
    headers = {"x-district":district_id}

    response = requests.get(menu_url, headers=headers)

    tomorrow = arrow.utcnow().to('US/Eastern').shift(days=1)
    formatted_tomorrow = tomorrow.format('YYYY-MM-DD')
    response_data = response.json()

    calendar = response_data.get("data").get("menu_month_calendar")
    for item in calendar:
        if not type(item) == type(dict()):
            continue
        day = item.get("day")
        if day == formatted_tomorrow:
            display = json.loads(item.get("setting"))

            # because there's no structure to the list, headers and recipes are equivalent. We'll use a flag to determine whether
            # recipes we encounter should be processed as such
            is_collecting_entrees = False

            for daily_item in display.get("current_display"):
                item_type = daily_item.get('type', "").lower()
                item_name = daily_item.get('name', "").lower()

                # flip the flag to determine whether we should be paying attention to recipes in future iterations of the loop
                if item_type == "category":
                    is_collecting_entrees = True if item_name == "entree" else False

                if is_collecting_entrees and item_type == "recipe":
                    entrees.append(item_name)

    if not entrees:
        output = "Quack, quack. There's no school tomorrow, you lucky ducks!"
    else:
        if len(entrees) > 1:
            entree_descriptor = "{0}, and {1}".format(', '.join(entrees[:-1]), entrees[-1])
        else:
            entree_descriptor = entrees[0]

        # remove jargon from the item name
        entree_descriptor = entree_descriptor.replace(", ms/hs", "")

        if "taco" in entree_descriptor:
            output = f"It's your lucky day, amigos! Take your pick from {entree_descriptor}."
        elif "brunch" in entree_descriptor:
            output = f"Bring a steaming cup of hot cocoa and bath robe kiddos, it's brunch for lunch! Choose from {entree_descriptor}."
        elif "turkey" in entree_descriptor:
            output = f"Gobble, gobble. Get ready for {entree_descriptor}."
        elif "spicy chicken sandwich" in entree_descriptor:
            output = f"Hey, hot tamale! Spicy Chicken is on the menu! But the full list is {entree_descriptor}."
        elif "fettucine" in entree_descriptor:
            output = f"Bada Bing! It's fettucine day! Grab yourself one of {entree_descriptor}."
        elif "quesadilla" in entree_descriptor:
            output = f"We're going south of the border today! Take your pick from {entree_descriptor}."
        else:
            adjective = random.choice(["delicious", "scrumptious", "amazing", "delightful", "spectacular", "wonderful", "stupendous", "unbelievable", "delectible"])
            output = f"Tomorrow's {adjective} entrees include {entree_descriptor}!"

    return {
        'statusCode': 200,
        'body': json.dumps(output)
    }
