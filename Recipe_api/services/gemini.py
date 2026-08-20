from google import genai 
import json
from Recipe_api.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


async def suggest_meals(craving: str, cuisine_type: str, dietary_preference: str, cooking_time:str) -> list:
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
    response = await client.aio.models.generate_content(model="gemini-2.5-flash",
                                                        contents=prompt)
    response_text = response.text.strip()

    
    meals = json.loads(response_text)
    return meals


async def generate_recipe(meal_name: str, cuisine_type: str, dietary_preference: str, cooking_time:str) -> dict:
    prompt = f"""
                You are a professional chef and food expert.

                Generate a detailed recipe for: {meal_name}
                Cuisine type: {cuisine_type}
                Dieatary requirement: {dietary_preference}
                Cooking time: {cooking_time}

                Respond ONLY with a JSON object, nothing else.
                No explanation, no markdown, no backticks.

                Use exactly this format:
                {{
                "meal_name": "{meal_name}",
                "ingredients": "list every ingredient with quantity, separated by newlines",
                "steps": "list every cooking step clearly, separated by newlines",
                "tips": "2-3 helpful cooking tips for this meal"
                }}
                """
    response = await client.aio.models.generate_content(model="gemini-2.5-flash",
                                                        contents=prompt)
    text = response.text.strip()

    
    text = text.replace("```json", "").replace("```", "").strip()
    recipe = json.loads(text)
    return recipe
