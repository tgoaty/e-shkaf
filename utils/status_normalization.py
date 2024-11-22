def get_normal_status_name(status_name):
    translate = {
        'C1:PREPARATION': 'Подготовка документов',
        'C1:PREPAYMENT_INVOICE': 'Счёт на предоплату',
        'C1:EXECUTING': 'В работе',
        'C1:FINAL_INVOIC': 'Финальный счет',
        'C1:WON': 'Сделка успешна',
        'C1:LOSE': 'Сделка провалена',
        'C1:APOLOGY': 'Анализ причины провала'

    }
    return translate[status_name]