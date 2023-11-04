# Telegram tracker
![Static Badge](https://img.shields.io/badge/version-2-blue)
![Static Badge](https://img.shields.io/badge/python-3.10-orange)

Track changes in public Telegram user data, like profiles, stories or online status

## Installation

Clone the repo from GitHub and install libraries:

``` bash
git clone https://github.com/ArtemiiKravchuk/vime-telegram-tracker.git
pip install -r requirements.txt
```

## Configuration

Change `config.json` according to your needs.

You have to fill in the `telegram => api_id` and `telegram => api_hash` fields with values from https://my.telegram.org

In `targets => users` field, put a list of users to track. You can use integer id (the user should be in your contacts) or string username (the user doesn't have to be in your contacts)

Program will save all the data in the desired format. You can change this in `output` filed of config: there should be a list of all locations to ouput data to.

As an example, program will save both to sqlite database and csv files, but you can remove unncesessary location.
