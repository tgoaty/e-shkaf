def get_normal_status_name(status_name):
    """
    Перевод стадий на русский.
    """
    translate = {
        'PREPARATION': 'Подготовка документов',
        'C2:PREPAYMENT_INVOICE': 'Счёт на предоплату',
        'C2:EXECUTING': 'В работе',
        'C2:FINAL_INVOIC': 'Финальный счет',
        'C2:WON': 'Сделка успешна',
        'C2:LOSE': 'Сделка провалена',
        'C2:APOLOGY': 'Анализ причины провала'

    }
    return translate.get(status_name, status_name)