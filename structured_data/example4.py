
from typing import List, Optional
from typing import Optional, List

from pydantic import BaseModel, Field
import os

from agents import Agent,ItemHelpers,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper, Runner,set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv(find_dotenv())
gemini_api_key: str | None = os.environ.get("GOOGLE_API_KEY")

set_tracing_disabled(disabled=True)
external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_provider : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model='gemini-2.5-flash', openai_client=external_client) 

from typing import List, Optional

class Ingredient(BaseModel):
    name: str
    amount: str
    unit: str
    notes: Optional[str] = None

class NutritionInfo(BaseModel):
    calories_per_serving: Optional[int] = None
    prep_time_minutes: int
    cook_time_minutes: int
    difficulty_level: str = Field(..., pattern=r'^(easy|medium|hard)$')

class Recipe(BaseModel):
    title: str
    description: str
    servings: int
    ingredients: List[Ingredient]
    instructions: List[str]
    nutrition: NutritionInfo
    cuisine_type: str
    dietary_tags: List[str]  # vegetarian, vegan, gluten-free, etc.

# Create recipe analyzer
recipe_analyzer = Agent(
    name="RecipeAnalyzer",
    instructions="Extract detailed recipe information from recipe text.",
    output_type=Recipe ,
    model =  llm_provider
)

# Test with recipe
recipe_text = """
Spaghetti Carbonara
A classic Italian pasta dish with eggs, cheese, and pancetta.
Serves 4 people. Prep time: 15 minutes, Cook time: 20 minutes. Medium difficulty.

Ingredients:
- 400g spaghetti pasta
- 150g pancetta, diced
- 3 large eggs
- 100g Parmesan cheese, grated
- 2 cloves garlic, minced
- Black pepper to taste
- Salt for pasta water

Instructions:
1. Boil salted water and cook spaghetti according to package directions
2. Fry pancetta in a large pan until crispy
3. Beat eggs with Parmesan cheese in a bowl
4. Drain pasta and add to pancetta pan
5. Remove from heat and quickly mix in egg mixture
6. Serve immediately with extra Parmesan

Cuisine: Italian
Dietary notes: Contains gluten, dairy, and eggs
Approximate calories: 650 per serving
"""

result = Runner.run_sync(recipe_analyzer, recipe_text)

print("=== Recipe Analysis ===")
print(f"Title: {result.final_output.title}")
print(f"Description: {result.final_output.description}")
print(f"Servings: {result.final_output.servings}")
print(f"Cuisine: {result.final_output.cuisine_type}")
print(f"Difficulty: {result.final_output.nutrition.difficulty_level}")
print(f"Total Time: {result.final_output.nutrition.prep_time_minutes + result.final_output.nutrition.cook_time_minutes} minutes")

print("\nIngredients:")
for ing in result.final_output.ingredients:
    notes_str = f" ({ing.notes})" if ing.notes else ""
    print(f"  • {ing.amount} {ing.unit} {ing.name}{notes_str}")

print("\nInstructions:")
for i, step in enumerate(result.final_output.instructions, 1):
    print(f"  {i}. {step}")

print(f"\nDietary Tags: {', '.join(result.final_output.dietary_tags)}")
if result.final_output.nutrition.calories_per_serving:
    print(f"Calories per serving: {result.final_output.nutrition.calories_per_serving}")


    