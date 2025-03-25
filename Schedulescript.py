Name: Run Automation Script
on:
  schedule:
    - cron: '0 14 * * *'
  # Optional: Add workflow_dispatch to allow manual triggers
  workflow_dispatch:

jobs:
  run-script:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4  # Updated to latest version

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'  # Specify your Python version (3.8, 3.10, etc.)

      - Name: Cache Python dependencies
        use: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hash files('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Run script
        run: python run_tests.py  # Make sure this filename matches your actual script
