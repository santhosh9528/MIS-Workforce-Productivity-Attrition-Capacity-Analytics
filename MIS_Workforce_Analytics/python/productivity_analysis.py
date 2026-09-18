import pandas as pd

# Cleaned workbook location
file_path = "../Cleaned/MIS_Workforce_Cleaned.xlsx"

# Productivity sheet load
productivity = pd.read_excel(
    file_path,
    sheet_name="Productivity"
)

print("Productivity dataset loaded successfully")
print("Total records:", len(productivity))

# Department-wise aggregation
department_analysis = productivity.groupby(
    "Department"
).agg(
    Employee_Months=("Employee_ID", "count"),
    Workload_Units=("Workload_Units", "sum"),
    Completed_Units=("Completed_Units", "sum"),
    Productive_Hours=("Productive_Hours", "sum"),
    Available_Hours=("Available_Hours", "sum"),
    Average_Quality_Score=("Quality_Score", "mean"),
    Revenue_Contribution=("Revenue_Contribution", "sum")
).reset_index()

# Weighted productivity
department_analysis["Productivity_Percentage"] = (
    department_analysis["Completed_Units"]
    / department_analysis["Workload_Units"]
) * 100

# Capacity utilization
department_analysis["Capacity_Utilization_Percentage"] = (
    department_analysis["Productive_Hours"]
    / department_analysis["Available_Hours"]
) * 100

# Round values
department_analysis[
    "Average_Quality_Score"
] = department_analysis["Average_Quality_Score"].round(2)

department_analysis[
    "Revenue_Contribution"
] = department_analysis["Revenue_Contribution"].round(2)

department_analysis[
    "Productivity_Percentage"
] = department_analysis["Productivity_Percentage"].round(2)

department_analysis[
    "Capacity_Utilization_Percentage"
] = department_analysis[
    "Capacity_Utilization_Percentage"
].round(2)

# Sort by productivity
department_analysis = department_analysis.sort_values(
    "Productivity_Percentage",
    ascending=False
)

print("\nDEPARTMENT PRODUCTIVITY ANALYSIS")
print(department_analysis.to_string(index=False))

# Save output
department_analysis.to_csv(
    "../output/department_productivity_analysis.csv",
    index=False
)

print("\nDepartment analysis saved successfully")


# =====================================================
# LOCATION-WISE PRODUCTIVITY ANALYSIS
# =====================================================

location_analysis = productivity.groupby(
    "Location"
).agg(
    Employee_Months=("Employee_ID", "count"),
    Workload_Units=("Workload_Units", "sum"),
    Completed_Units=("Completed_Units", "sum"),
    Productive_Hours=("Productive_Hours", "sum"),
    Available_Hours=("Available_Hours", "sum"),
    Average_Quality_Score=("Quality_Score", "mean"),
    Revenue_Contribution=("Revenue_Contribution", "sum")
).reset_index()

# Weighted productivity
location_analysis["Productivity_Percentage"] = (
    location_analysis["Completed_Units"]
    / location_analysis["Workload_Units"]
) * 100

# Capacity utilization
location_analysis["Capacity_Utilization_Percentage"] = (
    location_analysis["Productive_Hours"]
    / location_analysis["Available_Hours"]
) * 100

# Round values
location_analysis["Average_Quality_Score"] = (
    location_analysis["Average_Quality_Score"].round(2)
)

location_analysis["Revenue_Contribution"] = (
    location_analysis["Revenue_Contribution"].round(2)
)

location_analysis["Productivity_Percentage"] = (
    location_analysis["Productivity_Percentage"].round(2)
)

location_analysis["Capacity_Utilization_Percentage"] = (
    location_analysis[
        "Capacity_Utilization_Percentage"
    ].round(2)
)

# Highest productivity first
location_analysis = location_analysis.sort_values(
    "Productivity_Percentage",
    ascending=False
)

print("\nLOCATION-WISE PRODUCTIVITY ANALYSIS")
print(location_analysis.to_string(index=False))

# Save output
location_analysis.to_csv(
"../output/location_productivity_analysis.csv",
    index=False
)

print("\nLocation analysis saved successfully")



# =====================================================
# DESIGNATION-WISE PRODUCTIVITY ANALYSIS
# =====================================================

designation_analysis = productivity.groupby(
    "Designation"
).agg(
    Employee_Months=("Employee_ID", "count"),
    Workload_Units=("Workload_Units", "sum"),
    Completed_Units=("Completed_Units", "sum"),
    Productive_Hours=("Productive_Hours", "sum"),
    Available_Hours=("Available_Hours", "sum"),
    Average_Quality_Score=("Quality_Score", "mean"),
    Revenue_Contribution=("Revenue_Contribution", "sum")
).reset_index()

# Weighted productivity percentage
designation_analysis["Productivity_Percentage"] = (
    designation_analysis["Completed_Units"]
    / designation_analysis["Workload_Units"]
) * 100

# Weighted capacity utilization percentage
designation_analysis["Capacity_Utilization_Percentage"] = (
    designation_analysis["Productive_Hours"]
    / designation_analysis["Available_Hours"]
) * 100

# Round numeric columns
designation_analysis[
    [
        "Average_Quality_Score",
        "Revenue_Contribution",
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage"
    ]
] = designation_analysis[
    [
        "Average_Quality_Score",
        "Revenue_Contribution",
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage"
    ]
].round(2)

# Highest productivity first
designation_analysis = designation_analysis.sort_values(
    by="Productivity_Percentage",
    ascending=False
)

print("\nDESIGNATION-WISE PRODUCTIVITY ANALYSIS")
print(designation_analysis.to_string(index=False))

designation_analysis.to_csv(
    "../output/designation_productivity_analysis.csv",
    index=False
)

print("\nDesignation analysis saved successfully")

# =====================================================
# EXPERIENCE-WISE PRODUCTIVITY ANALYSIS
# =====================================================

# Create experience groups
productivity["Experience_Group"] = pd.cut(
    productivity["Experience_Years"],
    bins=[-float("inf"), 1, 3, 5, float("inf")],
    labels=[
        "0-1 Years",
        "1-3 Years",
        "3-5 Years",
        "Above 5 Years"
    ]
)

experience_analysis = productivity.groupby(
    "Experience_Group",
    observed=True
).agg(
    Employee_Months=("Employee_ID", "count"),
    Unique_Employees=("Employee_ID", "nunique"),
    Workload_Units=("Workload_Units", "sum"),
    Completed_Units=("Completed_Units", "sum"),
    Productive_Hours=("Productive_Hours", "sum"),
    Available_Hours=("Available_Hours", "sum"),
    Average_Quality_Score=("Quality_Score", "mean"),
    Revenue_Contribution=("Revenue_Contribution", "sum")
).reset_index()

# Weighted productivity percentage
experience_analysis["Productivity_Percentage"] = (
    experience_analysis["Completed_Units"]
    / experience_analysis["Workload_Units"]
) * 100

# Weighted capacity utilization
experience_analysis["Capacity_Utilization_Percentage"] = (
    experience_analysis["Productive_Hours"]
    / experience_analysis["Available_Hours"]
) * 100

# Revenue contribution per employee-month
experience_analysis["Revenue_Per_Employee_Month"] = (
    experience_analysis["Revenue_Contribution"]
    / experience_analysis["Employee_Months"]
)

# Round numeric results
columns_to_round = [
    "Average_Quality_Score",
    "Revenue_Contribution",
    "Productivity_Percentage",
    "Capacity_Utilization_Percentage",
    "Revenue_Per_Employee_Month"
]

experience_analysis[columns_to_round] = (
    experience_analysis[columns_to_round].round(2)
)

print("\nEXPERIENCE-WISE PRODUCTIVITY ANALYSIS")
print(experience_analysis.to_string(index=False))

experience_analysis.to_csv(
   "../output/experience_productivity_analysis.csv",
    index=False
)

print("\nExperience analysis saved successfully")


# =====================================================
# REMAINING PRODUCTIVITY ANALYSIS
# Manager, Month, Team, Department Trend,
# Declining Teams and Declining Employees
# =====================================================

import numpy as np

# -----------------------------------------------------
# PREPARE MONTH COLUMN
# -----------------------------------------------------

productivity["Month"] = pd.to_datetime(
    productivity["Month"],
    errors="coerce"
)

if productivity["Month"].isna().any():
    print(
        "\nWarning:",
        productivity["Month"].isna().sum(),
        "records contain invalid Month values"
    )

productivity["Month_Label"] = (
    productivity["Month"].dt.strftime("%Y-%m")
)

# Replace missing category values
productivity["Manager"] = productivity["Manager"].fillna(
    "Manager Not Assigned"
)

productivity["Team"] = productivity["Team"].fillna(
    "Team Not Assigned"
)


# =====================================================
# COMMON SUMMARY FUNCTION
# =====================================================

def create_productivity_summary(data, group_column):

    summary = data.groupby(
        group_column,
        observed=True
    ).agg(
        Employee_Months=("Employee_ID", "count"),
        Unique_Employees=("Employee_ID", "nunique"),
        Workload_Units=("Workload_Units", "sum"),
        Completed_Units=("Completed_Units", "sum"),
        Productive_Hours=("Productive_Hours", "sum"),
        Available_Hours=("Available_Hours", "sum"),
        Average_Quality_Score=("Quality_Score", "mean"),
        Revenue_Contribution=("Revenue_Contribution", "sum")
    ).reset_index()

    summary["Productivity_Percentage"] = (
        summary["Completed_Units"]
        / summary["Workload_Units"]
    ) * 100

    summary["Capacity_Utilization_Percentage"] = (
        summary["Productive_Hours"]
        / summary["Available_Hours"]
    ) * 100

    summary["Revenue_Per_Employee_Month"] = (
        summary["Revenue_Contribution"]
        / summary["Employee_Months"]
    )

    numeric_columns = [
        "Average_Quality_Score",
        "Revenue_Contribution",
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage",
        "Revenue_Per_Employee_Month"
    ]

    summary[numeric_columns] = (
        summary[numeric_columns].round(2)
    )

    return summary


# =====================================================
# 1. MANAGER-WISE PRODUCTIVITY ANALYSIS
# =====================================================

manager_analysis = create_productivity_summary(
    productivity,
    "Manager"
)

manager_analysis = manager_analysis.sort_values(
    by="Productivity_Percentage",
    ascending=False
)

print("\nMANAGER-WISE PRODUCTIVITY ANALYSIS")
print(manager_analysis.to_string(index=False))

manager_analysis.to_csv(
      "../output/manager_productivity_analysis.csv",
    index=False
)

print("\nManager analysis saved successfully")


# =====================================================
# 2. MONTH-WISE PRODUCTIVITY ANALYSIS
# =====================================================

monthly_analysis = create_productivity_summary(
    productivity,
    "Month_Label"
)

monthly_analysis = monthly_analysis.sort_values(
    by="Month_Label"
)

# Monthly productivity change
monthly_analysis["Productivity_Change_Percentage_Points"] = (
    monthly_analysis["Productivity_Percentage"].diff()
).round(2)

# Monthly capacity change
monthly_analysis["Capacity_Change_Percentage_Points"] = (
    monthly_analysis[
        "Capacity_Utilization_Percentage"
    ].diff()
).round(2)

# Monthly workload growth
monthly_analysis["Workload_Growth_Percentage"] = (
    monthly_analysis["Workload_Units"]
    .pct_change() * 100
).round(2)

# Monthly revenue growth
monthly_analysis["Revenue_Growth_Percentage"] = (
    monthly_analysis["Revenue_Contribution"]
    .pct_change() * 100
).round(2)

print("\nMONTH-WISE PRODUCTIVITY ANALYSIS")
print(monthly_analysis.to_string(index=False))

monthly_analysis.to_csv(
       "../output/monthly_productivity_analysis.csv",
    index=False
)

print("\nMonthly analysis saved successfully")


# =====================================================
# 3. TEAM-WISE PRODUCTIVITY ANALYSIS
# =====================================================

team_analysis = create_productivity_summary(
    productivity,
    "Team"
)

team_analysis = team_analysis.sort_values(
    by="Productivity_Percentage",
    ascending=False
)

# Productivity risk classification
team_analysis["Productivity_Risk"] = np.select(
    [
        team_analysis["Productivity_Percentage"] < 75,
        team_analysis["Productivity_Percentage"] < 85,
        team_analysis["Productivity_Percentage"] >= 85
    ],
    [
        "High Risk",
        "Medium Risk",
        "Low Risk"
    ],
    default="Review Required"
)

# Capacity status
team_analysis["Capacity_Status"] = np.select(
    [
        team_analysis[
            "Capacity_Utilization_Percentage"
        ] > 95,

        team_analysis[
            "Capacity_Utilization_Percentage"
        ] < 75
    ],
    [
        "Potential Over-Capacity",
        "Potential Under-Utilization"
    ],
    default="Normal Capacity"
)

print("\nTEAM-WISE PRODUCTIVITY ANALYSIS")
print(team_analysis.to_string(index=False))

team_analysis.to_csv(
       "../output/team_productivity_analysis.csv",
    index=False
)

print("\nTeam analysis saved successfully")


# =====================================================
# 4. DEPARTMENT MONTHLY TREND
# =====================================================

department_monthly = productivity.groupby(
    ["Department", "Month_Label"]
).agg(
    Headcount=("Employee_ID", "nunique"),
    Workload_Units=("Workload_Units", "sum"),
    Completed_Units=("Completed_Units", "sum"),
    Productive_Hours=("Productive_Hours", "sum"),
    Available_Hours=("Available_Hours", "sum"),
    Revenue_Contribution=("Revenue_Contribution", "sum")
).reset_index()

department_monthly["Productivity_Percentage"] = (
    department_monthly["Completed_Units"]
    / department_monthly["Workload_Units"]
) * 100

department_monthly["Capacity_Utilization_Percentage"] = (
    department_monthly["Productive_Hours"]
    / department_monthly["Available_Hours"]
) * 100

department_monthly[
    [
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage",
        "Revenue_Contribution"
    ]
] = department_monthly[
    [
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage",
        "Revenue_Contribution"
    ]
].round(2)

department_monthly = department_monthly.sort_values(
    by=["Department", "Month_Label"]
)

department_monthly["Headcount_Change"] = (
    department_monthly.groupby("Department")[
        "Headcount"
    ].diff()
)

department_monthly[
    "Productivity_Change_Percentage_Points"
] = (
    department_monthly.groupby("Department")[
        "Productivity_Percentage"
    ].diff()
).round(2)

department_monthly["Department_Risk_Flag"] = np.where(
    (
        department_monthly["Headcount_Change"] > 0
    )
    &
    (
        department_monthly[
            "Productivity_Change_Percentage_Points"
        ] < 0
    ),
    "Headcount Increasing - Productivity Declining",
    "No Immediate Risk"
)

print("\nDEPARTMENT MONTHLY PRODUCTIVITY TREND")
print(department_monthly.to_string(index=False))

department_monthly.to_csv(
      "../output/department_monthly_trend.csv",
    index=False
)

print("\nDepartment monthly trend saved successfully")


# =====================================================
# 5. HEADCOUNT INCREASE AND PRODUCTIVITY DECLINE RISKS
# =====================================================

department_risk = department_monthly[
    department_monthly["Department_Risk_Flag"]
    ==
    "Headcount Increasing - Productivity Declining"
].copy()

department_risk = department_risk.sort_values(
    by="Productivity_Change_Percentage_Points"
)

print(
    "\nDEPARTMENTS WHERE HEADCOUNT INCREASED "
    "BUT PRODUCTIVITY DECLINED"
)

if department_risk.empty:
    print("No department risk records identified")
else:
    print(department_risk.to_string(index=False))

department_risk.to_csv(
    "../output/headcount_increase_productivity_decline.csv",
    index=False
)

print("\nDepartment risk report saved successfully")


# =====================================================
# 6. TEAM MONTHLY TREND
# =====================================================

team_monthly = productivity.groupby(
    ["Team", "Month_Label"]
).agg(
    Headcount=("Employee_ID", "nunique"),
    Workload_Units=("Workload_Units", "sum"),
    Completed_Units=("Completed_Units", "sum"),
    Productive_Hours=("Productive_Hours", "sum"),
    Available_Hours=("Available_Hours", "sum")
).reset_index()

team_monthly["Productivity_Percentage"] = (
    team_monthly["Completed_Units"]
    / team_monthly["Workload_Units"]
) * 100

team_monthly["Capacity_Utilization_Percentage"] = (
    team_monthly["Productive_Hours"]
    / team_monthly["Available_Hours"]
) * 100

team_monthly[
    [
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage"
    ]
] = team_monthly[
    [
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage"
    ]
].round(2)

team_monthly = team_monthly.sort_values(
    by=["Team", "Month_Label"]
)

team_monthly["Monthly_Productivity_Change"] = (
    team_monthly.groupby("Team")[
        "Productivity_Percentage"
    ].diff()
).round(2)

team_monthly.to_csv(
       "../output/team_monthly_trend.csv",
    index=False
)

print("\nTeam monthly trend saved successfully")


# =====================================================
# 7. DECLINING TEAM IDENTIFICATION
# =====================================================

declining_team_records = []

for team_name, team_data in team_monthly.groupby("Team"):

    team_data = team_data.sort_values(
        by="Month_Label"
    ).copy()

    if len(team_data) >= 3:

        recent_data = team_data.tail(3)

        changes = recent_data[
            "Productivity_Percentage"
        ].diff().dropna()

        first_productivity = recent_data[
            "Productivity_Percentage"
        ].iloc[0]

        latest_productivity = recent_data[
            "Productivity_Percentage"
        ].iloc[-1]

        total_change = (
            latest_productivity - first_productivity
        )

        consistently_declining = (
            changes < 0
        ).all()

        if consistently_declining:

            declining_team_records.append({
                "Team": team_name,
                "Months_Reviewed": len(recent_data),
                "Starting_Productivity":
                    round(first_productivity, 2),
                "Latest_Productivity":
                    round(latest_productivity, 2),
                "Total_Change_Percentage_Points":
                    round(total_change, 2),
                "Risk_Level":
                    "High Productivity Risk"
            })

declining_teams = pd.DataFrame(
    declining_team_records
)

if not declining_teams.empty:

    declining_teams = declining_teams.sort_values(
        by="Total_Change_Percentage_Points"
    )

print("\nCONSISTENTLY DECLINING PRODUCTIVITY TEAMS")

if declining_teams.empty:
    print(
        "No team recorded productivity decline "
        "for three consecutive months"
    )
else:
    print(declining_teams.to_string(index=False))

declining_teams.to_csv(
       "../output/declining_productivity_teams.csv",
    index=False
)

print("\nDeclining team report saved successfully")


# =====================================================
# 8. EMPLOYEE MONTHLY PRODUCTIVITY TREND
# =====================================================

employee_monthly = productivity.groupby(
    ["Employee_ID", "Month_Label"]
).agg(
    Department=("Department", "first"),
    Team=("Team", "first"),
    Manager=("Manager", "first"),
    Workload_Units=("Workload_Units", "sum"),
    Completed_Units=("Completed_Units", "sum"),
    Productive_Hours=("Productive_Hours", "sum"),
    Available_Hours=("Available_Hours", "sum"),
    Average_Quality_Score=("Quality_Score", "mean"),
    Revenue_Contribution=("Revenue_Contribution", "sum")
).reset_index()

employee_monthly["Productivity_Percentage"] = (
    employee_monthly["Completed_Units"]
    / employee_monthly["Workload_Units"]
) * 100

employee_monthly["Capacity_Utilization_Percentage"] = (
    employee_monthly["Productive_Hours"]
    / employee_monthly["Available_Hours"]
) * 100

employee_monthly[
    [
        "Average_Quality_Score",
        "Revenue_Contribution",
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage"
    ]
] = employee_monthly[
    [
        "Average_Quality_Score",
        "Revenue_Contribution",
        "Productivity_Percentage",
        "Capacity_Utilization_Percentage"
    ]
].round(2)

employee_monthly = employee_monthly.sort_values(
    by=["Employee_ID", "Month_Label"]
)

employee_monthly["Monthly_Productivity_Change"] = (
    employee_monthly.groupby("Employee_ID")[
        "Productivity_Percentage"
    ].diff()
).round(2)

employee_monthly.to_csv(
       "../output/employee_monthly_trend.csv",
    index=False
)

print("\nEmployee monthly trend saved successfully")


# =====================================================
# 9. DECLINING EMPLOYEE IDENTIFICATION
# =====================================================

declining_employee_records = []

for employee_id, employee_data in employee_monthly.groupby(
    "Employee_ID"
):

    employee_data = employee_data.sort_values(
        by="Month_Label"
    ).copy()

    if len(employee_data) >= 3:

        recent_data = employee_data.tail(3)

        changes = recent_data[
            "Productivity_Percentage"
        ].diff().dropna()

        starting_productivity = recent_data[
            "Productivity_Percentage"
        ].iloc[0]

        latest_productivity = recent_data[
            "Productivity_Percentage"
        ].iloc[-1]

        total_change = (
            latest_productivity
            - starting_productivity
        )

        consistently_declining = (
            changes < 0
        ).all()

        if consistently_declining:

            declining_employee_records.append({
                "Employee_ID": employee_id,
                "Department":
                    recent_data["Department"].iloc[-1],
                "Team":
                    recent_data["Team"].iloc[-1],
                "Manager":
                    recent_data["Manager"].iloc[-1],
                "Starting_Productivity":
                    round(starting_productivity, 2),
                "Latest_Productivity":
                    round(latest_productivity, 2),
                "Total_Change_Percentage_Points":
                    round(total_change, 2),
                "Risk_Level":
                    "High Productivity Risk"
            })

declining_employees = pd.DataFrame(
    declining_employee_records
)

if not declining_employees.empty:

    declining_employees = declining_employees.sort_values(
        by="Total_Change_Percentage_Points"
    )

print("\nCONSISTENTLY DECLINING PRODUCTIVITY EMPLOYEES")

if declining_employees.empty:
    print(
        "No employee recorded productivity decline "
        "for three consecutive months"
    )
else:
    print(declining_employees.to_string(index=False))

declining_employees.to_csv(
     "../output/declining_productivity_employees.csv",
    index=False
)

print("\nDeclining employee report saved successfully")


# =====================================================
# COMPLETION MESSAGE
# =====================================================

print("\n=====================================================")
print("ALL PRODUCTIVITY ANALYSES COMPLETED SUCCESSFULLY")
print("=====================================================")