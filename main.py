import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
# Hello from new subject I need to study for me to pass my exams
# Your API key for Spoonacular API
API_KEY = '9f46ac46373b4b69afc652edd022063d'

# Your Telegram Bot Token
TOKEN = '7962516434:AAFB8jcyOR5xfcc62ExFf56wclR9XR09Rr8'

# Function to get a random recipe
async def get_random_recipe():
    url = f'https://api.spoonacular.com/recipes/random?apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and 'recipes' in data:
        recipe = data['recipes'][0]
        title = recipe['title']
        instructions = recipe.get('instructions', "No instructions available.")
        return f"🍽 *Recipe:* {title}\n\n📜 *Instructions:* {instructions}", recipe.get("image", "")
    else:
        return "❌ Sorry, I couldn't fetch a recipe. Please try again later.", ""

# Function to get recipes by ingredients
async def get_recipes_by_ingredients(ingredients):
    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and len(data) > 0:
        recipe = data[0]
        title = recipe['title']
        id = recipe['id']
        return f"🍲 *Recipe:* {title}\n🔗 [View Recipe](https://spoonacular.com/recipes/{title.replace(' ', '-')}-{id})", recipe.get("image", "")
    else:
        return "❌ Sorry, I couldn't find any recipes with those ingredients.", ""

# Function to handle the /start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "👋 Welcome! I can help you find delicious recipes. Try these commands:\n"
        "✅ /randomrecipe - Get a random recipe\n"
        "✅ /recipe <ingredients> - Get recipes by ingredients\n"
        "✅ /help - Get help on how to use the bot"
    )

# Function to handle the /randomrecipe command
async def random_recipe(update: Update, context: CallbackContext):
    message, image_url = await get_random_recipe()
    if image_url:
        await update.message.reply_photo(image_url, caption=message, parse_mode="Markdown")
    else:
        await update.message.reply_text(message, parse_mode="Markdown")

# Function to handle the /recipe command
async def recipe_by_ingredients(update: Update, context: CallbackContext):
    if context.args:
        ingredients = ','.join(context.args)
        message, image_url = await get_recipes_by_ingredients(ingredients)
        if image_url:
            await update.message.reply_photo(image_url, caption=message, parse_mode="Markdown")
        else:
            await update.message.reply_text(message, parse_mode="Markdown")
    else:
        await update.message.reply_text("❗ Please provide some ingredients after the /recipe command.\nExample: `/recipe chicken tomato`", parse_mode="Markdown")

# Function to handle the /help command
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "ℹ️ To use the bot, try these commands:\n"
        "✅ /randomrecipe - Get a random recipe\n"
        "✅ /recipe <ingredients> - Get recipes by ingredients (e.g. `/recipe chicken tomato`)"
    )

# Main function to start the bot
def main():
    app = Application.builder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("randomrecipe", random_recipe))
    app.add_handler(CommandHandler("recipe", recipe_by_ingredients))
    app.add_handler(CommandHandler("help", help_command))

    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
