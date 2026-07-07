import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext

from src.database import init_database
from src.employee import (
    add_employee,
    get_all_employees,
    delete_employee,
    update_employee,
    search_employees
)
from src.exporter import export_employees_to_excel
from src.logger import setup_logger


class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System v2.1")
        self.root.geometry("1020x760")

        init_database()
        self.logger = setup_logger()
        self.selected_emp_id = None

        self.build_ui()
        self.load_employees()
        self.write_log("系统启动完成")

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="Employee Management System",
            font=("Microsoft YaHei UI", 18, "bold")
        )
        title.pack(pady=10)

        subtitle = tk.Label(
            self.root,
            text="企业员工信息管理系统：SQLite数据库、员工增删改查、搜索、Excel导出、运行日志",
            font=("Microsoft YaHei UI", 10)
        )
        subtitle.pack(pady=3)

        form = tk.Frame(self.root)
        form.pack(fill="x", padx=30, pady=10)

        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.position_var = tk.StringVar()
        self.salary_var = tk.StringVar()

        labels = ["姓名：", "年龄：", "部门：", "职位：", "工资："]
        vars_ = [
            self.name_var,
            self.age_var,
            self.department_var,
            self.position_var,
            self.salary_var
        ]

        for i, (label, var) in enumerate(zip(labels, vars_)):
            tk.Label(form, text=label, width=8, anchor="w").grid(row=i, column=0, pady=5)
            tk.Entry(form, textvariable=var, width=40).grid(row=i, column=1, pady=5, padx=5)

        search_frame = tk.Frame(self.root)
        search_frame.pack(fill="x", padx=30, pady=5)

        self.search_var = tk.StringVar()

        tk.Label(search_frame, text="搜索：", width=8, anchor="w").pack(side="left")

        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side="left", padx=5)
        search_entry.bind("<Return>", lambda event: self.search_employee())

        tk.Button(search_frame, text="搜索员工", width=12, command=self.search_employee).pack(side="left", padx=5)
        tk.Button(search_frame, text="显示全部", width=12, command=self.load_employees).pack(side="left", padx=5)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="新增员工", width=13, command=self.add_employee).grid(row=0, column=0, padx=6)
        tk.Button(button_frame, text="修改员工", width=13, command=self.update_employee).grid(row=0, column=1, padx=6)
        tk.Button(button_frame, text="删除员工", width=13, command=self.delete_employee).grid(row=0, column=2, padx=6)
        tk.Button(button_frame, text="刷新列表", width=13, command=self.load_employees).grid(row=0, column=3, padx=6)
        tk.Button(button_frame, text="导出Excel", width=13, command=self.export_excel).grid(row=0, column=4, padx=6)
        tk.Button(button_frame, text="清空输入", width=13, command=self.clear_form).grid(row=0, column=5, padx=6)

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)

        columns = ("no", "id", "name", "age", "department", "position", "salary")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        headings = {
            "no": "序号",
            "id": "数据库ID",
            "name": "姓名",
            "age": "年龄",
            "department": "部门",
            "position": "职位",
            "salary": "工资"
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=120, anchor="center")

        self.tree.column("no", width=80, anchor="center")
        self.tree.column("id", width=100, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.pack(fill="both", expand=True)

        self.status_var = tk.StringVar(value="员工人数：0")
        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="w",
            font=("Microsoft YaHei UI", 9)
        )
        status_label.pack(fill="x", padx=30, pady=5)

        tk.Label(self.root, text="运行日志：", anchor="w").pack(fill="x", padx=30)

        self.log_box = scrolledtext.ScrolledText(self.root, height=6)
        self.log_box.pack(fill="x", padx=30, pady=5)

    def add_employee(self):
        try:
            name, age, department, position, salary = self.get_form_data()

            add_employee(name, age, department, position, salary)
            self.logger.info(f"新增员工：{name}")
            self.write_log(f"新增员工：{name}")

            self.load_employees()
            self.clear_form()

            messagebox.showinfo("成功", "员工新增成功")

        except ValueError:
            messagebox.showerror("错误", "年龄必须是整数，工资必须是数字")

        except Exception as e:
            messagebox.showerror("错误", str(e))

    def update_employee(self):
        try:
            if not self.selected_emp_id:
                messagebox.showwarning("提示", "请先选择要修改的员工")
                return

            name, age, department, position, salary = self.get_form_data()

            update_employee(
                self.selected_emp_id,
                name,
                age,
                department,
                position,
                salary
            )

            self.logger.info(f"修改员工：{name}")
            self.write_log(f"修改员工：{name}")

            self.load_employees()
            self.clear_form()

            messagebox.showinfo("成功", "员工修改成功")

        except ValueError:
            messagebox.showerror("错误", "年龄必须是整数，工资必须是数字")

        except Exception as e:
            messagebox.showerror("错误", str(e))

    def delete_employee(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("提示", "请先选择要删除的员工")
            return

        item = self.tree.item(selected[0])
        emp_id = item["values"][1]
        name = item["values"][2]

        confirm = messagebox.askyesno("确认删除", f"确定删除员工：{name} 吗？")

        if confirm:
            delete_employee(emp_id)
            self.logger.info(f"删除员工：{name}")
            self.write_log(f"删除员工：{name}")

            self.load_employees()
            self.clear_form()

            messagebox.showinfo("成功", "员工删除成功")

    def search_employee(self):
        keyword = self.search_var.get().strip()

        if not keyword:
            messagebox.showwarning("提示", "请输入搜索关键词")
            return

        employees = search_employees(keyword)
        self.show_employees(employees)

        self.status_var.set(f"搜索结果：{len(employees)} 条")
        self.write_log(f"搜索员工：{keyword}，结果 {len(employees)} 条")

    def load_employees(self):
        employees = get_all_employees()
        self.show_employees(employees)

        self.status_var.set(f"员工人数：{len(employees)}")
        self.write_log(f"刷新员工列表，共 {len(employees)} 条")

    def show_employees(self, employees):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, emp in enumerate(employees, start=1):
            values = list(emp)
            values[5] = f"{float(values[5]):.2f}"

            display_values = [
                index,
                values[0],
                values[1],
                values[2],
                values[3],
                values[4],
                values[5],
            ]

            self.tree.insert("", "end", values=display_values)

    def export_excel(self):
        try:
            path = export_employees_to_excel()
            self.logger.info(f"导出员工数据：{path}")
            self.write_log(f"导出Excel：{path}")

            messagebox.showinfo("导出成功", f"导出成功：\n{path}")

        except Exception as e:
            messagebox.showerror("导出失败", str(e))

    def on_select(self, event):
        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(selected[0])
        values = item["values"]

        self.selected_emp_id = values[1]
        self.name_var.set(values[2])
        self.age_var.set(values[3])
        self.department_var.set(values[4])
        self.position_var.set(values[5])
        self.salary_var.set(values[6])

    def get_form_data(self):
        name = self.name_var.get().strip()
        age = int(self.age_var.get().strip())
        department = self.department_var.get().strip()
        position = self.position_var.get().strip()
        salary = float(self.salary_var.get().strip())

        if not name:
            raise Exception("姓名不能为空")

        return name, age, department, position, salary

    def clear_form(self):
        self.selected_emp_id = None
        self.name_var.set("")
        self.age_var.set("")
        self.department_var.set("")
        self.position_var.set("")
        self.salary_var.set("")

    def write_log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()