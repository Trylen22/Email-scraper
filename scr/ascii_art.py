def get_cat_art():
    """
    Returns the ASCII art of a cat as a string.
    """
    return r"""
        /\_/\  
       ( o.o ) 
        > ^ <
    """

def display_welcome_message():
    """
    Displays the ASCII art of the cat and a welcome message for the system.
    """
    print(get_cat_art())
    print("Welcome to Email Scraper 2.0")
    print("Fetching and summarizing your emails, pawsitively!")
    print("-" * 50)

def goodbye_message():
    """
    Displays a goodbye message with the ASCII art of the cat.
    """
    print(get_cat_art())
    print("Thank you for using Email Scraper 2.0!")
    print("Have a purr-fect day!")
    print("-" * 50)

def show_progress_bar(total_steps, task):
    """
    Displays a progress bar with a given number of steps and task description.

    Args:
        total_steps (int): Total number of steps in the progress bar.
        task (str): Description of the current task.
    """
    from tqdm import tqdm
    print(task)
    for _ in tqdm(range(total_steps)):
        pass
