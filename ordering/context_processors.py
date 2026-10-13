from django.conf import settings


def site(request):
    return {
        "CURRENCY": settings.CURRENCY_SYMBOL,
        "TAX_RATE": settings.TAX_RATE,
        "TAX_PERCENT": (settings.TAX_RATE * 100).normalize(),
        "MAX_QTY": settings.MAX_ITEM_QUANTITY,
    }
