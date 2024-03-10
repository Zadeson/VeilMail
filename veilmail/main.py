from datetime import datetime
import requests
import random
import time
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from pyfiglet import Figlet
from rich import box
from yaspin import yaspin
from yaspin.spinners import Spinners
from alive_progress import alive_bar
import pyperclip
import questionary
import html2text

def paginate_inbox(inbox, page, items_per_page=10):
    """
    Paginates the inbox list and returns a sublist containing the items for the specified page.

    Args:
        inbox (list): The list of items in the inbox.
        page (int): The page number to retrieve.
        items_per_page (int, optional): The number of items to display per page. Defaults to 10.

    Returns:
        list: A sublist containing the items for the specified page.
    """
    start = (page - 1) * items_per_page
    end = start + items_per_page
    return inbox[start:end]

console = Console()

def fetch_active_domains():
    """
    Fetches the list of active domains from the 1secmail API.

    Returns:
        list: A list of active domains.

    Raises:
        requests.RequestException: If there is an error while fetching the active domains.
    """
    try:
        api_url = "https://www.1secmail.com/api/v1/?action=getDomainList"
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        console.print(f"[bold red]Error fetching active domains:[/bold red] {e}")
        return ['com', 'net', 'org']

def generate_domain():
    """
    Generates a random domain from the list of active domains.

    Returns:
        str: A randomly selected active domain.
    """
    active_domains = fetch_active_domains()
    return random.choice(active_domains)

def create_email(custom_username=None):
    """
    Generates a random email address and copies it to the clipboard.
    Optionally accepts a custom domain.

    Args:
        custom_domain (str, optional): A custom domain provided by the user.

    Returns:
        str: The generated email address.
    """
    username = custom_username if custom_username else ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=10))
    # List of predefined domains
    predefined_domains = ["1secmail.com", "1secmail.org", "1secmail.net", "icznn.com", "ezztt.com", "vjuum.com", "laafd.com", "txcct.com"]
    domain = random.choice(predefined_domains)
    email_address = f"{username}@{domain}"
    pyperclip.copy(email_address)
    return email_address

def check_inbox(email):
    """
    Retrieves the messages from the inbox of the specified email address.

    Args:
        email (str): The email address to check the inbox for.

    Returns:
        dict: A dictionary containing the response from the API call, which includes the messages in the inbox.

    Raises:
        requests.RequestException: If there is an error while making the API request.

    """
    try:
        username, domain = email.split('@')
        api_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return None

def fetch_email_content(email, id):
    """
    Fetches the content of an email from a given email address and message ID.

    Args:
        email (str): The email address to fetch the email from.
        id (str): The ID of the email message to fetch.

    Returns:
        dict: The JSON response containing the email content.

    Raises:
        requests.RequestException: If there is an error while making the API request.
    """
    try:
        username, domain = email.split('@')
        api_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={id}"
        response = requests.get(api_url)
        response.raise_for_status()
        email_data = response.json()

        # Check if the email is HTML and convert it
        if email_data.get('htmlBody'):
            h = html2text.HTML2Text()
            h.ignore_links = True
            email_data['textBody'] = h.handle(email_data['htmlBody'])
        
        return email_data
    except requests.RequestException as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return None


def print_inbox(email, inbox, app_name):
    """
    Prints the inbox for a given email address.

    Args:
        email (str): The email address.
        inbox (list): A list of dictionaries representing the inbox messages.
    """
    console.clear()
    f = Figlet(font='ANSI_shadow')
    rendered_text = f.renderText(app_name)
    header_text = Text(rendered_text, style="bold gray")

    console.print(header_text)

    header = ("[bold gray]" + "-"*25 + f"| Inbox {email} |" + "-"*25 + "[/bold gray]\n")
    console.print(header)
    console.print("Command Options: view <no>, refresh, quit\n")
    if len(inbox) == 0:
        console.print("[bold red]Inbox is empty.[/bold red]")
    else:
        for i, message in enumerate(inbox):
            console.print(f"[bold green]{i}[/bold green] - {message['from']} - {message['subject']} - {message['date']}\n")
    header_length = len("-"*25 + f"| Inbox {email} |" + "-"*25)
    console.print("[bold gray]" + "-" * header_length + "[/bold gray]")

def print_email(message, email, message_id, app_name):
    """
    Prints the details of an email.

    Args:
        message (dict): A dictionary containing the email message details.
        email (str): The email address of the recipient.
        message_id (int): The ID of the email message.
    """
    console.clear()
    
    f = Figlet(font='ANSI_shadow')
    rendered_text = f.renderText(app_name)
    header_text = Text(rendered_text, style="bold gray")

    console.print(header_text)

    header = ("[bold gray]" + "-"*25 + f"| {email} - viewing email {message_id} |" + "-"*25 + "[/bold gray]\n")
    console.print(header)
    console.print("From: " + "[bold green]" + message['from'] + "[/bold green]")
    console.print("Subject: " + "[bold yellow]" + message['subject'] + "[/bold yellow]")
    console.print("Date: " + "[bold magenta]" + message['date'] + "[/bold magenta]\n")
    header_length = len(header)
    console.print("-" * header_length)
    console.print(message['textBody'], justify="left")
    console.print("-" * header_length)
    console.printconsole.print("[bold gray]" + "-" * header_length + "[/bold gray]")
    questionary.confirm("Return to Inbox?").ask()

def main():
    """
    Entry point of the VeilMail program.
    """
    # Application Information
    app_name = "VeilMail"
    app_version = "1.0.9" # Semantic Versioning: MAJOR.MINOR.PATCH
    description = "A simple command-line email client to view temporary emails using the 1secmail API."
    console = Console()
    console.clear()
    
    # Render App Name with ASCII Art
    f = Figlet(font='ANSI_shadow')
    rendered_text = f.renderText(app_name)

    # Prepare the header text
    header_text = Text(rendered_text, style="bold gray")
    version_text = Text(f"Version: {app_version}\n", style="bold green")
    description_text = Text(description + "\n", style="italic")
    
    # Display the Header
    console.print(header_text)
    console.print(version_text)
    console.print(description_text)
    console.print("-" * 80 + "\n")

    custom_username = questionary.text("Enter a custom username or press enter for a random one:").ask().strip()

    email = create_email(custom_username if custom_username else None)

    console.print(f"\nYour temporary email is [bold green]{email}[/bold green] - Email address copied to clipboard.\n")
    questionary.confirm("Ready?").ask()

    inbox = check_inbox(email)
    page = 1
    while True:
        inbox = check_inbox(email)
        paginated_inbox = paginate_inbox(inbox, page)
        print_inbox(email, paginated_inbox, app_name)
        command = questionary.text("").ask()
        if command == "quit":
            if questionary.confirm("Are you sure? Your temporary email will be lost.").ask():
                exit()
        elif command == "refresh":
            inbox = check_inbox(email)
            continue
        elif command.startswith("view"):
            parts = command.split()
            if len(parts) == 2 and parts[1].isdigit():
                message_id = int(parts[1])
                if 0 <= message_id < len(inbox):
                    message = fetch_email_content(email, inbox[message_id]['id'])
                    print_email(message, email, inbox[message_id]['id'], app_name)
                else:
                    console.print(f"No message with ID {message_id}. Please try again.")
                    time.sleep(1)
                    continue
            else:
                console.print("Invalid command format. Use 'view <number>'.")
                time.sleep(1)
                continue
        else:
            console.print("Invalid command. Please try again.")
            time.sleep(1)
            continue



if __name__ == "__main__":
    main()
