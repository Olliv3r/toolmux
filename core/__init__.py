from .tool import Tool
from db import DB_PATH

TOOL = Tool()
VERSION = "0.0.3"
AUTHOR = "Olliv3r"

try:
    TOTAL_TOOLS = TOOL.get_total_tools().fetchone()[0]
except AttributeError:
    TOTAL_TOOLS = 0
