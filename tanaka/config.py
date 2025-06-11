from __future__ import annotations
import glob
from pathlib import Path
import hikari

__all__ = ('__TOKEN__', 'I18N')

import dotenv
import os
from typing import Final
import hikari
import orjson

dotenv.load_dotenv()

__TOKEN__: Final[str] = os.getenv('BOT_TOKEN', '')
"""The bot token used to connect to Discord."""

I18N = {}
_paths = glob.glob('i18n/*.json')
for path in _paths:
    with open(path, 'rb') as f:
        data = orjson.loads(f.read())
        I18N[hikari.Locale(Path(path).stem)] = data
