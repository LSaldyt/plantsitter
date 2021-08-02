# Plantsitter

A smart monitor for your plants, in pure Python.  

`git clone https://github.com/LSaldyt/plantsitter`

Install Python [`3.9`](https://www.python.org/).  
Install Python packages using poetry:  
`pip3 install poetry`  
`cd plantsitter`  
`poetry update`  

Install [InfluxDB](https://www.influxdata.com/) & set it to run as a service. The default setup uses a database called `plants` and the default port `8086`.
Optionally, create [Twilio](https://www.twilio.com) and [Google](https://developers.google.com/gmail/api/quickstart/python) accounts, noting tokens, ids, and passwords.  

Copy the config file, and fill in information from above (such as IP addresses, ports, phone numbers, passwords, emails, etc). Do not commit this file to github or share it with anyone. Ideally, change the permissions of the file as well.  
`cp config.json.sample config.json`  
It is also necessary to move Google's `credentials.json` and `token.json` into the same directory (if being used).  
At time of writing, it is recommended to keep as many default settings as possible, since it is possible there are places that don't load the config file. Importantly, the `plantsitter_ip` needs to be the same IP as the Raspberry Pi.  


Repeat for both the Raspberry Pi (sitter) and dashboard (i.e. a laptop, desktop, or dedicated server).


To scrape plant data using `selenium`, it is necessary to install Google Chrome, and to have the [chromedriver](https://chromedriver.chromium.org/downloads) binary on the path.
The latest tested version was `92`.  
For example, it is easiest to copy `chromedriver` to `/usr/local/bin/chromedriver`, and install chrome via a system package manager like `apt` or `pacman`.  
This is only necessary for the dashboard.  

To start the sitter: `cd sitter && ./run`  
To start the dashboard: `cd dashboard && ./run`  

