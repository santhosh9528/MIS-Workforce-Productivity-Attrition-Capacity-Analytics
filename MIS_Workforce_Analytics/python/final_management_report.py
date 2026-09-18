import pandas as pd
import numpy as np
from pathlib import Path


# =====================================================
# 1. FILE LOCATIONS
# =====================================================

cleaned_file = Path(
    r"C:\Users\Hooooo\Documents\Excel\MIS_Workforce_Analytics\Cleaned\MIS_Workforce_Cleaned.xlsx"
)

output_folder = Path(
    r"C:\Users\Hooooo\Documents\Excel\MIS_Workforce_Analytics\output"
)

output_folder.mkdir(parents=True, exist_ok=True)


# =====================================================
# 2. LOAD CLEANED SOURCE DATA
# =====================================================

employee_master = pd.read_excel(
    cleaned_file,
    sheet_name="Employee_Master"
)

attendance = pd.read_excel(
    cleaned_file,
    sheet_name="Attendance"
)

leave_data = pd.read_excel(
    cleaned_file,
    sheet_name="Leave"
)

overtime = pd.read_excel(
    cleaned_file,
    sheet_name="Overtime"
)

productivity = pd.read_excel(
    cleaned_file,
    sheet_name="Productivity"
)

attrition = pd.read_excel(
    cleaned_file,
    sheet_name="Attrition"
)

print("Cleaned source datasets loaded successfully")


# =====================================================
# 3. LOAD PREVIOUS ANALYSIS OUTPUTS
# =====================================================

department_risk = pd.read_csv(
    output_folder /
    "department_workforce_risk_summary.csv"
)

declining_teams = pd.read_csv(
    output_folder /
    "declining_productivity_teams.csv"
)

declining_employees = pd.read_csv(
    output_folder /
    "declining_productivity_employees.csv"
)

overtime_exceptions = pd.read_csv(
    output_folder /
    "overtime_productivity_exceptions.csv"
)

headcount_productivity_risk = pd.read_csv(
    output_folder /
    "headcount_increase_productivity_decline.csv"
)

forecast_exceptions = pd.read_csv(
    output_folder /
    "forecast_exception_report.csv"
)

department_hiring = pd.read_csv(
    output_folder /
    "department_hiring_requirement.csv"
)

monthly_hiring = pd.read_csv(
    output_folder /
    "monthly_hiring_requirement.csv"
)

monthly_productivity = pd.read_csv(
    output_folder /
    "monthly_productivity_analysis.csv"
)

print("Previous analysis outputs loaded successfully")


# =====================================================
# 4. DATE AND NUMERIC CLEANING
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

productivity["Month"] = pd.to_datetime(
    productivity["Month"],
    errors="coerce"
)

attrition["Exit_Date"] = pd.to_datetime(
    attrition["Exit_Date"],
    errors="coerce"
)


for column in [
    "Scheduled_Hours",
    "Actual_Hours",
    "Present_Flag"
]:
    attendance[column] = pd.to_numeric(
        attendance[column],
        errors="coerce"
    ).fillna(0)


for column in [
    "Workload_Units",
    "Completed_Units",
    "Productive_Hours",
    "Available_Hours",
    "Revenue_Contribution"
]:
    productivity[column] = pd.to_numeric(
        productivity[column],
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


# =====================================================
# 5. OVERALL KPI CALCULATION
# =====================================================

analysis_start = productivity["Month"].min()

analysis_end = (
    productivity["Month"].max()
    + pd.offsets.MonthEnd(0)
)


total_headcount = employee_master[
    "Employee_ID"
].nunique()


active_employees = employee_master[
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
]["Employee_ID"].nunique()


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
]["Employee_ID"].nunique()


new_joiners = employee_master[
    employee_master["Date_of_Joining"].between(
        analysis_start,
        analysis_end
    )
]["Employee_ID"].nunique()


total_exits = attrition[
    "Employee_ID"
].nunique()


average_headcount = (
    opening_headcount
    + active_employees
) / 2


attrition_percentage = (
    total_exits
    / average_headcount
) * 100 if average_headcount > 0 else 0


attendance["Absent_Flag"] = np.where(
    attendance["Present_Flag"] == 0,
    1,
    0
)

attendance["Lost_Hours"] = (
    attendance["Scheduled_Hours"]
    - attendance["Actual_Hours"]
).clip(lower=0)


absenteeism_percentage = (
    attendance["Absent_Flag"].sum()
    / len(attendance)
) * 100


hour_based_absenteeism = (
    attendance["Lost_Hours"].sum()
    / attendance["Scheduled_Hours"].sum()
) * 100


annual_leave_entitlement = 12

approved_leave_days = leave_data.loc[
    leave_data["Approval_Status"]
    .astype(str)
    .str.strip()
    .str.lower()
    ==
    "approved",
    "Leave_Days"
].sum()


available_leave_days = (
    total_headcount
    * annual_leave_entitlement
)


leave_utilization_percentage = (
    approved_leave_days
    / available_leave_days
) * 100 if available_leave_days > 0 else 0


total_overtime_hours = overtime[
    "OT_Hours"
].sum()


average_ot_per_active_employee = (
    total_overtime_hours
    / active_employees
) if active_employees > 0 else 0


total_workload = productivity[
    "Workload_Units"
].sum()

total_completed = productivity[
    "Completed_Units"
].sum()


overall_productivity = (
    total_completed
    / total_workload
) * 100 if total_workload > 0 else 0


total_productive_hours = productivity[
    "Productive_Hours"
].sum()

total_available_hours = productivity[
    "Available_Hours"
].sum()


overall_capacity_utilization = (
    total_productive_hours
    / total_available_hours
) * 100 if total_available_hours > 0 else 0


total_revenue_contribution = productivity[
    "Revenue_Contribution"
].sum()


revenue_per_employee = (
    total_revenue_contribution
    / total_headcount
) if total_headcount > 0 else 0


latest_productivity = monthly_productivity[
    "Productivity_Percentage"
].iloc[-1]

starting_productivity = monthly_productivity[
    "Productivity_Percentage"
].iloc[0]

productivity_change = (
    latest_productivity
    - starting_productivity
)


maximum_monthly_hiring = monthly_hiring[
    "Recommended_Hires"
].max()

total_forecast_shortfall = monthly_hiring[
    "Workload_Shortfall_Units"
].sum()


# =====================================================
# 6. EXECUTIVE KPI SUMMARY
# =====================================================

executive_kpi_summary = pd.DataFrame({
    "KPI": [
        "Employee Headcount",
        "Active Employees",
        "Opening Headcount",
        "New Joiners",
        "Exits",
        "Average Headcount",
        "Attrition Percentage",
        "Absenteeism Percentage",
        "Hour Based Absenteeism Percentage",
        "Approved Leave Days",
        "Available Leave Days",
        "Leave Utilization Percentage",
        "Total Overtime Hours",
        "Average OT per Active Employee",
        "Total Workload Units",
        "Completed Units",
        "Overall Productivity Percentage",
        "Overall Capacity Utilization Percentage",
        "Revenue Contribution",
        "Revenue Contribution per Employee",
        "Starting Monthly Productivity",
        "Latest Monthly Productivity",
        "Productivity Change Percentage Points",
        "Maximum Monthly Hiring Requirement",
        "Total Forecast Workload Shortfall"
    ],
    "Value": [
        total_headcount,
        active_employees,
        opening_headcount,
        new_joiners,
        total_exits,
        round(average_headcount, 2),
        round(attrition_percentage, 2),
        round(absenteeism_percentage, 2),
        round(hour_based_absenteeism, 2),
        round(approved_leave_days, 2),
        round(available_leave_days, 2),
        round(leave_utilization_percentage, 2),
        round(total_overtime_hours, 2),
        round(average_ot_per_active_employee, 2),
        round(total_workload, 2),
        round(total_completed, 2),
        round(overall_productivity, 2),
        round(overall_capacity_utilization, 2),
        round(total_revenue_contribution, 2),
        round(revenue_per_employee, 2),
        round(starting_productivity, 2),
        round(latest_productivity, 2),
        round(productivity_change, 2),
        round(maximum_monthly_hiring, 2),
        round(total_forecast_shortfall, 2)
    ]
})

print("\nEXECUTIVE KPI SUMMARY")
print(executive_kpi_summary.to_string(index=False))

executive_kpi_summary.to_csv(
    output_folder /
    "executive_kpi_summary.csv",
    index=False
)


# =====================================================
# 7. CONSOLIDATED EXCEPTION REPORT
# =====================================================

exception_records = []


# Department workforce risks
for _, row in department_risk.iterrows():

    if row["Workforce_Risk_Level"] != "Low Risk":

        exception_records.append({
            "Exception_Category":
                "Department Workforce Risk",

            "Priority":
                row["Workforce_Risk_Level"]
                .replace(" Risk", ""),

            "Department":
                row["Department"],

            "Team":
                "",

            "Employee_ID":
                "",

            "Period":
                "Historical Analysis",

            "Metric":
                "Risk Score",

            "Metric_Value":
                row["Risk_Score"],

            "Issue":
                row["Risk_Reasons"],

            "Business_Impact":
                (
                    "Workforce productivity, capacity "
                    "and retention risk"
                ),

            "Recommended_Action":
                (
                    "Review department productivity, "
                    "overtime, absenteeism and attrition"
                )
        })


# Declining team risks
for _, row in declining_teams.iterrows():

    exception_records.append({
        "Exception_Category":
            "Declining Team Productivity",

        "Priority":
            "High",

        "Department":
            "",

        "Team":
            row["Team"],

        "Employee_ID":
            "",

        "Period":
            "Recent 3 Months",

        "Metric":
            "Productivity Change",

        "Metric_Value":
            row[
                "Total_Change_Percentage_Points"
            ],

        "Issue":
            (
                "Team productivity declined "
                "for three consecutive months"
            ),

        "Business_Impact":
            (
                "Potential delivery delay and "
                "workload shortfall"
            ),

        "Recommended_Action":
            (
                "Perform team-level root-cause "
                "and manager review"
            )
    })


# Declining employee risks
for _, row in declining_employees.iterrows():

    exception_records.append({
        "Exception_Category":
            "Declining Employee Productivity",

        "Priority":
            "High",

        "Department":
            row["Department"],

        "Team":
            row["Team"],

        "Employee_ID":
            row["Employee_ID"],

        "Period":
            "Recent 3 Months",

        "Metric":
            "Productivity Change",

        "Metric_Value":
            row[
                "Total_Change_Percentage_Points"
            ],

        "Issue":
            (
                "Employee productivity declined "
                "for three consecutive months"
            ),

        "Business_Impact":
            (
                "Individual productivity and "
                "performance risk"
            ),

        "Recommended_Action":
            (
                "Provide coaching, workload review "
                "and performance support"
            )
    })


# High overtime and low productivity
for _, row in overtime_exceptions.iterrows():

    exception_records.append({
        "Exception_Category":
            "Overtime Inefficiency",

        "Priority":
            "Medium",

        "Department":
            row["Department"],

        "Team":
            row["Team"],

        "Employee_ID":
            row["Employee_ID"],

        "Period":
            row["Month_Label"],

        "Metric":
            "Overtime Hours",

        "Metric_Value":
            row["OT_Hours"],

        "Issue":
            (
                "High overtime with below-median "
                "productivity"
            ),

        "Business_Impact":
            (
                "Higher employee cost without "
                "matching productivity improvement"
            ),

        "Recommended_Action":
            (
                "Review workload allocation, process "
                "delay and overtime authorization"
            )
    })


# Headcount increase but productivity decline
for _, row in headcount_productivity_risk.iterrows():

    exception_records.append({
        "Exception_Category":
            "Headcount Productivity Mismatch",

        "Priority":
            "High",

        "Department":
            row["Department"],

        "Team":
            "",

        "Employee_ID":
            "",

        "Period":
            row["Month_Label"],

        "Metric":
            "Productivity Change",

        "Metric_Value":
            row[
                "Productivity_Change_Percentage_Points"
            ],

        "Issue":
            (
                "Headcount increased while "
                "productivity declined"
            ),

        "Business_Impact":
            (
                "Additional workforce cost without "
                "expected output improvement"
            ),

        "Recommended_Action":
            (
                "Review onboarding, training, "
                "workload and process efficiency"
            )
    })


# Forecast exceptions
for _, row in forecast_exceptions.iterrows():

    exception_records.append({
        "Exception_Category":
            "Forecast Capacity Risk",

        "Priority":
            row["Exception_Priority"],

        "Department":
            row["Department"],

        "Team":
            "",

        "Employee_ID":
            "",

        "Period":
            row["Forecast_Month"],

        "Metric":
            "Recommended Hires",

        "Metric_Value":
            row["Recommended_Hires"],

        "Issue":
            row["Exception_Reason"],

        "Business_Impact":
            (
                "Forecast workload may exceed "
                "available workforce capacity"
            ),

        "Recommended_Action":
            (
                "Improve productivity, redistribute "
                "workload and plan phased hiring"
            )
    })


consolidated_exceptions = pd.DataFrame(
    exception_records
)

priority_order = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4
}

consolidated_exceptions[
    "Priority_Order"
] = consolidated_exceptions[
    "Priority"
].map(priority_order).fillna(5)

consolidated_exceptions = (
    consolidated_exceptions.sort_values(
        by=[
            "Priority_Order",
            "Exception_Category",
            "Department",
            "Period"
        ]
    )
)

consolidated_exceptions = (
    consolidated_exceptions.drop(
        columns=["Priority_Order"]
    )
)

consolidated_exceptions.insert(
    0,
    "Exception_ID",
    [
        f"EXC-{number:04d}"
        for number in range(
            1,
            len(consolidated_exceptions) + 1
        )
    ]
)

print("\nCONSOLIDATED EXCEPTION REPORT")
print(
    "Total consolidated exceptions:",
    len(consolidated_exceptions)
)

print(
    consolidated_exceptions[
        "Priority"
    ].value_counts()
)

consolidated_exceptions.to_csv(
    output_folder /
    "consolidated_exception_report.csv",
    index=False
)


# =====================================================
# 8. MANAGEMENT RECOMMENDATIONS
# =====================================================

management_recommendations = pd.DataFrame([
    {
        "Priority": "Critical",
        "Area": "Operations",
        "Finding": (
            "Low productivity, high overtime "
            "and high attrition"
        ),
        "Recommended_Action": (
            "Conduct immediate workflow root-cause "
            "analysis and phased capacity planning"
        ),
        "Expected_Outcome": (
            "Reduce workload shortfall and "
            "operational risk"
        )
    },
    {
        "Priority": "Critical",
        "Area": "Sales",
        "Finding": (
            "Productivity declined while "
            "attrition reached a high level"
        ),
        "Recommended_Action": (
            "Review targets, employee support, "
            "training and retention drivers"
        ),
        "Expected_Outcome": (
            "Improve output and reduce employee exits"
        )
    },
    {
        "Priority": "High",
        "Area": "Technology",
        "Finding": (
            "High capacity utilization with "
            "declining productivity"
        ),
        "Recommended_Action": (
            "Review technical workload complexity, "
            "process delays and skill gaps"
        ),
        "Expected_Outcome": (
            "Convert utilized hours into "
            "higher completed output"
        )
    },
    {
        "Priority": "High",
        "Area": "Customer Support",
        "Finding": (
            "Highest absenteeism, leave utilization "
            "and overtime"
        ),
        "Recommended_Action": (
            "Review scheduling, shift coverage, "
            "leave patterns and workload allocation"
        ),
        "Expected_Outcome": (
            "Reduce employee fatigue and "
            "attendance risk"
        )
    },
    {
        "Priority": "High",
        "Area": "New Joiners",
        "Finding": (
            "New joiner productivity is below "
            "experienced employees"
        ),
        "Recommended_Action": (
            "Introduce 30, 60 and 90-day training "
            "and productivity monitoring"
        ),
        "Expected_Outcome": (
            "Reduce new-joiner productivity gap"
        )
    },
    {
        "Priority": "High",
        "Area": "Overtime",
        "Finding": (
            "High overtime has no meaningful "
            "positive productivity relationship"
        ),
        "Recommended_Action": (
            "Approve overtime using workload and "
            "productivity exception evidence"
        ),
        "Expected_Outcome": (
            "Reduce overtime cost and inefficiency"
        )
    },
    {
        "Priority": "High",
        "Area": "Hiring",
        "Finding": (
            "Forecast indicates increasing "
            "capacity pressure"
        ),
        "Recommended_Action": (
            "Use productivity recovery, workload "
            "redistribution and phased hiring"
        ),
        "Expected_Outcome": (
            "Avoid excessive immediate hiring "
            "and manage demand growth"
        )
    },
    {
        "Priority": "Medium",
        "Area": "Management Monitoring",
        "Finding": (
            "Productivity declined from January "
            "to August"
        ),
        "Recommended_Action": (
            "Track monthly department productivity, "
            "capacity, overtime and attrition"
        ),
        "Expected_Outcome": (
            "Identify risk earlier and support "
            "timely corrective action"
        )
    }
])

management_recommendations.to_csv(
    output_folder /
    "management_recommendations.csv",
    index=False
)


# =====================================================
# 9. DASHBOARD DATA DICTIONARY
# =====================================================

dashboard_data_dictionary = pd.DataFrame([
    {
        "Dashboard_Page": "Executive Overview",
        "Recommended_File": "executive_kpi_summary.csv",
        "Purpose": "Overall workforce KPI cards"
    },
    {
        "Dashboard_Page": "Productivity",
        "Recommended_File": "monthly_productivity_analysis.csv",
        "Purpose": "Monthly productivity trend"
    },
    {
        "Dashboard_Page": "Department Risk",
        "Recommended_File": "department_workforce_risk_summary.csv",
        "Purpose": "Department workforce risk matrix"
    },
    {
        "Dashboard_Page": "Attendance and Leave",
        "Recommended_File": "department_attendance_analysis.csv",
        "Purpose": "Absenteeism and attendance analysis"
    },
    {
        "Dashboard_Page": "Overtime",
        "Recommended_File": "overtime_productivity_analysis.csv",
        "Purpose": "Overtime and productivity relationship"
    },
    {
        "Dashboard_Page": "Attrition",
        "Recommended_File": "department_attrition_analysis.csv",
        "Purpose": "Department attrition comparison"
    },
    {
        "Dashboard_Page": "Capacity Forecast",
        "Recommended_File": "three_month_workforce_capacity_forecast.csv",
        "Purpose": "Three-month capacity forecast"
    },
    {
        "Dashboard_Page": "Hiring Requirement",
        "Recommended_File": "monthly_hiring_requirement.csv",
        "Purpose": "Forecast hiring requirement"
    },
    {
        "Dashboard_Page": "Exceptions",
        "Recommended_File": "consolidated_exception_report.csv",
        "Purpose": "Management exception report"
    }
])

dashboard_data_dictionary.to_csv(
    output_folder /
    "dashboard_data_dictionary.csv",
    index=False
)


# =====================================================
# 10. EXECUTIVE SUMMARY TEXT FILE
# =====================================================

critical_exceptions = len(
    consolidated_exceptions[
        consolidated_exceptions["Priority"]
        ==
        "Critical"
    ]
)

high_exceptions = len(
    consolidated_exceptions[
        consolidated_exceptions["Priority"]
        ==
        "High"
    ]
)

medium_exceptions = len(
    consolidated_exceptions[
        consolidated_exceptions["Priority"]
        ==
        "Medium"
    ]
)


executive_summary_text = f"""
WORKFORCE PRODUCTIVITY, ATTRITION AND CAPACITY PLANNING
EXECUTIVE SUMMARY

Analysis Period:
{analysis_start.strftime("%B %Y")} to {analysis_end.strftime("%B %Y")}

1. WORKFORCE OVERVIEW

Employee Headcount: {total_headcount}
Active Employees: {active_employees}
New Joiners: {new_joiners}
Employee Exits: {total_exits}
Attrition Rate: {attrition_percentage:.2f}%

2. ATTENDANCE AND LEAVE

Absenteeism Rate: {absenteeism_percentage:.2f}%
Hour-Based Absenteeism Rate: {hour_based_absenteeism:.2f}%
Approved Leave Days: {approved_leave_days:.0f}
Leave Utilization Rate: {leave_utilization_percentage:.2f}%

Leave utilization assumes an annual entitlement of
{annual_leave_entitlement} days per employee.

3. PRODUCTIVITY AND CAPACITY

Total Workload Units: {total_workload:,.0f}
Completed Units: {total_completed:,.0f}
Overall Productivity: {overall_productivity:.2f}%
Overall Capacity Utilization: {overall_capacity_utilization:.2f}%

Monthly productivity changed from
{starting_productivity:.2f}% to {latest_productivity:.2f}%,
a change of {productivity_change:.2f} percentage points.

4. OVERTIME

Total Overtime Hours: {total_overtime_hours:,.2f}
Average Overtime per Active Employee:
{average_ot_per_active_employee:.2f} hours

The analysis identified high-overtime records where
productivity remained below the median. Overtime did
not show a meaningful positive relationship with productivity.

5. WORKFORCE RISK

Operations was classified as Critical Risk due to
low productivity, high overtime and high attrition.

Sales was classified as High Risk due to declining
productivity and high attrition.

Customer Support recorded the highest absenteeism
and overtime exposure.

New joiners recorded lower productivity than
experienced employees, indicating a training and
onboarding improvement opportunity.

6. FORECAST

Maximum Monthly Hiring Requirement:
{maximum_monthly_hiring:.0f}

Total Forecast Workload Shortfall:
{total_forecast_shortfall:,.2f} units

The hiring forecast represents additional FTE-equivalent
capacity required if historical workload and productivity
trends continue. Management should first improve productivity,
redistribute workload and then use phased hiring.

7. MANAGEMENT EXCEPTIONS

Critical Exceptions: {critical_exceptions}
High Exceptions: {high_exceptions}
Medium Exceptions: {medium_exceptions}
Total Exceptions: {len(consolidated_exceptions)}

8. MANAGEMENT RECOMMENDATIONS

- Perform immediate root-cause analysis for Operations.
- Review Sales productivity, targets and retention drivers.
- Reduce overtime that does not improve completed output.
- Improve Customer Support scheduling and leave coverage.
- Introduce 30, 60 and 90-day new-joiner monitoring.
- Use phased hiring instead of immediate full hiring.
- Review productivity, capacity, absenteeism, overtime
  and attrition every month.
"""


executive_summary_path = (
    output_folder /
    "executive_summary.txt"
)

with open(
    executive_summary_path,
    "w",
    encoding="utf-8"
) as file:
    file.write(
        executive_summary_text.strip()
    )


# =====================================================
# 11. COMPLETION MESSAGE
# =====================================================

print("\n=====================================================")
print("FINAL MANAGEMENT REPORT COMPLETED SUCCESSFULLY")
print("=====================================================")

print("\nFiles created:")

print(
    output_folder /
    "executive_kpi_summary.csv"
)

print(
    output_folder /
    "consolidated_exception_report.csv"
)

print(
    output_folder /
    "management_recommendations.csv"
)

print(
    output_folder /
    "dashboard_data_dictionary.csv"
)

print(
    output_folder /
    "executive_summary.txt"
)