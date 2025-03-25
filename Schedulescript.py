name: Run Automation Script

on:
  schedule:
    - cron: '0 14 * * *' # Runs at 14:00 UTC (2:00 PM UTC) daily

jobs:
  run-script:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python (optional, if Python script)
      uses: actions/setup-python@v4
      with:
        python-version: '3.x' # Adjust if needed
    - name: Run script
      run: python run_tests.py # Replace with your script command
