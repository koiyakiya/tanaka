__all__ = ('lcl', '_lcldict')

from tanaka.config import I18N
import lightbulb
import hikari


def lcl(locale: str, key: str) -> str:
    return I18N[hikari.Locale(locale)][key.lower()]


_lcldict = lightbulb.DictLocalizationProvider(I18N)
