from .tool import Tool
from .category import Category
from db import DB_PATH
from banner import load_banner

TOOL = Tool()
CATEGORY = Category()
VERSION = "0.0.3"
AUTHOR = "Olliv3r"
BANNER_MENU = load_banner("menu")
BANNER_REPORT = load_banner("report", center=True)

TOTAL_TOOLS = TOOL.select().count().execute()
TOTAL_CATEGORIES = CATEGORY.select().count().execute()
