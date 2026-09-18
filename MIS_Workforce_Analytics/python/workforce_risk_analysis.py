import pandas as pd
import numpy as np
from pathlib import Path


# =====================================================
# 1. FILE LOCATIONS
# =====================================================

file_path = Path(
    r"C:\Users\Hooooo\Documents\Excel\MIS_Workforce_Analytics\Cleaned\MIS_Workforce_Cleaned.xlsx"
)

output_folder = Path(
    r"C:\Users\Hooooo\Documents\Excel\MIS_Workforce_Analytics\output"
)

output_folder.mkdir(parents=True, exist_ok=True)


# =====================================================
# 2. LOAD DATASETS
# =====================================================

employee_master = pd.read_excel(
    file_path,
    sheet_name="Employee_Master"
)

attendance = pd.read_excel(
    file_path,
    sheet_name="Attendance"
)

leave_data = pd.read_excel(
    file_path,
    sheet_name="Leave"
)

overtime = pd.read_excel(
    file_path,
    sheet_name="Overtime"
)

productivity = pd.read_excel(
    file_path,
    sheet_name="Productivity"
)

attrition = pd.read_excel(
    file_path,
    sheet_name="Attrition"
)

print("All required datasets loaded successfully")


# =====================================================
# 3. DATE CONVERSION
# =====================================================

employee_master["Date_of_Joining"] = pd.to_datetime(
    employee_master["Date_of_Joining"],
    errors="coerce"
)

employee_master["Exit_Date"] = pd.to_datetime(
    employee_master["Exit_Date"],
    errors="coerce"
)

attendance["Work_Date"] = pd.to_datetime(
    attendance["Work_Date"],
    errors="coerce"
)

leave_data["Leave_Start"] = pd.to_datetime(
    leave_data["Leave_Start"],
    errors="coerce"
)

leave_data["Leave_End"] = pd.to_datetime(
    leave_data["Leave_End"],
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

attrition["Exit_Date"] = pd.to_datetime(
    attrition["Exit_Date"],
    errors="coerce"
)


# =====================================================
# 4. NUMERIC CONVERSION
# =====================================================

for column in [
    "Scheduled_Hours",
    "Actual_Hours",
    "Present_Flag"
]:
    attendance[column] = pd.to_numeric(
        attendance[column],
        errors="coerce"
    ).fillna(0)

leave_data["Leave_Days"] = pd.to_numeric(
    leave_data["Leave_Days"],
    errors="coerce"
).fillna(0)

overtime["OT_Hours"] = pd.to_numeric(
    overtime["OT_Hours"],
    errors="coerce"
).fillna(0)

for column in [
    "Experience_Years",
    "Workload_Units",
    "Completed_Units",
    "Productive_Hours",
    "Available_Hours",
    "Quality_Score",
    "Revenue_Contribution"
]:
    productivity[column] = pd.to_numeric(
        productivity[column],
        errors="coerce"
    ).fillna(0)

attrition["Tenure_Years"] = pd.to_numeric(
    attrition["Tenure_Years"],
    errors="coerce"
).fillna(0)


# =====================================================
# 5. CLEAN ATTRITION FLAG
# =====================================================

attrition["Voluntary_Exit_Flag"] = (
    attrition["Voluntary_Flag"]
    .astype(str)
    .str.strip()
    .str.lower()
    .isin([
        "yes",
        "y",
        "true",
        "1",
        "voluntary"
    ])
    .astype(int)
)


# =====================================================
# 6. CREATE MONTH COLUMNS
# =====================================================

attendance["Month"] = (
    attendance["Work_Date"]
    .dt.to_period("M")
    .astype(str)
)

overtime["Month"] = (
    overtime["OT_Date"]
    .dt.to_period("M")
    .astype(str)
)

productivity["Month_Label"] = (
    productivity["Month"]
    .dt.to_period("M")
    .astype(str)
)

attrition["Month"] = (
    attrition["Exit_Date"]
    .dt.to_period("M")
    .astype(str)
)


# =====================================================
# 7. ATTENDANCE AND ABSENTEEISM
# =====================================================

attendance["Lost_Hours"] = (
    attendance["Scheduled_Hours"]
    - attendance["Actual_Hours"]
).clip(lower=0)

attendance["Absent_Flag"] = np.where(
    attendance["Present_Flag"] == 0,
    1,
    0
)


department_attendance = attendance.groupby(
    "Department"
).agg(
    Attendance_Records=("Employee_ID", "count"),
    Unique_Employees=("Employee_ID", "nunique"),
    Present_Days=("Present_Flag", "sum"),
    Absent_Days=("Absent_Flag", "sum"),
    Scheduled_Hours=("Scheduled_Hours", "sum"),
    Actual_Hours=("Actual_Hours", "sum"),
    Lost_Hours=("Lost_Hours", "sum")
).reset_index()

department_attendance["Absenteeism_Percentage"] = np.where(
    department_attendance["Attendance_Records"] > 0,
    (
        department_attendance["Absent_Days"]
        / department_attendance["Attendance_Records"]
    ) * 100,
    0
)

department_attendance[
    "Hour_Based_Absenteeism_Percentage"
] = np.where(
    department_attendance["Scheduled_Hours"] > 0,
    (
        department_attendance["Lost_Hours"]
        / department_attendance["Scheduled_Hours"]
    ) * 100,
    0
)

department_attendance["Attendance_Percentage"] = np.where(
    department_attendance["Attendance_Records"] > 0,
    (
        department_attendance["Present_Days"]
        / department_attendance["Attendance_Records"]
    ) * 100,
    0
)

department_attendance[
    "Hour_Based_Attendance_Percentage"
] = np.where(
    department_attendance["Scheduled_Hours"] > 0,
    (
        department_attendance["Actual_Hours"]
        / department_attendance["Scheduled_Hours"]
    ) * 100,
    0
)

department_attendance[
    [
        "Scheduled_Hours",
        "Actual_Hours",
        "Lost_Hours",
        "Absenteeism_Percentage",
        "Hour_Based_Absenteeism_Percentage",
        "Attendance_Percentage",
        "Hour_Based_Attendance_Percentage"
    ]
] = department_attendance[
    [
        "Scheduled_Hours",
        "Actual_Hours",
        "Lost_Hours",
        "Absenteeism_Percentage",
        "Hour_Based_Absenteeism_Percentage",
        "Attendance_Percentage",
        "Hour_Based_Attendance_Percentage"
    ]
].round(2)

department_attendance = department_attendance.sort_values(
    by="Absenteeism_Percentage",
    ascending=False
)

print("\nDEPARTMENT ATTENDANCE AND ABSENTEEISM")
print(department_attendance.to_string(index=False))

department_attendance.to_csv(
    output_folder / "department_attendance_analysis.csv",
    index=False
)


monthly_attendance = attendance.groupby(
    "Month"
).agg(
    Attendance_Records=("Employee_ID", "count"),
    Unique_Employees=("Employee_ID", "nunique"),
    Present_Days=("Present_Flag", "sum"),
    Absent_Days=("Absent_Flag", "sum"),
    Scheduled_Hours=("Scheduled_Hours", "sum"),
    Actual_Hours=("Actual_Hours", "sum"),
    Lost_Hours=("Lost_Hours", "sum")
).reset_index()

monthly_attendance["Absenteeism_Percentage"] = np.where(
    monthly_attendance["Attendance_Records"] > 0,
    (
        monthly_attendance["Absent_Days"]
        / monthly_attendance["Attendance_Records"]
    ) * 100,
    0
)

monthly_attendance[
    "Hour_Based_Absenteeism_Percentage"
] = np.where(
    monthly_attendance["Scheduled_Hours"] > 0,
    (
        monthly_attendance["Lost_Hours"]
        / monthly_attendance["Scheduled_Hours"]
    ) * 100,
    0
)

monthly_attendance["Attendance_Percentage"] = np.where(
    monthly_attendance["Attendance_Records"] > 0,
    (
        monthly_attendance["Present_Days"]
        / monthly_attendance["Attendance_Records"]
    ) * 100,
    0
)

monthly_attendance[
    "Hour_Based_Attendance_Percentage"
] = np.where(
    monthly_attendance["Scheduled_Hours"] > 0,
    (
        monthly_attendance["Actual_Hours"]
        / monthly_attendance["Scheduled_Hours"]
    ) * 100,
    0
)

monthly_attendance[
    [
        "Scheduled_Hours",
        "Actual_Hours",
        "Lost_Hours",
        "Absenteeism_Percentage",
        "Hour_Based_Absenteeism_Percentage",
        "Attendance_Percentage",
        "Hour_Based_Attendance_Percentage"
    ]
] = monthly_attendance[
    [
        "Scheduled_Hours",
        "Actual_Hours",
        "Lost_Hours",
        "Absenteeism_Percentage",
        "Hour_Based_Absenteeism_Percentage",
        "Attendance_Percentage",
        "Hour_Based_Attendance_Percentage"
    ]
].round(2)

monthly_attendance = monthly_attendance.sort_values(
    by="Month"
)

monthly_attendance[
    "Absenteeism_Change_Percentage_Points"
] = monthly_attendance[
    "Absenteeism_Percentage"
].diff().round(2)

print("\nMONTHLY ATTENDANCE AND ABSENTEEISM")
print(monthly_attendance.to_string(index=False))

monthly_attendance.to_csv(
    output_folder / "monthly_attendance_analysis.csv",
    index=False
)


# =====================================================
# 8. LEAVE UTILIZATION
# Annual entitlement assumption: 12 days per employee
# =====================================================

annual_leave_entitlement = 12

leave_data["Approval_Status_Clean"] = (
    leave_data["Approval_Status"]
    .astype(str)
    .str.strip()
    .str.lower()
)

leave_data["Approved_Leave_Days"] = np.where(
    leave_data["Approval_Status_Clean"] == "approved",
    leave_data["Leave_Days"],
    0
)

leave_data["Rejected_Leave_Days"] = np.where(
    leave_data["Approval_Status_Clean"] == "rejected",
    leave_data["Leave_Days"],
    0
)

employee_department_map = employee_master[
    ["Employee_ID", "Department"]
].drop_duplicates(
    subset="Employee_ID"
)

leave_analysis_data = leave_data.merge(
    employee_department_map,
    on="Employee_ID",
    how="left"
)

department_leave = leave_analysis_data.groupby(
    "Department"
).agg(
    Leave_Requests=("Leave_ID", "count"),
    Employees_Requesting_Leave=(
        "Employee_ID",
        "nunique"
    ),
    Requested_Leave_Days=("Leave_Days", "sum"),
    Approved_Leave_Days=(
        "Approved_Leave_Days",
        "sum"
    ),
    Rejected_Leave_Days=(
        "Rejected_Leave_Days",
        "sum"
    )
).reset_index()

department_employee_count = employee_master.groupby(
    "Department"
).agg(
    Department_Employees=("Employee_ID", "nunique")
).reset_index()

department_leave = department_leave.merge(
    department_employee_count,
    on="Department",
    how="left"
)

department_leave["Available_Leave_Days"] = (
    department_leave["Department_Employees"]
    * annual_leave_entitlement
)

department_leave[
    "Leave_Utilization_Percentage"
] = np.where(
    department_leave["Available_Leave_Days"] > 0,
    (
        department_leave["Approved_Leave_Days"]
        / department_leave["Available_Leave_Days"]
    ) * 100,
    0
)

department_leave[
    "Leave_Approval_Percentage"
] = np.where(
    department_leave["Requested_Leave_Days"] > 0,
    (
        department_leave["Approved_Leave_Days"]
        / department_leave["Requested_Leave_Days"]
    ) * 100,
    0
)

department_leave[
    "Average_Approved_Leave_Per_Employee"
] = np.where(
    department_leave["Department_Employees"] > 0,
    (
        department_leave["Approved_Leave_Days"]
        / department_leave["Department_Employees"]
    ),
    0
)

department_leave[
    [
        "Leave_Utilization_Percentage",
        "Leave_Approval_Percentage",
        "Average_Approved_Leave_Per_Employee"
    ]
] = department_leave[
    [
        "Leave_Utilization_Percentage",
        "Leave_Approval_Percentage",
        "Average_Approved_Leave_Per_Employee"
    ]
].round(2)

department_leave = department_leave.sort_values(
    by="Leave_Utilization_Percentage",
    ascending=False
)

print("\nDEPARTMENT LEAVE UTILIZATION ANALYSIS")
print(department_leave.to_string(index=False))

department_leave.to_csv(
    output_folder / "department_leave_analysis.csv",
    index=False
)


leave_type_analysis = leave_analysis_data.groupby(
    "Leave_Type"
).agg(
    Leave_Requests=("Leave_ID", "count"),
    Requested_Leave_Days=("Leave_Days", "sum"),
    Approved_Leave_Days=(
        "Approved_Leave_Days",
        "sum"
    ),
    Rejected_Leave_Days=(
        "Rejected_Leave_Days",
        "sum"
    )
).reset_index()

leave_type_analysis[
    "Approval_Percentage"
] = np.where(
    leave_type_analysis["Requested_Leave_Days"] > 0,
    (
        leave_type_analysis["Approved_Leave_Days"]
        / leave_type_analysis["Requested_Leave_Days"]
    ) * 100,
    0
)

leave_type_analysis[
    "Approval_Percentage"
] = leave_type_analysis[
    "Approval_Percentage"
].round(2)

leave_type_analysis.to_csv(
    output_folder / "leave_type_analysis.csv",
    index=False
)


# =====================================================
# 9. OVERTIME ANALYSIS
# =====================================================

department_overtime = overtime.groupby(
    "Department"
).agg(
    OT_Records=("OT_ID", "count"),
    Unique_Employees=("Employee_ID", "nunique"),
    Total_OT_Hours=("OT_Hours", "sum"),
    Average_OT_Hours=("OT_Hours", "mean"),
    Maximum_OT_Hours=("OT_Hours", "max")
).reset_index()

department_overtime[
    "OT_Hours_Per_Employee"
] = np.where(
    department_overtime["Unique_Employees"] > 0,
    (
        department_overtime["Total_OT_Hours"]
        / department_overtime["Unique_Employees"]
    ),
    0
)

department_overtime[
    [
        "Total_OT_Hours",
        "Average_OT_Hours",
        "Maximum_OT_Hours",
        "OT_Hours_Per_Employee"
    ]
] = department_overtime[
    [
        "Total_OT_Hours",
        "Average_OT_Hours",
        "Maximum_OT_Hours",
        "OT_Hours_Per_Employee"
    ]
].round(2)

department_overtime = department_overtime.sort_values(
    by="Total_OT_Hours",
    ascending=False
)

print("\nDEPARTMENT OVERTIME ANALYSIS")
print(department_overtime.to_string(index=False))

department_overtime.to_csv(
    output_folder / "department_overtime_analysis.csv",
    index=False
)


monthly_overtime = overtime.groupby(
    "Month"
).agg(
    OT_Records=("OT_ID", "count"),
    Unique_Employees=("Employee_ID", "nunique"),
    Total_OT_Hours=("OT_Hours", "sum"),
    Average_OT_Hours=("OT_Hours", "mean")
).reset_index()

monthly_overtime[
    "OT_Hours_Per_Employee"
] = np.where(
    monthly_overtime["Unique_Employees"] > 0,
    (
        monthly_overtime["Total_OT_Hours"]
        / monthly_overtime["Unique_Employees"]
    ),
    0
)

monthly_overtime[
    [
        "Total_OT_Hours",
        "Average_OT_Hours",
        "OT_Hours_Per_Employee"
    ]
] = monthly_overtime[
    [
        "Total_OT_Hours",
        "Average_OT_Hours",
        "OT_Hours_Per_Employee"
    ]
].round(2)

monthly_overtime = monthly_overtime.sort_values(
    by="Month"
)

monthly_overtime["OT_Growth_Percentage"] = (
    monthly_overtime["Total_OT_Hours"]
    .pct_change() * 100
).round(2)

print("\nMONTHLY OVERTIME ANALYSIS")
print(monthly_overtime.to_string(index=False))

monthly_overtime.to_csv(
    output_folder / "monthly_overtime_analysis.csv",
    index=False
)


team_overtime = overtime.groupby(
    ["Department", "Team"]
).agg(
    Unique_Employees=("Employee_ID", "nunique"),
    Total_OT_Hours=("OT_Hours", "sum"),
    Average_OT_Hours=("OT_Hours", "mean")
).reset_index()

team_overtime[
    "OT_Hours_Per_Employee"
] = np.where(
    team_overtime["Unique_Employees"] > 0,
    (
        team_overtime["Total_OT_Hours"]
        / team_overtime["Unique_Employees"]
    ),
    0
)

team_overtime[
    [
        "Total_OT_Hours",
        "Average_OT_Hours",
        "OT_Hours_Per_Employee"
    ]
] = team_overtime[
    [
        "Total_OT_Hours",
        "Average_OT_Hours",
        "OT_Hours_Per_Employee"
    ]
].round(2)

team_overtime = team_overtime.sort_values(
    by="OT_Hours_Per_Employee",
    ascending=False
)

team_overtime.to_csv(
    output_folder / "team_overtime_analysis.csv",
    index=False
)


# =====================================================
# 10. OVERTIME VS PRODUCTIVITY
# =====================================================

employee_monthly_overtime = overtime.groupby(
    ["Employee_ID", "Month"]
).agg(
    OT_Hours=("OT_Hours", "sum")
).reset_index()

employee_monthly_productivity = productivity.groupby(
    ["Employee_ID", "Month_Label"]
).agg(
    Department=("Department", "first"),
    Team=("Team", "first"),
    Workload_Units=("Workload_Units", "sum"),
    Completed_Units=("Completed_Units", "sum"),
    Productive_Hours=("Productive_Hours", "sum"),
    Available_Hours=("Available_Hours", "sum")
).reset_index()

employee_monthly_productivity[
    "Productivity_Percentage"
] = np.where(
    employee_monthly_productivity["Workload_Units"] > 0,
    (
        employee_monthly_productivity["Completed_Units"]
        / employee_monthly_productivity["Workload_Units"]
    ) * 100,
    0
)

employee_monthly_productivity[
    "Capacity_Utilization_Percentage"
] = np.where(
    employee_monthly_productivity["Available_Hours"] > 0,
    (
        employee_monthly_productivity["Productive_Hours"]
        / employee_monthly_productivity["Available_Hours"]
    ) * 100,
    0
)

overtime_productivity = (
    employee_monthly_productivity.merge(
        employee_monthly_overtime,
        left_on=[
            "Employee_ID",
            "Month_Label"
        ],
        right_on=[
            "Employee_ID",
            "Month"
        ],
        how="left"
    )
)

overtime_productivity["OT_Hours"] = (
    overtime_productivity["OT_Hours"].fillna(0)
)

correlation = overtime_productivity[
    [
        "OT_Hours",
        "Productivity_Percentage"
    ]
].corr().iloc[0, 1]

if pd.isna(correlation):
    correlation = 0

if correlation >= 0.50:
    correlation_result = "Strong positive relationship"

elif correlation >= 0.20:
    correlation_result = "Weak positive relationship"

elif correlation <= -0.50:
    correlation_result = "Strong negative relationship"

elif correlation <= -0.20:
    correlation_result = "Weak negative relationship"

else:
    correlation_result = "No meaningful relationship"

print("\nOVERTIME VS PRODUCTIVITY CORRELATION")
print("Correlation:", round(correlation, 4))
print("Interpretation:", correlation_result)

high_ot_threshold = overtime_productivity[
    "OT_Hours"
].quantile(0.75)

median_productivity = overtime_productivity[
    "Productivity_Percentage"
].median()

overtime_productivity[
    "OT_Productivity_Status"
] = np.select(
    [
        (
            overtime_productivity["OT_Hours"]
            >= high_ot_threshold
        )
        &
        (
            overtime_productivity[
                "Productivity_Percentage"
            ]
            < median_productivity
        ),

        (
            overtime_productivity["OT_Hours"]
            >= high_ot_threshold
        )
        &
        (
            overtime_productivity[
                "Productivity_Percentage"
            ]
            >= median_productivity
        )
    ],
    [
        "High OT - Low Productivity - Inefficiency Risk",
        "High OT - High Productivity"
    ],
    default="Normal OT"
)

overtime_productivity[
    [
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage",
        "OT_Hours"
    ]
] = overtime_productivity[
    [
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage",
        "OT_Hours"
    ]
].round(2)

overtime_productivity.to_csv(
    output_folder /
    "overtime_productivity_analysis.csv",
    index=False
)

overtime_inefficiency = overtime_productivity[
    overtime_productivity[
        "OT_Productivity_Status"
    ]
    ==
    "High OT - Low Productivity - Inefficiency Risk"
].copy()

overtime_inefficiency = overtime_inefficiency.sort_values(
    by="OT_Hours",
    ascending=False
)

print("\nHIGH OVERTIME AND LOW PRODUCTIVITY EXCEPTIONS")
print("Total exception records:", len(overtime_inefficiency))

overtime_inefficiency.to_csv(
    output_folder /
    "overtime_productivity_exceptions.csv",
    index=False
)

correlation_summary = pd.DataFrame({
    "Metric": [
        "OT Productivity Correlation",
        "High OT Threshold",
        "Median Productivity",
        "Interpretation"
    ],
    "Value": [
        round(correlation, 4),
        round(high_ot_threshold, 2),
        round(median_productivity, 2),
        correlation_result
    ]
})

correlation_summary.to_csv(
    output_folder /
    "overtime_productivity_correlation.csv",
    index=False
)


# =====================================================
# 11. ATTRITION ANALYSIS
# =====================================================

analysis_start = productivity["Month"].min()

analysis_end = (
    productivity["Month"].max()
    + pd.offsets.MonthEnd(0)
)

opening_headcount = employee_master[
    (
        employee_master["Date_of_Joining"]
        < analysis_start
    )
    &
    (
        employee_master["Exit_Date"].isna()
        |
        (
            employee_master["Exit_Date"]
            >= analysis_start
        )
    )
].groupby(
    "Department"
)["Employee_ID"].nunique().reset_index(
    name="Opening_Headcount"
)

closing_headcount = employee_master[
    (
        employee_master["Date_of_Joining"]
        <= analysis_end
    )
    &
    (
        employee_master["Exit_Date"].isna()
        |
        (
            employee_master["Exit_Date"]
            > analysis_end
        )
    )
].groupby(
    "Department"
)["Employee_ID"].nunique().reset_index(
    name="Closing_Headcount"
)

department_exits = attrition.groupby(
    "Department"
).agg(
    Exits=("Employee_ID", "nunique"),
    Voluntary_Exits=(
        "Voluntary_Exit_Flag",
        "sum"
    ),
    Average_Tenure_Years=(
        "Tenure_Years",
        "mean"
    )
).reset_index()

department_attrition = department_exits.merge(
    opening_headcount,
    on="Department",
    how="outer"
).merge(
    closing_headcount,
    on="Department",
    how="outer"
)

for column in [
    "Exits",
    "Voluntary_Exits",
    "Average_Tenure_Years",
    "Opening_Headcount",
    "Closing_Headcount"
]:
    department_attrition[column] = pd.to_numeric(
        department_attrition[column],
        errors="coerce"
    ).fillna(0)

department_attrition["Average_Headcount"] = (
    department_attrition["Opening_Headcount"]
    + department_attrition["Closing_Headcount"]
) / 2

department_attrition[
    "Attrition_Percentage"
] = np.where(
    department_attrition["Average_Headcount"] > 0,
    (
        department_attrition["Exits"]
        / department_attrition["Average_Headcount"]
    ) * 100,
    0
)

department_attrition[
    "Voluntary_Attrition_Percentage"
] = np.where(
    department_attrition["Average_Headcount"] > 0,
    (
        department_attrition["Voluntary_Exits"]
        / department_attrition["Average_Headcount"]
    ) * 100,
    0
)

department_attrition[
    [
        "Average_Tenure_Years",
        "Average_Headcount",
        "Attrition_Percentage",
        "Voluntary_Attrition_Percentage"
    ]
] = department_attrition[
    [
        "Average_Tenure_Years",
        "Average_Headcount",
        "Attrition_Percentage",
        "Voluntary_Attrition_Percentage"
    ]
].round(2)

department_attrition = department_attrition.sort_values(
    by="Attrition_Percentage",
    ascending=False
)

print("\nDEPARTMENT ATTRITION ANALYSIS")
print(department_attrition.to_string(index=False))

department_attrition.to_csv(
    output_folder / "department_attrition_analysis.csv",
    index=False
)


monthly_attrition = attrition.groupby(
    "Month"
).agg(
    Exits=("Employee_ID", "nunique"),
    Voluntary_Exits=(
        "Voluntary_Exit_Flag",
        "sum"
    ),
    Average_Tenure_Years=(
        "Tenure_Years",
        "mean"
    )
).reset_index()

monthly_attrition[
    "Average_Tenure_Years"
] = monthly_attrition[
    "Average_Tenure_Years"
].round(2)

monthly_attrition = monthly_attrition.sort_values(
    by="Month"
)

monthly_attrition.to_csv(
    output_folder / "monthly_attrition_analysis.csv",
    index=False
)


exit_reason_analysis = attrition.groupby(
    "Exit_Reason"
).agg(
    Exit_Count=("Employee_ID", "nunique")
).reset_index()

total_exits = exit_reason_analysis[
    "Exit_Count"
].sum()

exit_reason_analysis[
    "Exit_Percentage"
] = np.where(
    total_exits > 0,
    (
        exit_reason_analysis["Exit_Count"]
        / total_exits
    ) * 100,
    0
)

exit_reason_analysis[
    "Exit_Percentage"
] = exit_reason_analysis[
    "Exit_Percentage"
].round(2)

exit_reason_analysis = exit_reason_analysis.sort_values(
    by="Exit_Count",
    ascending=False
)

exit_reason_analysis.to_csv(
    output_folder / "exit_reason_analysis.csv",
    index=False
)


# =====================================================
# 12. NEW JOINER VS EXPERIENCED
# =====================================================

productivity["Employee_Group"] = np.where(
    productivity["Experience_Years"] <= 1,
    "New Joiner - 0 to 1 Year",
    "Experienced - Above 1 Year"
)

experience_comparison = productivity.groupby(
    "Employee_Group"
).agg(
    Employee_Months=("Employee_ID", "count"),
    Unique_Employees=("Employee_ID", "nunique"),
    Workload_Units=("Workload_Units", "sum"),
    Completed_Units=("Completed_Units", "sum"),
    Productive_Hours=("Productive_Hours", "sum"),
    Available_Hours=("Available_Hours", "sum"),
    Average_Quality_Score=("Quality_Score", "mean"),
    Revenue_Contribution=(
        "Revenue_Contribution",
        "sum"
    )
).reset_index()

experience_comparison[
    "Productivity_Percentage"
] = np.where(
    experience_comparison["Workload_Units"] > 0,
    (
        experience_comparison["Completed_Units"]
        / experience_comparison["Workload_Units"]
    ) * 100,
    0
)

experience_comparison[
    "Capacity_Utilization_Percentage"
] = np.where(
    experience_comparison["Available_Hours"] > 0,
    (
        experience_comparison["Productive_Hours"]
        / experience_comparison["Available_Hours"]
    ) * 100,
    0
)

experience_comparison[
    "Revenue_Per_Employee_Month"
] = np.where(
    experience_comparison["Employee_Months"] > 0,
    (
        experience_comparison["Revenue_Contribution"]
        / experience_comparison["Employee_Months"]
    ),
    0
)

experience_comparison[
    [
        "Average_Quality_Score",
        "Revenue_Contribution",
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage",
        "Revenue_Per_Employee_Month"
    ]
] = experience_comparison[
    [
        "Average_Quality_Score",
        "Revenue_Contribution",
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage",
        "Revenue_Per_Employee_Month"
    ]
].round(2)

print("\nNEW JOINER VS EXPERIENCED EMPLOYEE ANALYSIS")
print(experience_comparison.to_string(index=False))

experience_comparison.to_csv(
    output_folder /
    "new_joiner_vs_experienced_analysis.csv",
    index=False
)


# =====================================================
# 13. DEPARTMENT WORKFORCE RISK
# =====================================================

department_productivity = productivity.groupby(
    "Department"
).agg(
    Workload_Units=("Workload_Units", "sum"),
    Completed_Units=("Completed_Units", "sum"),
    Productive_Hours=("Productive_Hours", "sum"),
    Available_Hours=("Available_Hours", "sum"),
    Revenue_Contribution=(
        "Revenue_Contribution",
        "sum"
    )
).reset_index()

department_productivity[
    "Productivity_Percentage"
] = np.where(
    department_productivity["Workload_Units"] > 0,
    (
        department_productivity["Completed_Units"]
        / department_productivity["Workload_Units"]
    ) * 100,
    0
)

department_productivity[
    "Capacity_Utilization_Percentage"
] = np.where(
    department_productivity["Available_Hours"] > 0,
    (
        department_productivity["Productive_Hours"]
        / department_productivity["Available_Hours"]
    ) * 100,
    0
)

workforce_risk = department_productivity.merge(
    department_attendance[
        [
            "Department",
            "Absenteeism_Percentage",
            "Hour_Based_Absenteeism_Percentage"
        ]
    ],
    on="Department",
    how="left"
).merge(
    department_overtime[
        [
            "Department",
            "OT_Hours_Per_Employee"
        ]
    ],
    on="Department",
    how="left"
).merge(
    department_attrition[
        [
            "Department",
            "Attrition_Percentage"
        ]
    ],
    on="Department",
    how="left"
)

workforce_risk = workforce_risk.fillna(0)

high_ot_department_threshold = workforce_risk[
    "OT_Hours_Per_Employee"
].quantile(0.75)

workforce_risk["Risk_Score"] = 0

workforce_risk.loc[
    workforce_risk["Productivity_Percentage"] < 85,
    "Risk_Score"
] += 2

workforce_risk.loc[
    workforce_risk["Productivity_Percentage"] < 75,
    "Risk_Score"
] += 1

workforce_risk.loc[
    workforce_risk["Absenteeism_Percentage"] > 5,
    "Risk_Score"
] += 1

workforce_risk.loc[
    workforce_risk["OT_Hours_Per_Employee"]
    >= high_ot_department_threshold,
    "Risk_Score"
] += 1

workforce_risk.loc[
    workforce_risk["Attrition_Percentage"] > 10,
    "Risk_Score"
] += 2

workforce_risk.loc[
    workforce_risk[
        "Capacity_Utilization_Percentage"
    ] > 95,
    "Risk_Score"
] += 1

workforce_risk[
    "Workforce_Risk_Level"
] = np.select(
    [
        workforce_risk["Risk_Score"] >= 5,
        workforce_risk["Risk_Score"] >= 3,
        workforce_risk["Risk_Score"] >= 1
    ],
    [
        "Critical Risk",
        "High Risk",
        "Medium Risk"
    ],
    default="Low Risk"
)


def create_risk_reason(row):

    reasons = []

    if row["Productivity_Percentage"] < 85:
        reasons.append("Low Productivity")

    if row["Absenteeism_Percentage"] > 5:
        reasons.append("High Absenteeism")

    if (
        row["OT_Hours_Per_Employee"]
        >= high_ot_department_threshold
    ):
        reasons.append("High Overtime")

    if row["Attrition_Percentage"] > 10:
        reasons.append("High Attrition")

    if (
        row["Capacity_Utilization_Percentage"]
        > 95
    ):
        reasons.append("Over-Utilization")

    if len(reasons) == 0:
        return "No Major Risk"

    return ", ".join(reasons)


workforce_risk["Risk_Reasons"] = workforce_risk.apply(
    create_risk_reason,
    axis=1
)

workforce_risk[
    [
        "Revenue_Contribution",
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage",
        "Absenteeism_Percentage",
        "Hour_Based_Absenteeism_Percentage",
        "OT_Hours_Per_Employee",
        "Attrition_Percentage"
    ]
] = workforce_risk[
    [
        "Revenue_Contribution",
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage",
        "Absenteeism_Percentage",
        "Hour_Based_Absenteeism_Percentage",
        "OT_Hours_Per_Employee",
        "Attrition_Percentage"
    ]
].round(2)

workforce_risk = workforce_risk.sort_values(
    by=[
        "Risk_Score",
        "Productivity_Percentage"
    ],
    ascending=[
        False,
        True
    ]
)

print("\nDEPARTMENT WORKFORCE RISK SUMMARY")
print(workforce_risk.to_string(index=False))

workforce_risk.to_csv(
    output_folder /
    "department_workforce_risk_summary.csv",
    index=False
)


# =====================================================
# 14. OVERALL VALIDATION SUMMARY
# =====================================================

overall_absenteeism = (
    attendance["Absent_Flag"].sum()
    / len(attendance)

) * 100

overall_hour_absenteeism = (
    attendance["Lost_Hours"].sum()
    / attendance["Scheduled_Hours"].sum()
) * 100

overall_leave_utilization = (
    leave_data["Approved_Leave_Days"].sum()
    / (
        employee_master["Employee_ID"].nunique()
        * annual_leave_entitlement
    )
) * 100

validation_summary = pd.DataFrame({
    "Metric": [
        "Total Attendance Records",
        "Present Days",
        "Absent Days",
        "Overall Absenteeism Percentage",
        "Overall Hour Based Absenteeism Percentage",
        "Approved Leave Days",
        "Available Leave Days",
        "Overall Leave Utilization Percentage"
    ],
    "Value": [
        len(attendance),
        int(attendance["Present_Flag"].sum()),
        int(attendance["Absent_Flag"].sum()),
        round(overall_absenteeism, 2),
        round(overall_hour_absenteeism, 2),
        round(leave_data["Approved_Leave_Days"].sum(), 2),
        (
            employee_master["Employee_ID"].nunique()
            * annual_leave_entitlement
        ),
        round(overall_leave_utilization, 2)
    ]
})

print("\nOVERALL VALIDATION SUMMARY")
print(validation_summary.to_string(index=False))

validation_summary.to_csv(
    output_folder / "workforce_validation_summary.csv",
    index=False
)


# =====================================================
# 15. COMPLETION MESSAGE
# =====================================================

print("\n=====================================================")
print("WORKFORCE RISK ANALYSIS COMPLETED SUCCESSFULLY")
print("=====================================================")

print("\nOutput location:")
print(output_folder)