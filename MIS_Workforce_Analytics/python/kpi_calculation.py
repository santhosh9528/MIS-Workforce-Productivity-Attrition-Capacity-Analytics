import pandas as pd
import numpy as np
import os

# =========================================================
# 1. FILE PATHS
# =========================================================

input_file = r"C:\Users\Hooooo\Documents\Excel\MIS_Workforce_Analytics\Cleaned\MIS_Workforce_Cleaned.xlsx"

output_folder = r"C:\Users\Hooooo\Documents\Excel\MIS_Workforce_Analytics\Analysis"

os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(
    output_folder,
    "MIS_Workforce_KPI_Calculations.xlsx"
)


# =========================================================
# 2. LOAD CLEANED DATA
# =========================================================

employee = pd.read_excel(
    input_file,
    sheet_name="Employee_Master"
)

attendance = pd.read_excel(
    input_file,
    sheet_name="Attendance"
)

leave = pd.read_excel(
    input_file,
    sheet_name="Leave"
)

overtime = pd.read_excel(
    input_file,
    sheet_name="Overtime"
)

productivity = pd.read_excel(
    input_file,
    sheet_name="Productivity"
)

performance = pd.read_excel(
    input_file,
    sheet_name="Performance"
)

hiring = pd.read_excel(
    input_file,
    sheet_name="Hiring"
)

attrition = pd.read_excel(
    input_file,
    sheet_name="Attrition"
)

print("All cleaned datasets loaded successfully")


# =========================================================
# 3. DATE CONVERSION
# =========================================================

employee["Date_of_Joining"] = pd.to_datetime(
    employee["Date_of_Joining"],
    errors="coerce"
)

employee["Exit_Date"] = pd.to_datetime(
    employee["Exit_Date"],
    errors="coerce"
)

attendance["Work_Date"] = pd.to_datetime(
    attendance["Work_Date"],
    errors="coerce"
)

leave["Leave_Start"] = pd.to_datetime(
    leave["Leave_Start"],
    errors="coerce"
)

leave["Leave_End"] = pd.to_datetime(
    leave["Leave_End"],
    errors="coerce"
)

overtime["OT_Date"] = pd.to_datetime(
    overtime["OT_Date"],
    errors="coerce"
)

productivity["Month"] = pd.to_datetime(
    productivity["Month"],
    errors="coerce"
)

performance["Period_End"] = pd.to_datetime(
    performance["Period_End"],
    errors="coerce"
)

hiring["Month"] = pd.to_datetime(
    hiring["Month"],
    errors="coerce"
)

attrition["Exit_Date"] = pd.to_datetime(
    attrition["Exit_Date"],
    errors="coerce"
)


# =========================================================
# 4. ANALYSIS PERIOD
# =========================================================

analysis_start = pd.Timestamp("2026-01-01")
analysis_end = pd.Timestamp("2026-08-31")


# =========================================================
# 5. OVERALL HEADCOUNT KPIs
# =========================================================

# Employees who joined on or before analysis end
headcount = employee[
    employee["Date_of_Joining"] <= analysis_end
]["Employee_ID"].nunique()


# Active employees as of Aug 31, 2026
active_employees = employee[
    (employee["Date_of_Joining"] <= analysis_end)
    &
    (
        employee["Exit_Date"].isna()
        |
        (employee["Exit_Date"] > analysis_end)
    )
]["Employee_ID"].nunique()


# New joiners during analysis period
new_joiners = employee[
    employee["Date_of_Joining"].between(
        analysis_start,
        analysis_end
    )
]["Employee_ID"].nunique()


# Exits during analysis period
exits = employee[
    employee["Exit_Date"].between(
        analysis_start,
        analysis_end
    )
]["Employee_ID"].nunique()


# =========================================================
# 6. ATTRITION %
# =========================================================

opening_headcount = employee[
    (employee["Date_of_Joining"] < analysis_start)
    &
    (
        employee["Exit_Date"].isna()
        |
        (employee["Exit_Date"] >= analysis_start)
    )
]["Employee_ID"].nunique()


closing_headcount = active_employees

average_headcount = (
    opening_headcount
    +
    closing_headcount
) / 2


attrition_percentage = (
    exits / average_headcount * 100
    if average_headcount > 0
    else 0
)


# =========================================================
# 7. ABSENTEEISM %
# =========================================================

scheduled_days = len(attendance)

absent_days = len(
    attendance[
        attendance["Present_Flag"] == 0
    ]
)


absenteeism_percentage = (
    absent_days
    /
    scheduled_days
    *
    100
    if scheduled_days > 0
    else 0
)


# Hours-based absenteeism
scheduled_hours = attendance[
    "Scheduled_Hours"
].sum()

actual_hours = attendance[
    "Actual_Hours"
].sum()

attendance["Lost_Hours"] = (
    attendance["Scheduled_Hours"]
    - attendance["Actual_Hours"]
).clip(lower=0)

absent_hours = attendance["Lost_Hours"].sum()

hour_based_absenteeism = (
    absent_hours
    /
    scheduled_hours
    *
    100
    if scheduled_hours > 0
    else 0
)


# =========================================================
# 8. LEAVE UTILIZATION %
# =========================================================

approved_leave = leave[
    leave["Approval_Status"].str.lower()
    ==
    "approved"
].copy()


total_leave_days = approved_leave[
    "Leave_Days"
].sum()


# Assumption:
# 18 leave days entitlement per employee per year.
# Jan-Aug = 8/12 of annual entitlement.

annual_leave_entitlement = 18

period_leave_entitlement = (
    annual_leave_entitlement
    *
    8
    /
    12
)


available_leave_days = (
    headcount
    *
    period_leave_entitlement
)


leave_utilization_percentage = (
    total_leave_days
    /
    available_leave_days
    *
    100
    if available_leave_days > 0
    else 0
)


# =========================================================
# 9. OVERTIME KPI
# =========================================================

total_overtime_hours = overtime[
    "OT_Hours"
].sum()


average_ot_per_employee = (
    total_overtime_hours
    /
    active_employees
    if active_employees > 0
    else 0
)


# =========================================================
# 10. PRODUCTIVITY KPIs
# =========================================================

total_workload = productivity[
    "Workload_Units"
].sum()

total_completed = productivity[
    "Completed_Units"
].sum()


overall_productivity_percentage = (
    total_completed
    /
    total_workload
    *
    100
    if total_workload > 0
    else 0
)


# Productivity per employee
productivity_per_employee = (
    total_completed
    /
    productivity["Employee_ID"].nunique()
    if productivity["Employee_ID"].nunique() > 0
    else 0
)


# =========================================================
# 11. REVENUE CONTRIBUTION KPI
# =========================================================

total_revenue_contribution = productivity[
    "Revenue_Contribution"
].sum()


revenue_per_employee = (
    total_revenue_contribution
    /
    productivity["Employee_ID"].nunique()
    if productivity["Employee_ID"].nunique() > 0
    else 0
)


# =========================================================
# 12. CAPACITY UTILIZATION
# =========================================================

total_productive_hours = productivity[
    "Productive_Hours"
].sum()

total_available_hours = productivity[
    "Available_Hours"
].sum()


capacity_utilization = (
    total_productive_hours
    /
    total_available_hours
    *
    100
    if total_available_hours > 0
    else 0
)


# =========================================================
# 13. QUALITY SCORE
# =========================================================

average_quality_score = productivity[
    "Quality_Score"
].mean()


# =========================================================
# 14. OVERALL KPI SUMMARY
# =========================================================

overall_kpi = pd.DataFrame({

    "KPI": [
        "Employee Headcount",
        "Active Employees",
        "Opening Headcount",
        "New Joiners",
        "Exits",
        "Average Headcount",
        "Attrition %",
        "Absenteeism %",
	"Scheduled Hour Shortfall %",
        "Leave Utilization %",
        "Overtime Hours",
        "Average OT per Employee",
        "Total Workload Units",
        "Completed Units",
        "Productivity %",
        "Productivity per Employee",
        "Revenue Contribution",
        "Revenue Contribution per Employee",
        "Capacity Utilization %",
        "Average Quality Score"
    ],

    "Value": [
        headcount,
        active_employees,
        opening_headcount,
        new_joiners,
        exits,
        round(average_headcount, 2),
        round(attrition_percentage, 2),
        round(absenteeism_percentage, 2),
        round(hour_based_absenteeism, 2),
        round(leave_utilization_percentage, 2),
        round(total_overtime_hours, 2),
        round(average_ot_per_employee, 2),
        round(total_workload, 2),
        round(total_completed, 2),
        round(overall_productivity_percentage, 2),
        round(productivity_per_employee, 2),
        round(total_revenue_contribution, 2),
        round(revenue_per_employee, 2),
        round(capacity_utilization, 2),
        round(average_quality_score, 2)
    ]
})


# =========================================================
# 15. MONTH COLUMN CREATION
# =========================================================

attendance["Month"] = (
    attendance["Work_Date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

leave["Month"] = (
    leave["Leave_Start"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

overtime["Month"] = (
    overtime["OT_Date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

employee["Join_Month"] = (
    employee["Date_of_Joining"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

employee["Exit_Month"] = (
    employee["Exit_Date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)


# =========================================================
# 16. MONTHLY HEADCOUNT
# =========================================================

months = pd.date_range(
    analysis_start,
    analysis_end,
    freq="MS"
)

monthly_rows = []


for month in months:

    month_end = month + pd.offsets.MonthEnd(0)

    monthly_headcount = employee[
        (employee["Date_of_Joining"] <= month_end)
        &
        (
            employee["Exit_Date"].isna()
            |
            (employee["Exit_Date"] > month_end)
        )
    ]["Employee_ID"].nunique()


    monthly_joiners = employee[
        employee["Join_Month"] == month
    ]["Employee_ID"].nunique()


    monthly_exits = employee[
        employee["Exit_Month"] == month
    ]["Employee_ID"].nunique()


    month_attendance = attendance[
        attendance["Month"] == month
    ]


    scheduled = len(month_attendance)

    absent = len(
        month_attendance[
            month_attendance["Present_Flag"] == 0
        ]
    )


    monthly_absenteeism = (
        absent / scheduled * 100
        if scheduled > 0
        else 0
    )


    month_ot = overtime[
        overtime["Month"] == month
    ]["OT_Hours"].sum()


    month_productivity = productivity[
        productivity["Month"] == month
    ]


    workload = month_productivity[
        "Workload_Units"
    ].sum()

    completed = month_productivity[
        "Completed_Units"
    ].sum()


    productivity_pct = (
        completed
        /
        workload
        *
        100
        if workload > 0
        else 0
    )


    productive_hours = month_productivity[
        "Productive_Hours"
    ].sum()

    available_hours = month_productivity[
        "Available_Hours"
    ].sum()


    monthly_capacity = (
        productive_hours
        /
        available_hours
        *
        100
        if available_hours > 0
        else 0
    )


    revenue = month_productivity[
        "Revenue_Contribution"
    ].sum()


    monthly_rows.append({

        "Month": month,

        "Headcount": monthly_headcount,

        "New_Joiners": monthly_joiners,

        "Exits": monthly_exits,

        "Absenteeism_Percentage":
            round(monthly_absenteeism, 2),

        "Overtime_Hours":
            round(month_ot, 2),

        "Workload_Units":
            workload,

        "Completed_Units":
            completed,

        "Productivity_Percentage":
            round(productivity_pct, 2),

        "Capacity_Utilization_Percentage":
            round(monthly_capacity, 2),

        "Revenue_Contribution":
            round(revenue, 2)

    })


monthly_kpi = pd.DataFrame(
    monthly_rows
)


# =========================================================
# 17. MONTHLY ATTRITION %
# =========================================================

monthly_kpi["Previous_Headcount"] = (
    monthly_kpi["Headcount"]
    .shift(1)
)


monthly_kpi.loc[
    monthly_kpi.index[0],
    "Previous_Headcount"
] = opening_headcount


monthly_kpi["Average_Headcount"] = (

    monthly_kpi["Previous_Headcount"]
    +
    monthly_kpi["Headcount"]

) / 2


monthly_kpi["Attrition_Percentage"] = np.where(

    monthly_kpi["Average_Headcount"] > 0,

    (
        monthly_kpi["Exits"]
        /
        monthly_kpi["Average_Headcount"]
    )
    *
    100,

    0
)


monthly_kpi["Attrition_Percentage"] = (
    monthly_kpi[
        "Attrition_Percentage"
    ]
    .round(2)
)


# =========================================================
# 18. DEPARTMENT PRODUCTIVITY
# =========================================================

department_productivity = (

    productivity
    .groupby(
        "Department",
        as_index=False
    )
    .agg(

        Employees=(
            "Employee_ID",
            "nunique"
        ),

        Workload_Units=(
            "Workload_Units",
            "sum"
        ),

        Completed_Units=(
            "Completed_Units",
            "sum"
        ),

        Productive_Hours=(
            "Productive_Hours",
            "sum"
        ),

        Available_Hours=(
            "Available_Hours",
            "sum"
        ),

        Revenue_Contribution=(
            "Revenue_Contribution",
            "sum"
        ),

        Average_Quality_Score=(
            "Quality_Score",
            "mean"
        )

    )

)


department_productivity[
    "Productivity_Percentage"
] = (

    department_productivity[
        "Completed_Units"
    ]

    /

    department_productivity[
        "Workload_Units"
    ]

    *
    100

)


department_productivity[
    "Capacity_Utilization_Percentage"
] = (

    department_productivity[
        "Productive_Hours"
    ]

    /

    department_productivity[
        "Available_Hours"
    ]

    *
    100

)


department_productivity[
    "Productivity_Per_Employee"
] = (

    department_productivity[
        "Completed_Units"
    ]

    /

    department_productivity[
        "Employees"
    ]

)


department_productivity[
    "Revenue_Per_Employee"
] = (

    department_productivity[
        "Revenue_Contribution"
    ]

    /

    department_productivity[
        "Employees"
    ]

)


# =========================================================
# 19. DEPARTMENT OVERTIME
# =========================================================

department_ot = (

    overtime
    .groupby(
        "Department",
        as_index=False
    )
    ["OT_Hours"]
    .sum()

    .rename(
        columns={
            "OT_Hours":
            "Overtime_Hours"
        }
    )

)


department_productivity = (
    department_productivity
    .merge(
        department_ot,
        on="Department",
        how="left"
    )
)


department_productivity[
    "Overtime_Hours"
] = (
    department_productivity[
        "Overtime_Hours"
    ]
    .fillna(0)
)


# =========================================================
# 20. DEPARTMENT ABSENTEEISM
# =========================================================

department_attendance = (

    attendance
    .groupby(
        "Department",
        as_index=False
    )
    .agg(

        Scheduled_Days=(
            "Present_Flag",
            "count"
        ),

        Present_Days=(
            "Present_Flag",
            "sum"
        )

    )

)


department_attendance[
    "Absent_Days"
] = (

    department_attendance[
        "Scheduled_Days"
    ]

    -

    department_attendance[
        "Present_Days"
    ]

)


department_attendance[
    "Absenteeism_Percentage"
] = (

    department_attendance[
        "Absent_Days"
    ]

    /

    department_attendance[
        "Scheduled_Days"
    ]

    *
    100

)


department_productivity = (
    department_productivity
    .merge(

        department_attendance[
            [
                "Department",
                "Absenteeism_Percentage"
            ]
        ],

        on="Department",

        how="left"

    )
)


# =========================================================
# 21. DEPARTMENT ATTRITION
# =========================================================

department_exits = (

    attrition
    .groupby(
        "Department",
        as_index=False
    )
    .agg(

        Exits=(
            "Employee_ID",
            "nunique"
        )

    )

)


department_productivity = (
    department_productivity
    .merge(

        department_exits,

        on="Department",

        how="left"

    )
)


department_productivity[
    "Exits"
] = (
    department_productivity[
        "Exits"
    ]
    .fillna(0)
)


# =========================================================
# 22. LOCATION PRODUCTIVITY
# =========================================================

location_productivity = (

    productivity
    .groupby(
        "Location",
        as_index=False
    )
    .agg(

        Employees=(
            "Employee_ID",
            "nunique"
        ),

        Workload_Units=(
            "Workload_Units",
            "sum"
        ),

        Completed_Units=(
            "Completed_Units",
            "sum"
        ),

        Revenue_Contribution=(
            "Revenue_Contribution",
            "sum"
        )

    )

)


location_productivity[
    "Productivity_Percentage"
] = (

    location_productivity[
        "Completed_Units"
    ]

    /

    location_productivity[
        "Workload_Units"
    ]

    *
    100

)


# =========================================================
# 23. DESIGNATION PRODUCTIVITY
# =========================================================

designation_productivity = (

    productivity
    .groupby(
        "Designation",
        as_index=False
    )
    .agg(

        Employees=(
            "Employee_ID",
            "nunique"
        ),

        Workload_Units=(
            "Workload_Units",
            "sum"
        ),

        Completed_Units=(
            "Completed_Units",
            "sum"
        ),

        Revenue_Contribution=(
            "Revenue_Contribution",
            "sum"
        )

    )

)


designation_productivity[
    "Productivity_Percentage"
] = (

    designation_productivity[
        "Completed_Units"
    ]

    /

    designation_productivity[
        "Workload_Units"
    ]

    *
    100

)


# =========================================================
# 24. MANAGER PRODUCTIVITY
# =========================================================

manager_productivity = (

    productivity
    .groupby(
        [
            "Department",
            "Manager"
        ],
        as_index=False
    )
    .agg(

        Employees=(
            "Employee_ID",
            "nunique"
        ),

        Workload_Units=(
            "Workload_Units",
            "sum"
        ),

        Completed_Units=(
            "Completed_Units",
            "sum"
        ),

        Revenue_Contribution=(
            "Revenue_Contribution",
            "sum"
        )

    )

)


manager_productivity[
    "Productivity_Percentage"
] = (

    manager_productivity[
        "Completed_Units"
    ]

    /

    manager_productivity[
        "Workload_Units"
    ]

    *
    100

)


# =========================================================
# 25. EXPERIENCE GROUP
# =========================================================

productivity[
    "Experience_Group"
] = pd.cut(

    productivity[
        "Experience_Years"
    ],

    bins=[
        -1,
        1,
        3,
        5,
        100
    ],

    labels=[
        "0-1 Years",
        "1-3 Years",
        "3-5 Years",
        "5+ Years"
    ]

)


experience_productivity = (

    productivity
    .groupby(
        "Experience_Group",
        observed=True,
        as_index=False
    )
    .agg(

        Employees=(
            "Employee_ID",
            "nunique"
        ),

        Workload_Units=(
            "Workload_Units",
            "sum"
        ),

        Completed_Units=(
            "Completed_Units",
            "sum"
        ),

        Revenue_Contribution=(
            "Revenue_Contribution",
            "sum"
        )

    )

)


experience_productivity[
    "Productivity_Percentage"
] = (

    experience_productivity[
        "Completed_Units"
    ]

    /

    experience_productivity[
        "Workload_Units"
    ]

    *
    100

)


# =========================================================
# 26. NEW JOINER VS EXPERIENCED
# =========================================================

productivity["Employee_Category"] = np.where(

    productivity[
        "Experience_Years"
    ] < 1,

    "New Joiner",

    "Experienced"

)


joiner_comparison = (

    productivity
    .groupby(
        "Employee_Category",
        as_index=False
    )
    .agg(

        Employees=(
            "Employee_ID",
            "nunique"
        ),

        Workload_Units=(
            "Workload_Units",
            "sum"
        ),

        Completed_Units=(
            "Completed_Units",
            "sum"
        ),

        Revenue_Contribution=(
            "Revenue_Contribution",
            "sum"
        ),

        Average_Quality_Score=(
            "Quality_Score",
            "mean"
        )

    )

)


joiner_comparison[
    "Productivity_Percentage"
] = (

    joiner_comparison[
        "Completed_Units"
    ]

    /

    joiner_comparison[
        "Workload_Units"
    ]

    *
    100

)


# =========================================================
# 27. MONTHLY DEPARTMENT ANALYSIS
# =========================================================

monthly_department = (

    productivity
    .groupby(
        [
            "Month",
            "Department"
        ],
        as_index=False
    )
    .agg(

        Employees=(
            "Employee_ID",
            "nunique"
        ),

        Workload_Units=(
            "Workload_Units",
            "sum"
        ),

        Completed_Units=(
            "Completed_Units",
            "sum"
        ),

        Productive_Hours=(
            "Productive_Hours",
            "sum"
        ),

        Available_Hours=(
            "Available_Hours",
            "sum"
        ),

        Revenue_Contribution=(
            "Revenue_Contribution",
            "sum"
        )

    )

)


monthly_department[
    "Productivity_Percentage"
] = (

    monthly_department[
        "Completed_Units"
    ]

    /

    monthly_department[
        "Workload_Units"
    ]

    *
    100

)


monthly_department[
    "Capacity_Utilization_Percentage"
] = (

    monthly_department[
        "Productive_Hours"
    ]

    /

    monthly_department[
        "Available_Hours"
    ]

    *
    100

)


# =========================================================
# 28. TEAM PRODUCTIVITY / RISK BASE TABLE
# =========================================================

team_productivity = (

    productivity
    .groupby(
        [
            "Department",
            "Team"
        ],
        as_index=False
    )
    .agg(

        Employees=(
            "Employee_ID",
            "nunique"
        ),

        Workload_Units=(
            "Workload_Units",
            "sum"
        ),

        Completed_Units=(
            "Completed_Units",
            "sum"
        ),

        Productive_Hours=(
            "Productive_Hours",
            "sum"
        ),

        Available_Hours=(
            "Available_Hours",
            "sum"
        ),

        Revenue_Contribution=(
            "Revenue_Contribution",
            "sum"
        ),

        Average_Quality_Score=(
            "Quality_Score",
            "mean"
        )

    )

)


team_productivity[
    "Productivity_Percentage"
] = (

    team_productivity[
        "Completed_Units"
    ]

    /

    team_productivity[
        "Workload_Units"
    ]

    *
    100

)


team_productivity[
    "Capacity_Utilization_Percentage"
] = (

    team_productivity[
        "Productive_Hours"
    ]

    /

    team_productivity[
        "Available_Hours"
    ]

    *
    100

)


# =========================================================
# 29. ROUND RESULTS
# =========================================================

for df in [
    department_productivity,
    location_productivity,
    designation_productivity,
    manager_productivity,
    experience_productivity,
    joiner_comparison,
    monthly_department,
    team_productivity
]:

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    df[numeric_columns] = (
        df[numeric_columns]
        .round(2)
    )


# =========================================================
# 30. EXPORT ALL KPI TABLES TO EXCEL
# =========================================================

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    overall_kpi.to_excel(
        writer,
        sheet_name="Overall_KPI",
        index=False
    )

    monthly_kpi.to_excel(
        writer,
        sheet_name="Monthly_KPI",
        index=False
    )

    department_productivity.to_excel(
        writer,
        sheet_name="Department_KPI",
        index=False
    )

    location_productivity.to_excel(
        writer,
        sheet_name="Location_KPI",
        index=False
    )

    designation_productivity.to_excel(
        writer,
        sheet_name="Designation_KPI",
        index=False
    )

    manager_productivity.to_excel(
        writer,
        sheet_name="Manager_KPI",
        index=False
    )

    experience_productivity.to_excel(
        writer,
        sheet_name="Experience_KPI",
        index=False
    )

    joiner_comparison.to_excel(
        writer,
        sheet_name="Joiner_Comparison",
        index=False
    )

    monthly_department.to_excel(
        writer,
        sheet_name="Monthly_Department",
        index=False
    )

    team_productivity.to_excel(
        writer,
        sheet_name="Team_KPI",
        index=False
    )


# =========================================================
# 31. PRINT FINAL KPI SUMMARY
# =========================================================

print("\n")
print("=" * 55)
print("WORKFORCE KPI CALCULATION COMPLETED")
print("=" * 55)

print("\nOVERALL KPI SUMMARY\n")

print(
    overall_kpi.to_string(
        index=False
    )
)

print("\n")
print("=" * 55)

print(
    "KPI Excel file saved successfully:"
)

print(
    output_file
)

print("=" * 55)