import pandas as pd
import numpy as np

# =========================================================
# 1. FILE PATH
# =========================================================

input_file = r"C:\Users\Hooooo\Documents\Excel\MIS_Workforce_Analytics\Dataset\MIS_Workforce_Productivity_Attrition_Capacity_Dataset.xlsx"

output_file = r"C:\Users\Hooooo\Documents\Excel\MIS_Workforce_Analytics\Cleaned\MIS_Workforce_Cleaned.xlsx"

# =========================================================
# 2. LOAD ALL DATASETS
# =========================================================

employee = pd.read_excel(input_file, sheet_name="Employee_Master")
attendance = pd.read_excel(input_file, sheet_name="Attendance")
leave = pd.read_excel(input_file, sheet_name="Leave")
overtime = pd.read_excel(input_file, sheet_name="Overtime")
productivity = pd.read_excel(input_file, sheet_name="Productivity")
performance = pd.read_excel(input_file, sheet_name="Performance")
hiring = pd.read_excel(input_file, sheet_name="Hiring")
attrition = pd.read_excel(input_file, sheet_name="Attrition")


print("\n==============================")
print("DATA LOADED SUCCESSFULLY")
print("==============================")


# =========================================================
# 3. STANDARDIZE COLUMN NAMES
# =========================================================

datasets = {
    "Employee_Master": employee,
    "Attendance": attendance,
    "Leave": leave,
    "Overtime": overtime,
    "Productivity": productivity,
    "Performance": performance,
    "Hiring": hiring,
    "Attrition": attrition
}

for name, df in datasets.items():

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
    )


# =========================================================
# 4. REMOVE COMPLETELY EMPTY ROWS
# =========================================================

for name in datasets:

    datasets[name] = datasets[name].dropna(how="all")


employee = datasets["Employee_Master"]
attendance = datasets["Attendance"]
leave = datasets["Leave"]
overtime = datasets["Overtime"]
productivity = datasets["Productivity"]
performance = datasets["Performance"]
hiring = datasets["Hiring"]
attrition = datasets["Attrition"]


# =========================================================
# 5. REMOVE EXTRA SPACES FROM TEXT COLUMNS
# =========================================================

for df in [
    employee,
    attendance,
    leave,
    overtime,
    productivity,
    performance,
    hiring,
    attrition
]:

    text_columns = df.select_dtypes(include="object").columns

    for col in text_columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .replace("nan", np.nan)
        )


# =========================================================
# 6. EMPLOYEE MASTER CLEANING
# =========================================================

print("\nCleaning Employee Master...")


# Employee ID standardization

employee["Employee_ID"] = (
    employee["Employee_ID"]
    .astype(str)
    .str.strip()
    .str.upper()
)


# Remove duplicate Employee IDs

employee_duplicates = employee[
    employee["Employee_ID"].duplicated(keep=False)
].copy()

employee = employee.drop_duplicates(
    subset="Employee_ID",
    keep="first"
)


# Convert dates

employee["Date_of_Joining"] = pd.to_datetime(
    employee["Date_of_Joining"],
    errors="coerce"
)

employee["Exit_Date"] = pd.to_datetime(
    employee["Exit_Date"],
    errors="coerce"
)


# Fix status based on exit date

employee["Status"] = np.where(
    employee["Exit_Date"].isna(),
    "Active",
    "Exited"
)


# Invalid exit date

invalid_exit_dates = employee[
    employee["Exit_Date"].notna()
    &
    (
        employee["Exit_Date"]
        <
        employee["Date_of_Joining"]
    )
].copy()


# Experience calculation

reference_date = pd.Timestamp("2026-08-31")

employee["Experience_Years"] = (
    (
        reference_date
        -
        employee["Date_of_Joining"]
    ).dt.days
    / 365.25
).round(1)


employee["Experience_Years"] = employee[
    "Experience_Years"
].clip(lower=0)


# Numeric cleanup

employee["Age"] = pd.to_numeric(
    employee["Age"],
    errors="coerce"
)

employee["Monthly_Salary"] = pd.to_numeric(
    employee["Monthly_Salary"],
    errors="coerce"
)


# Invalid ages

invalid_age = employee[
    (employee["Age"] < 18)
    |
    (employee["Age"] > 65)
].copy()


# Invalid salaries

invalid_salary = employee[
    employee["Monthly_Salary"] < 0
].copy()


# =========================================================
# 7. ATTENDANCE CLEANING
# =========================================================

print("Cleaning Attendance...")


attendance["Employee_ID"] = (
    attendance["Employee_ID"]
    .astype(str)
    .str.strip()
    .str.upper()
)


attendance["Work_Date"] = pd.to_datetime(
    attendance["Work_Date"],
    errors="coerce"
)


attendance["Scheduled_Hours"] = pd.to_numeric(
    attendance["Scheduled_Hours"],
    errors="coerce"
)


attendance["Actual_Hours"] = pd.to_numeric(
    attendance["Actual_Hours"],
    errors="coerce"
)


attendance["Present_Flag"] = pd.to_numeric(
    attendance["Present_Flag"],
    errors="coerce"
)


# Remove exact duplicate transactions

attendance_duplicates = attendance[
    attendance.duplicated(
        subset=["Employee_ID", "Work_Date"],
        keep=False
    )
].copy()


attendance = attendance.drop_duplicates(
    subset=["Employee_ID", "Work_Date"],
    keep="first"
)


# Invalid hours

invalid_attendance_hours = attendance[
    (attendance["Scheduled_Hours"] < 0)
    |
    (attendance["Actual_Hours"] < 0)
].copy()


# =========================================================
# 8. LEAVE CLEANING
# =========================================================

print("Cleaning Leave...")


leave["Employee_ID"] = (
    leave["Employee_ID"]
    .astype(str)
    .str.strip()
    .str.upper()
)


leave["Leave_Start"] = pd.to_datetime(
    leave["Leave_Start"],
    errors="coerce"
)

leave["Leave_End"] = pd.to_datetime(
    leave["Leave_End"],
    errors="coerce"
)

leave["Leave_Days"] = pd.to_numeric(
    leave["Leave_Days"],
    errors="coerce"
)


leave_duplicates = leave[
    leave["Leave_ID"].duplicated(keep=False)
].copy()


leave = leave.drop_duplicates(
    subset="Leave_ID",
    keep="first"
)


invalid_leave_dates = leave[
    leave["Leave_End"]
    <
    leave["Leave_Start"]
].copy()


invalid_leave_days = leave[
    leave["Leave_Days"] <= 0
].copy()


# =========================================================
# 9. OVERTIME CLEANING
# =========================================================

print("Cleaning Overtime...")


overtime["Employee_ID"] = (
    overtime["Employee_ID"]
    .astype(str)
    .str.strip()
    .str.upper()
)


overtime["OT_Date"] = pd.to_datetime(
    overtime["OT_Date"],
    errors="coerce"
)


overtime["OT_Hours"] = pd.to_numeric(
    overtime["OT_Hours"],
    errors="coerce"
)


overtime_duplicates = overtime[
    overtime["OT_ID"].duplicated(keep=False)
].copy()


overtime = overtime.drop_duplicates(
    subset="OT_ID",
    keep="first"
)


invalid_ot = overtime[
    overtime["OT_Hours"] < 0
].copy()


# =========================================================
# 10. PRODUCTIVITY CLEANING
# =========================================================

print("Cleaning Productivity...")


productivity["Employee_ID"] = (
    productivity["Employee_ID"]
    .astype(str)
    .str.strip()
    .str.upper()
)


productivity["Month"] = pd.to_datetime(
    productivity["Month"],
    errors="coerce"
)


numeric_productivity_columns = [
    "Experience_Years",
    "Workload_Units",
    "Completed_Units",
    "Productive_Hours",
    "Available_Hours",
    "Capacity_Utilization",
    "Quality_Score",
    "Revenue_Contribution"
]


for col in numeric_productivity_columns:

    productivity[col] = pd.to_numeric(
        productivity[col],
        errors="coerce"
    )


productivity_duplicates = productivity[
    productivity.duplicated(
        subset=["Employee_ID", "Month"],
        keep=False
    )
].copy()


productivity = productivity.drop_duplicates(
    subset=["Employee_ID", "Month"],
    keep="first"
)


invalid_productivity = productivity[
    (productivity["Workload_Units"] < 0)
    |
    (productivity["Completed_Units"] < 0)
    |
    (productivity["Productive_Hours"] < 0)
    |
    (productivity["Available_Hours"] <= 0)
    |
    (productivity["Revenue_Contribution"] < 0)
].copy()


# Recalculate Capacity Utilization

productivity["Capacity_Utilization"] = (
    productivity["Productive_Hours"]
    /
    productivity["Available_Hours"]
)


# Productivity %

productivity["Productivity_Percentage"] = np.where(

    productivity["Workload_Units"] > 0,

    (
        productivity["Completed_Units"]
        /
        productivity["Workload_Units"]
    )
    * 100,

    np.nan
)


# =========================================================
# 11. PERFORMANCE CLEANING
# =========================================================

print("Cleaning Performance...")


performance["Employee_ID"] = (
    performance["Employee_ID"]
    .astype(str)
    .str.strip()
    .str.upper()
)


performance["Period_End"] = pd.to_datetime(
    performance["Period_End"],
    unit="D",
    origin="1899-12-30",
    errors="coerce"
)

performance["Performance_Rating"] = pd.to_numeric(
    performance["Performance_Rating"],
    errors="coerce"
)


performance_duplicates = performance[
    performance.duplicated(
        subset=["Employee_ID", "Period"],
        keep=False
    )
].copy()


performance = performance.drop_duplicates(
    subset=["Employee_ID", "Period"],
    keep="first"
)


invalid_rating = performance[
    (performance["Performance_Rating"] < 1)
    |
    (performance["Performance_Rating"] > 5)
].copy()


# =========================================================
# 12. HIRING CLEANING
# =========================================================

print("Cleaning Hiring...")


hiring["Month"] = pd.to_datetime(
    hiring["Month"],
    errors="coerce"
)


hiring_numeric_columns = [
    "Open_Positions",
    "Hires_Completed",
    "Open_Gap",
    "Avg_Time_to_Hire_Days",
    "Offer_Acceptance_Rate"
]


for col in hiring_numeric_columns:

    hiring[col] = pd.to_numeric(
        hiring[col],
        errors="coerce"
    )


hiring_duplicates = hiring[
    hiring.duplicated(
        subset=["Month", "Department"],
        keep=False
    )
].copy()


hiring = hiring.drop_duplicates(
    subset=["Month", "Department"],
    keep="first"
)


# Recalculate Open Gap

hiring["Open_Gap"] = (
    hiring["Open_Positions"]
    -
    hiring["Hires_Completed"]
)


invalid_hiring = hiring[
    (hiring["Open_Positions"] < 0)
    |
    (hiring["Hires_Completed"] < 0)
].copy()


# =========================================================
# 13. ATTRITION CLEANING
# =========================================================

print("Cleaning Attrition...")


attrition["Employee_ID"] = (
    attrition["Employee_ID"]
    .astype(str)
    .str.strip()
    .str.upper()
)


attrition["Exit_Date"] = pd.to_datetime(
    attrition["Exit_Date"],
    errors="coerce"
)


attrition["Tenure_Years"] = pd.to_numeric(
    attrition["Tenure_Years"],
    errors="coerce"
)


attrition_duplicates = attrition[
    attrition["Employee_ID"].duplicated(
        keep=False
    )
].copy()


attrition = attrition.drop_duplicates(
    subset="Employee_ID",
    keep="first"
)


# =========================================================
# 14. CROSS-DATASET RECONCILIATION
# =========================================================

print("\nRunning reconciliation checks...")


valid_employee_ids = set(
    employee["Employee_ID"]
)


def unmatched_employee_ids(df):

    return df[
        ~df["Employee_ID"].isin(valid_employee_ids)
    ].copy()


unmatched_attendance = unmatched_employee_ids(attendance)

unmatched_leave = unmatched_employee_ids(leave)

unmatched_overtime = unmatched_employee_ids(overtime)

unmatched_productivity = unmatched_employee_ids(productivity)

unmatched_performance = unmatched_employee_ids(performance)

unmatched_attrition = unmatched_employee_ids(attrition)


# =========================================================
# 15. EMPLOYMENT PERIOD VALIDATION
# =========================================================

employee_dates = employee[
    [
        "Employee_ID",
        "Date_of_Joining",
        "Exit_Date"
    ]
]


# Attendance

attendance_check = attendance.merge(
    employee_dates,
    on="Employee_ID",
    how="left"
)


attendance_outside_employment = attendance_check[

    (
        attendance_check["Work_Date"]
        <
        attendance_check["Date_of_Joining"]
    )

    |

    (
        attendance_check["Exit_Date"].notna()
        &
        (
            attendance_check["Work_Date"]
            >
            attendance_check["Exit_Date"]
        )
    )

].copy()


# Overtime

overtime_check = overtime.merge(
    employee_dates,
    on="Employee_ID",
    how="left"
)


overtime_outside_employment = overtime_check[

    (
        overtime_check["OT_Date"]
        <
        overtime_check["Date_of_Joining"]
    )

    |

    (
        overtime_check["Exit_Date"].notna()
        &
        (
            overtime_check["OT_Date"]
            >
            overtime_check["Exit_Date"]
        )
    )

].copy()


# Productivity

productivity_check = productivity.merge(
    employee_dates,
    on="Employee_ID",
    how="left"
)


productivity_outside_employment = productivity_check[

    (
        productivity_check["Month"]
        <
        productivity_check[
            "Date_of_Joining"
        ].dt.to_period("M").dt.to_timestamp()
    )

    |

    (
        productivity_check["Exit_Date"].notna()
        &
        (
            productivity_check["Month"]
            >
            productivity_check[
                "Exit_Date"
            ].dt.to_period("M").dt.to_timestamp()
        )
    )

].copy()


# =========================================================
# 16. ATTRITION VS EMPLOYEE MASTER RECONCILIATION
# =========================================================

master_exits = employee[
    employee["Status"] == "Exited"
][
    [
        "Employee_ID",
        "Exit_Date"
    ]
].copy()


attrition_compare = master_exits.merge(

    attrition[
        [
            "Employee_ID",
            "Exit_Date"
        ]
    ],

    on="Employee_ID",

    how="outer",

    suffixes=(
        "_Master",
        "_Attrition"
    ),

    indicator=True

)


attrition_mismatch = attrition_compare[

    (
        attrition_compare["_merge"]
        !=
        "both"
    )

    |

    (
        attrition_compare[
            "Exit_Date_Master"
        ]
        !=
        attrition_compare[
            "Exit_Date_Attrition"
        ]
    )

].copy()


# =========================================================
# 17. MISSING VALUE SUMMARY
# =========================================================

missing_summary_list = []


for dataset_name, df in {

    "Employee_Master": employee,

    "Attendance": attendance,

    "Leave": leave,

    "Overtime": overtime,

    "Productivity": productivity,

    "Performance": performance,

    "Hiring": hiring,

    "Attrition": attrition

}.items():

    for column in df.columns:

        missing_count = df[column].isna().sum()

        missing_summary_list.append({

            "Dataset": dataset_name,

            "Column": column,

            "Missing_Count": missing_count,

            "Total_Rows": len(df),

            "Missing_Percentage":
                round(
                    missing_count
                    /
                    len(df)
                    *
                    100,
                    2
                )
                if len(df) > 0
                else 0

        })


missing_summary = pd.DataFrame(
    missing_summary_list
)


# =========================================================
# 18. CLEANING / RECONCILIATION SUMMARY
# =========================================================

reconciliation_report = pd.DataFrame({

    "Check": [

        "Duplicate Employee IDs",

        "Invalid Exit Dates",

        "Invalid Employee Ages",

        "Invalid Salaries",

        "Duplicate Attendance",

        "Invalid Attendance Hours",

        "Duplicate Leave Records",

        "Invalid Leave Dates",

        "Invalid Leave Days",

        "Duplicate Overtime",

        "Invalid Overtime Hours",

        "Duplicate Productivity",

        "Invalid Productivity Values",

        "Duplicate Performance",

        "Invalid Performance Ratings",

        "Duplicate Hiring Records",

        "Invalid Hiring Values",

        "Duplicate Attrition Employees",

        "Unmatched Attendance Employee IDs",

        "Unmatched Leave Employee IDs",

        "Unmatched Overtime Employee IDs",

        "Unmatched Productivity Employee IDs",

        "Unmatched Performance Employee IDs",

        "Unmatched Attrition Employee IDs",

        "Attendance Outside Employment",

        "Overtime Outside Employment",

        "Productivity Outside Employment",

        "Attrition vs Employee Master Mismatch"

    ],

    "Issue_Count": [

        len(employee_duplicates),

        len(invalid_exit_dates),

        len(invalid_age),

        len(invalid_salary),

        len(attendance_duplicates),

        len(invalid_attendance_hours),

        len(leave_duplicates),

        len(invalid_leave_dates),

        len(invalid_leave_days),

        len(overtime_duplicates),

        len(invalid_ot),

        len(productivity_duplicates),

        len(invalid_productivity),

        len(performance_duplicates),

        len(invalid_rating),

        len(hiring_duplicates),

        len(invalid_hiring),

        len(attrition_duplicates),

        len(unmatched_attendance),

        len(unmatched_leave),

        len(unmatched_overtime),

        len(unmatched_productivity),

        len(unmatched_performance),

        len(unmatched_attrition),

        len(attendance_outside_employment),

        len(overtime_outside_employment),

        len(productivity_outside_employment),

        len(attrition_mismatch)

    ]

})


reconciliation_report["Status"] = np.where(

    reconciliation_report[
        "Issue_Count"
    ] == 0,

    "PASS",

    "REVIEW"

)


# =========================================================
# 19. CREATE EXCEPTION REPORT
# =========================================================

exceptions = []


def add_exception(
    df,
    dataset,
    issue
):

    if not df.empty:

        temp = df.copy()

        temp["Dataset"] = dataset

        temp["Issue"] = issue

        exceptions.append(
            temp
        )


add_exception(
    invalid_exit_dates,
    "Employee_Master",
    "Exit date before joining date"
)

add_exception(
    invalid_age,
    "Employee_Master",
    "Invalid employee age"
)

add_exception(
    invalid_salary,
    "Employee_Master",
    "Negative salary"
)

add_exception(
    unmatched_attendance,
    "Attendance",
    "Employee ID not found in Employee Master"
)

add_exception(
    unmatched_leave,
    "Leave",
    "Employee ID not found in Employee Master"
)

add_exception(
    unmatched_overtime,
    "Overtime",
    "Employee ID not found in Employee Master"
)

add_exception(
    unmatched_productivity,
    "Productivity",
    "Employee ID not found in Employee Master"
)

add_exception(
    invalid_ot,
    "Overtime",
    "Invalid overtime hours"
)

add_exception(
    invalid_productivity,
    "Productivity",
    "Invalid productivity values"
)


if exceptions:

    exception_report = pd.concat(
        exceptions,
        ignore_index=True
    )

else:

    exception_report = pd.DataFrame({
        "Message": [
            "No critical data-quality exceptions found"
        ]
    })


# =========================================================
# 20. SORT DATA
# =========================================================

employee = employee.sort_values(
    "Employee_ID"
)

attendance = attendance.sort_values(
    ["Work_Date", "Employee_ID"]
)

leave = leave.sort_values(
    ["Leave_Start", "Employee_ID"]
)

overtime = overtime.sort_values(
    ["OT_Date", "Employee_ID"]
)

productivity = productivity.sort_values(
    ["Month", "Employee_ID"]
)

performance = performance.sort_values(
    ["Period_End", "Employee_ID"]
)

hiring = hiring.sort_values(
    ["Month", "Department"]
)

attrition = attrition.sort_values(
    "Exit_Date"
)


# =========================================================
# 21. EXPORT CLEANED DATA
# =========================================================

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    employee.to_excel(
        writer,
        sheet_name="Employee_Master",
        index=False
    )

    attendance.to_excel(
        writer,
        sheet_name="Attendance",
        index=False
    )

    leave.to_excel(
        writer,
        sheet_name="Leave",
        index=False
    )

    overtime.to_excel(
        writer,
        sheet_name="Overtime",
        index=False
    )

    productivity.to_excel(
        writer,
        sheet_name="Productivity",
        index=False
    )

    performance.to_excel(
        writer,
        sheet_name="Performance",
        index=False
    )

    hiring.to_excel(
        writer,
        sheet_name="Hiring",
        index=False
    )

    attrition.to_excel(
        writer,
        sheet_name="Attrition",
        index=False
    )

    reconciliation_report.to_excel(
        writer,
        sheet_name="Reconciliation_Report",
        index=False
    )

    missing_summary.to_excel(
        writer,
        sheet_name="Missing_Value_Summary",
        index=False
    )

    exception_report.to_excel(
        writer,
        sheet_name="Exception_Report",
        index=False
    )


# =========================================================
# 22. FINAL OUTPUT
# =========================================================

print("\n================================")
print("DATA CLEANING COMPLETED")
print("================================")


print("\nEmployee Master Rows:",
      len(employee))

print("Attendance Rows:",
      len(attendance))

print("Leave Rows:",
      len(leave))

print("Overtime Rows:",
      len(overtime))

print("Productivity Rows:",
      len(productivity))

print("Performance Rows:",
      len(performance))

print("Hiring Rows:",
      len(hiring))

print("Attrition Rows:",
      len(attrition))


print("\nReconciliation Results:")

print(
    reconciliation_report
)


print(
    "\nCleaned file saved as:",
    output_file
)