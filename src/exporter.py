import os
from datetime import datetime

import pandas as pd

from src.employee import get_all_employees


def export_employees_to_excel(output_folder="output"):
    """导出员工数据到 Excel，并自动带时间戳"""

    os.makedirs(output_folder, exist_ok=True)

    employees = get_all_employees()

    columns = ["ID", "姓名", "年龄", "部门", "职位", "工资"]

    df = pd.DataFrame(employees, columns=columns)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_folder, f"employees_{now}.xlsx")

    df.to_excel(output_path, index=False)

    return output_path