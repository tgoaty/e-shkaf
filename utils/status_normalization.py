async def get_normal_status_name(status_name):
    """
    Перевод стадий на русский.
    """
    from create_bot import cache_manager

    deal_categories = await cache_manager.get_deal_categories()

    return deal_categories.get(status_name, [status_name, 0])[0]