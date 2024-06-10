from datetime import datetime

IGNORE = 'Ignore'
NEXT_YEAR = 'Next_year'
NEXT_MONTH = 'Next_month'
PREVIOUS_YEAR = 'Previous_year'
PREVIOUS_MONTH = 'Previous_month'
YEARS = {
    str(datetime.now().year),
    str(datetime.now().year + 1),
}
MONTHS = {
    str(i) for i in range(1, 13)
}
