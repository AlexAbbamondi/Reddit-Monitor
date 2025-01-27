# Reddit Keyword Alert System

This Python script monitors Reddit for posts containing specified keywords and sends email notifications with details of the posts found.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Features

- Monitors Reddit posts in real-time for specific keywords.
- Notifies via email about the top upvoted posts within the past day.
- Converts post timestamps to Eastern Standard Time (EST).

## Prerequisites

- Python 3.x
- Packages: `praw`, `python-dotenv`, `pytz`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/reddit-keyword-alert.git
    cd reddit-keyword-alert
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the root directory of your project with the following variables:

```plaintext
REDDIT_CLIENT_ID=<your_reddit_client_id>
REDDIT_CLIENT_SECRET=<your_reddit_client_secret>
USER_AGENT=<your_user_agent>
EMAIL_SENDER=<your_email>
EMAIL_PASSWORD=<your_email_password>
EMAIL_RECIPIENTS=<email1,email2,...>
```

- Replace placeholders with actual values:
  - `<your_reddit_client_id>`: Your Reddit API client ID.
  - `<your_reddit_client_secret>`: Your Reddit API client secret.
  - `<your_user_agent>`: A user agent string for your application.
  - `<your_email>` and `<your_email_password>`: The email address and password used for sending emails.
  - `<email1,email2,...>`: Comma-separated list of email recipients.

## Usage

Run the script using the command:

```bash
python reddit_keyword_alert.py
```

The script will automatically start monitoring Reddit and send daily alerts based on the specified keywords.

## How It Works

- **Keyword Monitoring**: Searches Reddit for posts with specified keywords (`mesothelioma`, `asbestos`) across all subreddits.
- **Email Notifications**: Sends an email with details of each matching post.
- **Timezone Conversion**: Converts the post creation time to EST for better understanding.

## Error Handling

- Handles network-related errors by retrying after a delay.
- Informs users of any issues encountered during email sending, such as authentication errors.

## Contributing

Contributions are welcome! Please fork the repository and make changes as you wish. Pull requests are warmly welcomed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Enjoy streamlined Reddit monitoring! If you have questions or suggestions, feel free to open an issue or contact me directly.
