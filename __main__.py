import os
from dotenv import load_dotenv
from logs import logger
from libs.bot import Bot

load_dotenv()
CHROME_FOLDER = os.getenv("CHROME_FOLDER")
CATEGORY = os.getenv("CATEGORY")
FOLLOWERS = os.getenv("FOLLOWERS")
CONTENT_TYPE = os.getenv("CONTENT_TYPE")
CREATOR_AGENCY = os.getenv("CREATOR_AGENCY")
CREATORS_NUM_LOOP = int(os.getenv("CREATORS_NUM_LOOP"))
PRODUCT_ID = int(os.getenv("PRODUCT_ID"))
PRODUCT_PERCENTAGE = int(os.getenv("PRODUCT_PERCENTAGE"))

if __name__ == '__main__':
    
    logger.info("Starting bot...")
    bot = Bot(
        CHROME_FOLDER,
        CREATORS_NUM_LOOP
    )
    
    # Login validation
    is_logged = bot.login()
    if not is_logged:
        logger.error("Error: Login failed")
        quit()
    
    logger.info("Filtering creators...")
    bot.filter_creators(
        CATEGORY,
        FOLLOWERS,
        CONTENT_TYPE,
        CREATOR_AGENCY
    )
    
    logger.info("Saving creators...")
    # bot.save_creators()
    
    logger.info("Selecting creators...")
    creators_selected = bot.select_creators()
    if not creators_selected:
        logger.error("Error: No enough creators found")
        quit()
    
    logger.info("Selecting product...")
    product_selected = bot.select_product(
        PRODUCT_ID,
        PRODUCT_PERCENTAGE
    )
    if not product_selected:
        logger.error("Error: Product not found")
        quit()
    
    print("done")