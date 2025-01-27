import logging

# Configure the logger
logging.basicConfig(
    filename="src/system.log", #Log file path
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s", # Log format
)

def log_action(action, username):
    """
    Logs a user action.
    Args:
        action(str): The action performed by the user.
        username (str): The username of the user performing the action.
    """
    logging.info(f"User '{username}' performed action {action}")

def log_security_event(event, username=None):

    if username:
        logging.warning(f"SECURITY ALERT: {event} detected for user '{username}'")
    else:
        logging.warning(f"SECURITY ALERT: {event}")

def log_error(error, username=None):
    """
    Logs an error in the system.
    Args:
        error (str): The error message.
        username (str, optional): The username involved in the error (if applicable).
    """
    if username:
        logging.error(f"ERROR: {error} for user '{username}'")
    else:
        logging.error(f"ERROR: {error}")
