"""CLI entrypoint for WoodFlow.

This file now delegates logic to the `woodflow` package.
"""
from woodflow import calendar as cal
from woodflow import storage
from woodflow import workbook
import os
from datetime import datetime


def main(year: int | None = None, month: int | None = None, template_file: str | None = None, out_dir: str | None = None):
    year = year or datetime.now().year
    month = month or datetime.now().month
    out_dir = out_dir or os.path.expanduser('~/Desktop/Отчёты')
    os.makedirs(out_dir, exist_ok=True)

    # load last state
    shift_file = os.path.join(out_dir, 'shift_log.json')
    state = storage.load_shift_state(shift_file)
    # For January 2026, initialize with shift=1 (so Jan 4 starts with shift=0)
    # Otherwise use stored state
    if not state and year == 2026 and month == 1:
        start_shift = 1
    else:
        start_shift = state.get('shift_counter', 0)

    dates, end_shift = cal.generate_working_dates(year, month, start_shift)

    if not dates:
        print('No working days to create for this month.')
        storage.save_shift_state(shift_file, end_shift, month)
        return

    template_file = template_file or 'шаблон.xlsx'
    output_path = os.path.join(out_dir, f"{cal.russian_month_name(month)}.xlsx")

    wb = workbook.create_report_from_template(template_file, dates)
    wb.save(output_path)

    storage.save_shift_state(shift_file, end_shift, month)

    print(f"Файл создан: {output_path}")
    print(f"Листов с датами: {len(dates)}")
    print(f"Следующая смена начнётся со статуса: {end_shift}")


if __name__ == '__main__':
    main()