name: Run Automation Script
on:
  schedule:
    - cron: '0 14 * * *'
jobs:
  run-script:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run script
        run: python run_tests.py # Adjust for your script
