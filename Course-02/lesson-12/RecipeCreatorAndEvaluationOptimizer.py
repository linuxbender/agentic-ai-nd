import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(
    base_url = "https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"))

# --- Helper Function for API Calls ---
def call_openai(system_prompt, user_prompt, model="gpt-3.5-turbo", tmptur=0):
    """Simple wrapper for OpenAI API calls."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature= tmptur
    )
    return response.choices[0].message.content

MAX_RETRIES = 5

# Example user constraints
RECIPE_REQUEST = {
    "base_dish": "pasta",
    "constraints": [
        "gluten-free",
        "vegan",
        "under 500 calories per serving",
        "high protein (>15g per serving)",
        "no coconut",
        "taste must be rated 7/10 or higher"
    ]
}

class RecipeCreatorAgent:
    """
    Recipe Creator Agent
    use create_recipe to start the work
    """
    def create_recipe(self, recipe_request_dict, feedback=None):

        system_message = """
            You are a creative chef known for generating innovative dishes.
            Prioritize flavor and general appeal. Follow dietary guidelines, but you can be flexible unless told otherwise.
            Experiment with different flavors, styles, try fusion of different places, each time you are asked it must be 
            something new, follow the instructions but be flexible to invent something new, never seen before.
            Try foods that are slightly outside the guilines given, experiment, try something bold, don't be affraid to break 
            the rules.
        """

        if feedback is None:
            user_prompt = f"""Recipe Request: {recipe_request_dict}
            
            Create an exciting, flavorful recipe inspired by comfort food classics.
            Do your best to follow the dietary guidelines, but prioritize creativity and taste first."""

        else:
            system_message = """You are an expert chef specializing in creating recipes that follow strict dietary constraints.
            You must correct previous issues and follow all requirements with precision."""

            user_prompt = f"""Recipe Request: {recipe_request_dict}
            
            Your previous recipe had the following issues:
            {feedback}
            
            Please create a revised recipe addressing these specific issues.
            Be precise and ensure all constraints are satisfied."""


        return call_openai(system_message, user_prompt, "gpt-4", 1)


class NutritionEvaluatorAgent:
    """Nutrition Evaluator Agent
    use evaluate to start the work
    """
    def evaluate(self, recipe_details_str, original_request_dict):
        system_message = "You are a nutrition expert."
        user_prompt = f"Evaluate this recipe: {recipe_details_str}"
        return call_openai(system_message, user_prompt, "gpt-4", 1)


def optimize_recipe():
    """
    starts the optimize recipe workflow
    """

    creator = RecipeCreatorAgent()
    evaluator = NutritionEvaluatorAgent()


if __name__ == "__main__":
    print("Starting AI Recipe Optimizer Workflow...")

    recipe_request = """
        Create a dinner recipe with the following requirements:
            - Must be high in protein (at least 30g per serving)
            - Must be low in carbohydrates (under 15g per serving)
            - Cannot contain gluten, dairy, or nuts (severe allergies)
            - Must be suitable for someone with diabetes (low glycemic index)
            - Should have no more than 8 ingredients
            - Must be flavorful and appealing to someone who normally eats a standard American diet
            - Total preparation and cooking time should be under 30 minutes
            - Should contain at least 3 different vegetables
            - Must include a source of omega-3 fatty acids
        """

    print("\nRecipe Request:")
    print(recipe_request)
    optimize_recipe()

