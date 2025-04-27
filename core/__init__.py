from .tool import Tool
from .category import Category
from db import DB_PATH

TOOL = Tool()
CATEGORY = Category()
VERSION = "0.0.3"
AUTHOR = "Olliv3r"

TOTAL_TOOLS = TOOL.select().count().execute()
TOTAL_CATEGORIES = CATEGORY.select().count().execute()
