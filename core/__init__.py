from banner import load_banner
from core.models import Session, Tool
import os
import sqlalchemy as sa

VERSION = "0.0.4"
AUTHOR = "Olliv3r"
BANNER_MENU = load_banner("menu")
BANNER_REPORT = load_banner("report", center=True)

session = Session()

total_tools = session.scalar(sa.select(sa.func.count(Tool.id)))
