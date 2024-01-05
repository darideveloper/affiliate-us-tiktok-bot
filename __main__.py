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
    bot.show_select_saved_creators()
    
    print("done")