import pytest



# List of browsers to run tests in
browsers = ["chromium", "firefox", "webkit"]

# Define the test directory where all test scripts are located
test_directory = "pages"  # Change this if your test scripts are in another folder

# Run all tests in the 'pages' folder and generate an HTML report
pytest.main([
    test_directory,         # Run all tests inside the 'pages' directory
    "--html=report.html",   # Generate an HTML report
    "--self-contained-html" # Ensure the report is self-contained
])



