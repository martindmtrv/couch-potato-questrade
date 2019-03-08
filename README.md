# couch-potato-questrade
Portfolio Balancer for the Questrade online brokerage

This nifty little program will calculate the quantity of shares you need to buy and sell to reach your target asset allocation for your Questrade self-directed investment account! IMPORTANT NOTE: this program does not make any trades on your behalf, it is simply a glorified calculator for your investments!

# Authentication

This Python app uses OAuth2 authentication to access real-time/delayed market data from Questrade and your current portfolio allocation!

Simply run main.py, and your default browser will open to a Questrade API login page where you will login with your Questrade account. You will be redirected to the landing page where you must click a button to copy your authentication code to your clipboard. Paste this into the terminal and away you go!

# Account selection

If you have multiple accounts with Questrade; no problem! Once authenticated you will be able to select which account you want to use the calculator for!

# Balancing

This program aims to make rebalancing a bit easier! You can set a target asset allocation amongst your current holdings from the main menu! Whatever is leftover from 100% allocation will be assigned to cash allocation.

# Development

I'm looking at different platforms for this program to develop it as maybe a web app or an Android app; anything to take it out of the command line right?


