name: Run Automation Script
on:
  schedule:
    - cron: '30 13 * * *' # Runs at 13:30 UTC (1:30 PM UTC) daily
jobs:
  run-script:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run script
        run: python run_tests.py # Adjust for your script
