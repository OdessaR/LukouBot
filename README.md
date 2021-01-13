# Lukou bot

This is a bot automatically scrapping group purchasing information from [Lukou](http://www.lukou.com/), a shopping experiencing sharing platform

The collected posts are updated on [this account](http://www.lukou.com/user/201324) on a daily basis, with 1626 followers by 2021 Jan. 12th 

## How to run the script

To run the script locally, you need to install *selenium*. This could be done with `pip3 install selenium`

Please also check if you already installed [ChromeDriver](https://chromedriver.chromium.org/downloads) for selenium to work on

- `main.py` will check all the posted group purchasing listed in the "Group purchase" tab and filter out posts created within three days (running date to 2 days before). Then check whether they have already been posted. The final result is written out in the format of `result_mmdd.csv`

- `post_bot.py` would perform the posting work. This script will automatically post the result from today, then send a message to the connected telegram account. Lukou username and password need to be filled in for the posting function, and the telegram token needs to be filled in for the messaging function.

- `main.sh` is used to create an auto-running script for both function scrips with running logs.
