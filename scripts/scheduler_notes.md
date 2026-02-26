# Daily Automation Scheduling

## macOS / Linux (cron)

1. Run: crontab -e
2. Add:

0 7 * * * /usr/bin/python3 /path/to/financial_intelligence_system/scripts/run_local.py

## Windows Task Scheduler

- Create Basic Task
- Trigger: Daily
- Action: Start a Program
- Program: python.exe
- Arguments: scripts/run_local.py
