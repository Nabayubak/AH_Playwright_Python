import random
import string
import webbrowser


def generate_random_email(domain="yopmail.com", length=10):
    
    # Generate random username
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    # Construct email
    email = f"{username}@{domain}"
    return email

def generate_random_phone(length=10):
    # Ensure the first digit is not zero
    first_digit = str(random.randint(4, 9))
    while True:
        remaining_digits = ''.join(random.choices("456789", k=9))  # Generate a 10-digit number
        # Combine to form the phone number
        phone_number = first_digit + remaining_digits
        if len(phone_number) == 10 and phone_number.isdigit():
            return phone_number


def generate_unique_fullname():
    
    first_name = ''.join(random.choices(string.ascii_lowercase, k=5))
    last_name = ''.join(random.choices(string.ascii_lowercase, k=7))
    return f"{first_name} {last_name}"

def generate_random_word_with_inc(length=8):

    # Generate a random word of the specified length
    random_word = ''.join(random.choices(string.ascii_letters, k=length)).capitalize()
    # Append "Inc"
    word_with_inc = f"{random_word} Inc"
    return word_with_inc


def choose_browser() -> str:
    """Prompts user for browser choice and returns the selected browser."""
    print("Please choose a browser:")
    print("1: Chrome")
    print("2: Firefox")
    print("3: Safari")
    print("4: Edge")
    
    choice = input("Enter the number of your choice: ")
    
    browser_map = {
        "1": "chrome",
        "2": "firefox",
        "3": "safari",
        "4": "edge"
    }
    
    return browser_map.get(choice, "chrome")  # Default to chrome


