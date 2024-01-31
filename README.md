# Reddit Top Users Analyzer

## Overview

This script is designed to interact with the Reddit API to collect and analyze user activity on a specified subreddit. It parses posts and comments from the last 3 days, then identifies and displays the top users based on the number of posts and comments they have made.

## Getting Started

Follow these steps to set up and run the script:

### Prerequisites

- Python 3.11
- Docker
- Reddit API credentials (client ID, client secret, username, password, and user agent)

### Installation

1. Clone this repository:

    ```
    git clone https://github.com/dukhovichanna/reddit_api.git
    cd reddit_api
    ```

2. Create a `.env` file in the project root and fill in your Reddit API credentials:

    ```
    CLIENT_ID=<your-client-id>
    CLIENT_SECRET=<your-client-secret>
    USERNAME=<your-username>
    PASSWORD=<your-password>
    USER_AGENT=<your-user-agent>
    TIMEOUT=<your-timeout>
    ```

### Usage

1. Build the Docker image:

    ```
    docker-compose build
    ```

2. Run the script using Docker:

    ```
    docker-compose up
    ```

## Customization

You can customize the script for different subreddits by modifying the `subreddit_name` variable in the `main()` function.

```
subreddit_name = 'books'
```

## Output

The script outputs the top users who have made the most posts and the top users who have written the most comments on the specified subreddit.

```
Top Posters: [('user1', 10), ('user2', 8), ('user3', 1)]
Top Commenters: [('user4', 15), ('user5', 12), ('user6', 10)]
```

## License

This project is licensed under the MIT License.
