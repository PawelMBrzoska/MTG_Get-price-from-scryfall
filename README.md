# MTG_Get-price-from-scryfall
Simple script to scrap prices using Scryfall API. Input database is from MTGStock.

# Getting started

## Packages

First of all you need pandas for data processing. Easiest way is going for pip install.

> pip install pandas

Furthermore, I used urllib, requests and JSON.

# Running app

The script needs inventory file to operate. It search for cards using Scryfall API and saves the version and prices in that file.

# Changelog

- 1.0 Working app
- 1.1 Better sets management 
- 1.2 Upgrade of engine (choosing the set and tracking price history)