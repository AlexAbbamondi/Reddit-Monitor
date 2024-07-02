import praw  # Python Reddit API Wrapper
from praw.models import Submission  # Importing Submission model from PRAW
from prawcore.exceptions import RequestException  # Exception for network-related errors in PRAW
import time  # Module to handle time-related tasks
import smtplib  # SMTP protocol client for sending emails
from email.mime.multipart import MIMEMultipart  # For creating a multipart MIME email
from email.mime.text import MIMEText  # For creating text MIME part of email
from dotenv import load_dotenv  # To load environment variables from a .env file
import os  # Module for operating system related functions
from datetime import datetime, timedelta
import pytz

# Load environment variables from .env file
load_dotenv()

# Initialize the Reddit instance with credentials stored in environment variables
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),  # Get Reddit client ID
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),  # Get Reddit client secret
    user_agent=os.getenv('USER_AGENT')  # Get Reddit user agent
)

# Convert to Eastern Standard Time (EST) for display purposes
est = pytz.timezone('US/Eastern')

keywords = ['mesothelioma', 'asbestos']  # List of keywords to monitor
subreddits_to_monitor = ['all']  # Subreddit name to monitor, use 'all' for all subreddits
emails_list = os.getenv('EMAIL_RECIPIENTS')
email_recipients = emails_list.split(',')
email_sender = os.getenv('EMAIL_SENDER')  # Get the sender's email address from the environment variable
email_password = os.getenv('EMAIL_PASSWORD')  # Get the sender's email password from the environment variable

def send_email(subject, body):
    """
    Function to send an email.
    
    :param subject: Subject of the email
    :param body: Body content of the email
    """
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = ", ".join(email_recipients)  # Join the list into a comma-separated string for multiple recipients
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))  # Attach the email body as plain text
    
    server = None  # Initialize server variable
    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use appropriate SMTP server and port for Gmail
        server.starttls()  # Secure the connection with TLS
        
        # Log in to the server
        server.login(email_sender, email_password)
        
        # Send the email
        text = msg.as_string()
        server.sendmail(email_sender, email_recipients, text)
        print(f"Email sent to {', '.join(email_recipients)}")

    except smtplib.SMTPAuthenticationError as auth_error:
        print(f"Failed to send email: Authentication error - {auth_error.smtp_code} {auth_error.smtp_error}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        print(f"Email sender: {email_sender}, Email password: {'*' * len(email_password)}")
    finally:
        if server:
            # Close the connection
            server.quit()

def get_top_posts(subreddits, keywords):
    """
    Function to get the top 10 upvoted posts within the past day.
    
    :param subreddits: List of subreddits to search
    :param keywords: List of keywords to search in post titles
    """
    matching_posts = []
    try:
        for keyword in keywords:
            query = f"title:'{keyword}'"
            top_posts = reddit.subreddit('+'.join(subreddits)).search(query, sort="top", time_filter="day", limit=10)
            
            for submission in top_posts:
                # Convert post creation time to EST
                post_created_est = datetime.fromtimestamp(submission.created_utc, est).strftime('%Y-%m-%d %H:%M:%S %Z%z')
                
                post_info = f"Post Title:\n{submission.title}\n\nURL:\n{submission.url}\n\nCreated On (EST):\n{post_created_est}\n\nUpvotes: {submission.ups}\n\n---------------------------\n"
                print(post_info)
                matching_posts.append(post_info)

        if matching_posts:
            # Send all matched posts in one email
            email_body = "\n".join(matching_posts)
        else:
            # If no matching posts, send a different email
            email_body = "No posts containing the specified keywords were found in the past day."

        send_email("Daily Reddit Keyword Alerts", email_body)

    except RequestException as e:
        print(f"Network error: {e}")
        time.sleep(60)  # Wait a minute before retrying in case of network error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    # Program entry point
    print(f"Fetching top 10 upvoted posts that contain any of the keywords {keywords} in subreddits: {', '.join(subreddits_to_monitor)}")
    get_top_posts(subreddits_to_monitor, keywords)
