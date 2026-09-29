"""Streamlit interface for the Employee Management application.

Run with:  streamlit run app.py

This file is only a presentation layer. All business logic and validation
come from the employee_app package (models, utils, employee_service).
"""

import html

import pandas as pd
import streamlit as st

from employee_app import DEFAULT_DATA_FILE, Employee, EmployeeService

# --------------------------------------------------------------------------
# Page configuration and styling
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Employee Management",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    #MainMenu, footer {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px;}

    .hero {
        background: linear-gradient(120deg, #4f46e5 0%, #7c3aed 55%, #db2777 100%);
        border-radius: 18px;
        padding: 1.6rem 2rem;
        margin-bottom: 1.6rem;
        color: #ffffff;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.25);
    }
    .hero h1 {margin: 0; font-size: 1.9rem; font-weight: 700; color: #ffffff;}
    .hero p {margin: 0.3rem 0 0 0; opacity: 0.9; font-size: 1rem;}

    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-radius: 14px;
        padding: 1rem 1.2rem;
    }
    div[data-testid="stMetricLabel"] {opacity: 0.75;}

    .emp-card {
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-left: 5px solid #7c3aed;
        border-radius: 12px;
        padding: 1rem 1.3rem;
        margin: 0.4rem 0 1rem 0;
    }
    .emp-card .name {font-size: 1.15rem; font-weight: 700;}
    .emp-card .meta {opacity: 0.8; font-size: 0.93rem; margin-top: 0.15rem;}

    .badge {
        display: inline-block;
        background: rgba(124, 58, 237, 0.15);
        color: #7c3aed;
        border-radius: 999px;
        padding: 0.1rem 0.7rem;
        font-size: 0.8rem;
        font-weight: 600;
    }

    div[data-testid="stForm"] {
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-radius: 14px;
        padding: 1.4rem;
    }
    .stButton > button, .stFormSubmitButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] {border-right: 1px solid rgba(128, 128, 128, 0.2);}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

COLUMNS = ["ID", "Name", "Department", "Salary", "Email"]

SAMPLE_DATA = [
    (1001, "Aarav Sharma", "Engineering", 92000, "aarav.sharma@company.com"),
    (1002, "Meera Nair", "Engineering", 88000, "meera.nair@company.com"),
    (1003, "Rohan Iyer", "Data Science", 105000, "rohan.iyer@company.com"),
    (1004, "Sara Thomas", "Data Science", 98000, "sara.thomas@company.com"),
    (1005, "Kabir Menon", "Human Resources", 61000, "kabir.menon@company.com"),
    (1006, "Ananya Das", "Marketing", 67000, "ananya.das@company.com"),
    (1007, "Vikram Pillai", "Finance", 79000, "vikram.pillai@company.com"),
    (1008, "Diya Kurian", "Marketing", 64000, "diya.kurian@company.com"),
]


# --------------------------------------------------------------------------
# State and helper functions
# --------------------------------------------------------------------------
def get_service() -> EmployeeService:
    """One EmployeeService per browser session."""
    if "service" not in st.session_state:
        st.session_state.service = EmployeeService(DEFAULT_DATA_FILE)
    return st.session_state.service


def flash(message: str, icon: str = "✅") -> None:
    """Queue a toast that is shown after the next rerun."""
    st.session_state.flash = (message, icon)


def show_flash() -> None:
    if "flash" in st.session_state:
        message, icon = st.session_state.pop("flash")
        st.toast(message, icon=icon)


def to_dataframe(employees) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "ID": e.emp_id,
                "Name": e.name,
                "Department": e.department,
                "Salary": e.salary,
                "Email": e.email,
            }
            for e in employees
        ],
        columns=COLUMNS,
    )


def table(df: pd.DataFrame) -> None:
    st.dataframe(
        df,
        hide_index=True,
        width="stretch",
        column_config={
            "ID": st.column_config.NumberColumn("ID", format="%d", width="small"),
            "Salary": st.column_config.NumberColumn("Salary", format="%.2f"),
            "Email": st.column_config.TextColumn("Email", width="large"),
        },
    )


def page_header(title: str, subtitle: str) -> None:
    st.markdown(
        f'<div class="hero"><h1>{html.escape(title)}</h1>'
        f"<p>{html.escape(subtitle)}</p></div>",
        unsafe_allow_html=True,
    )


def employee_card(emp: Employee) -> None:
    st.markdown(
        f"""
        <div class="emp-card">
            <div class="name">{html.escape(emp.name)}
                &nbsp;<span class="badge">{html.escape(emp.department)}</span></div>
            <div class="meta">Employee ID {emp.emp_id} &nbsp;·&nbsp; {html.escape(emp.email)}</div>
            <div class="meta">Salary {emp.salary:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(service_is_empty: bool = True) -> None:
    st.info(
        "No employees yet. Use **Add Employee** to create one, "
        "or load demo records from the sidebar."
    )


def label_for(service: EmployeeService, emp_id: int) -> str:
    return f"{emp_id} · {service.get_employee(emp_id).name}"


def next_free_id(service: EmployeeService) -> int:
    ids = [e.emp_id for e in service.get_all_employees()]
    return (max(ids) + 1) if ids else 1001


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
def page_dashboard(service: EmployeeService) -> None:
    page_header("Dashboard", "A live overview of your workforce.")
    employees = service.get_all_employees()
    if not employees:
        empty_state()
        return

    df = to_dataframe(employees)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total employees", len(df))
    c2.metric("Departments", df["Department"].nunique())
    c3.metric("Average salary", f"{df['Salary'].mean():,.0f}")
    c4.metric("Total payroll", f"{df['Salary'].sum():,.0f}")

    st.write("")
    left, right = st.columns(2)
    with left:
        st.subheader("Headcount by department")
        st.bar_chart(df.groupby("Department").size(), color="#7c3aed")
    with right:
        st.subheader("Average salary by department")
        st.bar_chart(df.groupby("Department")["Salary"].mean().round(0), color="#db2777")

    st.subheader("Top earners")
    table(df.sort_values("Salary", ascending=False).head(5))


def page_add(service: EmployeeService) -> None:
    page_header("Add Employee", "Create a new employee record.")
    st.session_state.setdefault("add_counter", 0)
    n = st.session_state.add_counter

    with st.form(f"add_form_{n}"):
        c1, c2 = st.columns(2)
        emp_id = c1.number_input(
            "Employee ID", min_value=1, step=1, value=next_free_id(service),
            key=f"add_id_{n}", help="Must be unique.",
        )
        name = c2.text_input("Full name", key=f"add_name_{n}", placeholder="e.g. Anita Menon")
        department = c1.text_input("Department", key=f"add_dept_{n}", placeholder="e.g. Engineering")
        salary = c2.number_input(
            "Salary", min_value=0.0, step=1000.0, value=0.0, format="%.2f", key=f"add_sal_{n}",
        )
        email = st.text_input("Email", key=f"add_email_{n}", placeholder="name@company.com")
        submitted = st.form_submit_button("➕ Add employee", type="primary")

    if submitted:
        try:
            emp = service.add_employee(int(emp_id), name, department, salary, email)
        except ValueError as error:
            st.error(str(error))
        else:
            st.session_state.add_counter += 1  # resets the form fields
            flash(f"Added {emp.name} (ID {emp.emp_id})")
            st.rerun()


def page_search(service: EmployeeService) -> None:
    page_header("Search Employees", "Find people by ID, name or department, then refine with filters.")
    employees = service.get_all_employees()
    if not employees:
        empty_state()
        return

    df_all = to_dataframe(employees)
    query = st.text_input("🔍 Search", placeholder="Type an ID, a name or a department…")

    f1, f2 = st.columns([2, 2])
    departments = sorted(df_all["Department"].unique())
    chosen = f1.multiselect("Filter by department", departments)
    low, high = float(df_all["Salary"].min()), float(df_all["Salary"].max())
    if low < high:
        salary_range = f2.slider("Salary range", low, high, (low, high))
    else:
        salary_range = (low, high)
        f2.caption(f"All employees earn {low:,.2f}.")

    results = service.search_employees(query) if query.strip() else employees
    df = to_dataframe(results)
    if chosen:
        df = df[df["Department"].isin(chosen)]
    df = df[df["Salary"].between(*salary_range)]

    st.caption(f"{len(df)} result(s)")
    if df.empty:
        st.warning("No employees match your search.")
    else:
        table(df)


def page_update(service: EmployeeService) -> None:
    page_header("Update Employee", "Edit an existing record. Only changed values are saved.")
    ids = [e.emp_id for e in service.get_all_employees()]
    if not ids:
        empty_state()
        return

    emp_id = st.selectbox("Select employee", ids, format_func=lambda i: label_for(service, i))
    emp = service.get_employee(emp_id)
    employee_card(emp)

    with st.form(f"update_form_{emp_id}"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full name", emp.name, key=f"upd_name_{emp_id}")
        department = c2.text_input("Department", emp.department, key=f"upd_dept_{emp_id}")
        salary = c1.number_input(
            "Salary", min_value=0.0, step=1000.0, value=float(emp.salary),
            format="%.2f", key=f"upd_sal_{emp_id}",
        )
        email = c2.text_input("Email", emp.email, key=f"upd_email_{emp_id}")
        submitted = st.form_submit_button("💾 Save changes", type="primary")

    if submitted:
        try:
            updated = service.update_employee(emp_id, name, department, salary, email)
        except ValueError as error:
            st.error(str(error))
        else:
            flash(f"Updated {updated.name}")
            st.rerun()


def page_delete(service: EmployeeService) -> None:
    page_header("Delete Employee", "Permanently remove a record. This cannot be undone.")
    ids = [e.emp_id for e in service.get_all_employees()]
    if not ids:
        empty_state()
        return

    emp_id = st.selectbox("Select employee", ids, format_func=lambda i: label_for(service, i))
    emp = service.get_employee(emp_id)
    employee_card(emp)

    confirmed = st.checkbox("I understand this action is permanent.", key=f"del_confirm_{emp_id}")
    if st.button("🗑️ Delete employee", type="primary", disabled=not confirmed):
        try:
            removed = service.delete_employee(emp_id)
        except KeyError as error:
            st.error(error.args[0])
        else:
            flash(f"Deleted {removed.name}", icon="🗑️")
            st.rerun()


def page_all(service: EmployeeService) -> None:
    page_header("All Employees", "Browse, sort and export the full employee list.")
    employees = service.get_all_employees()
    if not employees:
        empty_state()
        return

    df = to_dataframe(employees)
    st.caption(f"{len(df)} employee(s). Click a column header to sort.")
    table(df)
    st.download_button(
        "⬇️ Download as CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="employees.csv",
        mime="text/csv",
    )


PAGES = {
    "📊 Dashboard": page_dashboard,
    "➕ Add Employee": page_add,
    "🔍 Search": page_search,
    "✏️ Update Employee": page_update,
    "🗑️ Delete Employee": page_delete,
    "📋 All Employees": page_all,
}


# --------------------------------------------------------------------------
# Sidebar and routing
# --------------------------------------------------------------------------
def load_sample_data(service: EmployeeService) -> int:
    added = 0
    for record in SAMPLE_DATA:
        try:
            service.add_employee(*record)
            added += 1
        except ValueError:
            pass  # already loaded
    return added


def main() -> None:
    service = get_service()

    with st.sidebar:
        st.markdown("## 👥 Employee Manager")
        page = st.radio("Navigate", list(PAGES), label_visibility="collapsed")
        st.divider()
        st.metric("Employees stored", service.count())

        if st.button("Load demo data", width="stretch"):
            added = load_sample_data(service)
            flash(f"Loaded {added} demo employee(s)" if added else "Demo data already loaded",
                  icon="📥" if added else "ℹ️")
            st.rerun()
        if st.button("Clear all data", width="stretch", disabled=service.count() == 0):
            service.clear_all()
            flash("All records cleared", icon="🧹")
            st.rerun()
        st.caption("Saved automatically to data/employees.json")

    show_flash()
    PAGES[page](service)


if __name__ == "__main__":
    main()