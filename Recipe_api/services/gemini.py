import google.generativeai as genini
import json
from Recipe_api.core.security import settings

genini.configure(api_key=settings.GEMINI_API_KEY)
model = genini.GenerativeModel("gemini-1.5-flash")



async def sugguest_meal(craving: str, cuisine_type: str, dietary_preference: str, cooking_time:str) -> list:
    prompt = f""" 
            You are a professional chef and food expert

            A user is craving: {craving}
            Cuisine preference: {cuisine_type}
            Dietary requirement: {dietary_preference}
            Available cooking time: {cooking_time}


            Suggest exactly 5 meal options that match these preferences.

            Respond ONLY with a JSON array of meal names, nothing else.
            No explanation, no numbering, no markdown.

            Example format:
            ["Jollof Rice", "Egusi Soup", "Pepper Soup", "Fried Rice", "Pounded Yam"]
            """
    response = await model.generate_content(prompt)
    response_text = response.text.strip()

    import json
    meals = json.load(response_text)
    return meals