# Workforce Productivity, Attrition & Capacity Planning Analytics

An end-to-end Workforce Analytics and Management Information System (MIS) project developed using Excel, Python, Pandas, Power BI and DAX.

The solution evaluates workforce productivity, attendance, overtime, attrition, employee capacity and hiring requirements from January 2026 to August 2026. It also provides a three-month workforce capacity forecast for September–November 2026.

## Business Objective

The objective of this project is to determine whether the organization has the right workforce capacity and identify productivity, employee-retention and operational risks.

The analysis includes:

- Employee headcount and active employees
- New joiners and employee exits
- Attrition analysis
- Attendance and absenteeism analysis
- Leave utilization analysis
- Overtime analysis
- Employee productivity analysis
- Revenue contribution per employee
- Workforce capacity utilization
- Department, location and designation analysis
- Manager and team performance analysis
- Employee experience analysis
- Declining employee and team productivity
- Overtime and productivity relationship
- Department-level workforce risk
- Hiring requirement estimation
- Three-month workforce capacity forecast
- Management exception reporting

## Tools and Technologies

- Microsoft Excel
- Python
- Pandas
- NumPy
- Power BI
- Power Query
- DAX
- Git
- GitHub

## Dataset

The project integrates the following workforce datasets:

- Employee Master
- Attendance
- Leave
- Overtime
- Productivity
- Performance
- Hiring
- Attrition

All major KPIs can be traced back to the underlying employee-level or transaction-level data.

## Data Cleaning and Validation

The source datasets were cleaned and validated using Excel and Python.

The validation process included:

- Missing-value identification
- Duplicate-record detection
- Invalid date correction
- Negative-value detection
- Employee ID validation
- Foreign-key reconciliation
- Employee status validation
- Attendance reconciliation
- Leave-data validation
- Overtime validation
- Productivity-data validation
- Performance-period validation
- Hiring and attrition reconciliation
- Exception identification

## Executive KPI Summary

| KPI | Result |
|---|---:|
| Total Employees | 80 |
| Active Employees | 72 |
| Opening Headcount | 68 |
| New Joiners | 12 |
| Employee Exits | 8 |
| Average Headcount | 70 |
| Attrition Rate | 11.43% |
| Absenteeism Rate | 3.97% |
| Hour-Based Absenteeism Rate | 6.37% |
| Approved Leave Days | 453 |
| Available Leave Days | 960 |
| Leave Utilization Rate | 47.19% |
| Total Overtime Hours | 3,727.64 |
| Average Overtime per Active Employee | 51.77 hours |
| Total Workload Units | 65,248 |
| Completed Units | 54,999 |
| Overall Productivity | 84.29% |
| Capacity Utilization | 87.28% |
| Revenue Contribution | 2,277,417.31 |
| Revenue Contribution per Employee | 28,467.72 |
| Maximum Monthly Hiring Requirement | 63 |
| Forecast Workload Shortfall | 10,278.37 units |

## Productivity Analysis

Productivity was analyzed across multiple workforce dimensions:

- Department
- Location
- Designation
- Experience group
- Manager
- Team
- Employee
- Month

Monthly productivity declined from 91.20% in January 2026 to 78.10% in August 2026.

This represents a decrease of 13.10 percentage points.

Departments with notable productivity risks included:

- Operations
- Technology
- Sales

The analysis also identified employees and teams with consistently declining productivity.

## Attendance and Absenteeism Analysis

The overall employee absenteeism rate was 3.97%.

The hour-based absenteeism rate was 6.37%.

Customer Support recorded the highest absenteeism exposure among the departments.

Attendance analysis was performed at:

- Department level
- Monthly level
- Employee level

## Leave Utilization Analysis

The analysis identified:

- 453 approved leave days
- 960 available leave days
- 47.19% overall leave utilization

The available leave calculation uses an annual entitlement of 18 days per employee, prorated to 12 days for the January–August analysis period.

Leave utilization was analyzed by department and leave type.

## Overtime Analysis

The organization recorded 3,727.64 total overtime hours.

Customer Support recorded the highest overtime exposure, followed by Operations and Technology.

The relationship between overtime and productivity was weak and negative.

This indicates that additional overtime did not consistently result in higher productivity.

The analysis also identified high-overtime and low-productivity exceptions for management review.

## Attrition Analysis

The organization recorded:

- 8 total employee exits
- 11.43% overall attrition rate

Departments with notable attrition risk included:

- Marketing
- Sales
- Operations
- Quality

Marketing recorded the highest departmental attrition percentage. However, this result should be interpreted together with its smaller department headcount.

Sales recorded a 25% attrition rate and declining productivity.

## Experience-Based Productivity

Employees with 0–1 year of experience recorded:

- Productivity: 74.98%
- Capacity Utilization: 79.13%

Employees with more than one year of experience recorded:

- Productivity: 86.19%
- Capacity Utilization: 88.90%

The result indicates a potential training and onboarding improvement opportunity for less-experienced employees.

## Workforce Risk Analysis

Operations was classified as a critical-risk department due to:

- Low productivity
- High overtime
- High attrition

Sales was classified as high risk because of:

- Declining productivity
- High attrition

Technology recorded low productivity despite high capacity utilization.

Customer Support recorded:

- High absenteeism
- High overtime exposure

## Three-Month Workforce Forecast

The workforce forecast covers:

- September 2026
- October 2026
- November 2026

| Forecast Month | Current Headcount | Required Headcount | Recommended Hires | Workload Shortfall |
|---|---:|---:|---:|---:|
| September 2026 | 72 | 115 | 43 | 2,983.06 |
| October 2026 | 72 | 123 | 51 | 3,426.12 |
| November 2026 | 72 | 135 | 63 | 3,869.19 |

The maximum monthly hiring requirement was 63 FTE-equivalent employees.

The total forecast workload shortfall was 10,278.37 units.

The forecast represents additional FTE-equivalent capacity required if historical workload and productivity trends continue.

Management should first improve productivity, redistribute workload and then use phased hiring based on operational priorities.

## Department Hiring Requirement

| Department | Current Headcount | Maximum Required Headcount | Maximum Recommended Hires |
|---|---:|---:|---:|
| Operations | 15 | 37 | 22 |
| Sales | 12 | 28 | 16 |
| Technology | 11 | 23 | 12 |
| Customer Support | 16 | 22 | 6 |
| Quality | 7 | 10 | 3 |
| HR | 6 | 8 | 2 |
| Marketing | 2 | 3 | 1 |
| Finance | 3 | 4 | 1 |

## Management Exception Report

The consolidated exception report identified 154 management exceptions.

| Priority | Number of Exceptions |
|---|---:|
| Critical | 17 |
| High | 45 |
| Medium | 92 |
| Total | 154 |

Each exception contains:

- Exception category
- Priority
- Department
- Team
- Employee ID
- Analysis period
- Metric
- Metric value
- Identified issue
- Business impact
- Recommended action

## Key Findings

- Monthly productivity declined by 13.10 percentage points.
- Operations was classified as a critical-risk department.
- Sales recorded declining productivity and a 25% attrition rate.
- Customer Support recorded the highest absenteeism and overtime exposure.
- Overtime did not show a meaningful positive relationship with productivity.
- Employees with 0–1 year of experience recorded lower productivity than employees with more than one year of experience.
- All eight departments were forecast to face workforce capacity pressure.
- Operations recorded the highest forecast hiring requirement.
- The maximum monthly hiring requirement was 63 FTE-equivalent employees.
- A total of 154 management exceptions were identified.

## Management Recommendations

1. Perform an immediate root-cause analysis of Operations productivity and workload allocation.
2. Review Sales targets, productivity barriers and employee-retention drivers.
3. Reduce overtime that does not result in higher completed output.
4. Improve Customer Support scheduling and leave coverage.
5. Introduce structured 30-, 60- and 90-day monitoring for new joiners.
6. Provide additional training and coaching for less-experienced employees.
7. Redistribute workload before approving additional hiring.
8. Use phased hiring based on department priority.
9. Review critical and high-priority management exceptions every month.
10. Monitor productivity, capacity, absenteeism, overtime and attrition regularly.

## Power BI Dashboard

The Power BI report contains six interactive dashboard pages:

1. Executive Overview
2. Productivity Analysis
3. Attendance & Overtime
4. Attrition Analysis
5. Capacity & Hiring Forecast
6. Management Exceptions

### Executive Overview

![Executive Overview](./Power%20Bi/Dashboards%20screenshot/Executive%20Overview.png)

### Productivity Analysis

![Productivity Analysis](./Power%20Bi/Dashboards%20screenshot/Productivity%20Analysis.png)

### Attendance & Overtime

![Attendance and Overtime](./Power%20Bi/Dashboards%20screenshot/Attendance%20%26%20Overtime.png)

### Attrition Analysis

![Attrition Analysis](./Power%20Bi/Dashboards%20screenshot/Attrition%20Analysis.png)

### Capacity & Hiring Forecast

![Capacity and Hiring Forecast](./Power%20Bi/Dashboards%20screenshot/Capacity%20%26%20Hiring%20Forecast.png)

### Management Exceptions

![Management Exceptions](./Power%20Bi/Dashboards%20screenshot/Management%20Exceptions.png)

## Project Structure

```text
MIS_Workforce_Analytics/
│
├── Dataset/
│   └── MIS_Workforce_Productivity_Attrition_Capacity_Dataset.xlsx
│
├── Cleaned/
│   └── MIS_Workforce_Cleaned.xlsx
│
├── Analysis/
│   └── MIS_Workforce_KPI_Calculations.xlsx
│
├── Python/
│   ├── cleaning.py
│   ├── kpi_calculation.py
│   ├── productivity_analysis.py
│   ├── workforce_risk_analysis.py
│   ├── workforce_forecast.py
│   └── final_management_report.py
│
├── Power Bi/
│   ├── Dashboards.pbix
│   └── Dashboards screenshot/
│       ├── Attendance & Overtime.png
│       ├── Attrition Analysis.png
│       ├── Capacity & Hiring Forecast.png
│       ├── Executive Overview.png
│       ├── Management Exceptions.png
│       └── Productivity Analysis.png
│
├── Calculation Sheet/
│   └── executive_kpi_summary.csv
│
├── Reconciliation Report/
│   └── Reconciliation_Report.xlsx
│
├── Exception Report/
│   └── consolidated_exception_report.csv
│
├── Executive Summary/
│   └── executive_summary.txt
│
├── Findings & Recommendations/
│   └── management_recommendations.csv
│
├── Workforce Forecast/
│   └── three_month_workforce_capacity_forecast.csv
│
├── output/
│   └── Generated analysis files
│
└── README.md
```

## Python Workflow

Run the Python scripts from the `Python` folder in the following order:

```powershell
py cleaning.py
py kpi_calculation.py
py productivity_analysis.py
py workforce_risk_analysis.py
py workforce_forecast.py
py final_management_report.py
```

The scripts perform the following activities:

1. Clean and validate the source datasets.
2. Generate reconciliation and data-quality reports.
3. Calculate workforce KPIs.
4. Analyze productivity across multiple workforce dimensions.
5. Analyze attendance, leave, overtime and attrition risks.
6. Identify declining employee and team productivity.
7. Generate a three-month capacity and hiring forecast.
8. Generate the consolidated exception report.
9. Create the final executive summary and management recommendations.

## Final Deliverables

- Cleaned workforce dataset
- KPI calculation workbook
- Reconciliation report
- Six-page Power BI dashboard
- Three-month workforce capacity forecast
- Consolidated management exception report
- Executive summary
- Key findings and management recommendations
- Reproducible Python scripts
- Dashboard screenshots

## Business Value

This project enables management to:

- Monitor workforce performance through traceable KPIs
- Identify departments with productivity and retention risks
- Understand whether overtime improves output
- Detect workforce capacity problems
- Estimate future hiring requirements
- Prioritize high-impact management exceptions
- Make data-driven workforce planning decisions

## Author

**Santhosh Kumar M**  
Data Analyst Intern  
Bengaluru, India

**GitHub Portfolio:** [github.com/santhosh9528](https://github.com/santhosh9528)

## Disclaimer

This project uses a simulated workforce dataset created for analytics practice and portfolio demonstration.

The results do not represent confidential information from a real organization.
