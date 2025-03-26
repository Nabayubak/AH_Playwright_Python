import pytest

<<<<<<< HEAD
=======

>>>>>>> 6ca92e872e9d09732526af8506ba4aaef316b240
# List of browsers to run tests in
browsers = ["chromium", "firefox", "webkit"]

# Define the test directory where all test scripts are located
test_directory = "pages"  # Change this if your test scripts are in another folder

# Check if we have additional arguments passed in, such as from GitHub Actions or CLI
args = sys.argv[1:]  # Get any arguments passed to the script

# If no arguments passed, set the default ones
if not args:
    args = [
        test_directory,           # Run all tests inside the 'pages' directory
        "--html=report.html",     # Generate an HTML report
        "--self-contained-html"   # Ensure the report is self-contained
    ]

# Run pytest with the given arguments
pytest.main(args)
