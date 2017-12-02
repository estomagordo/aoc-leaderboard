#!/usr/bin/env python

'''
This script will grab the leaderboard from Advent of Code and post it to Slack

Kodsnack modified version in swedish

Original here: https://github.com/tomswartz07/AdventOfCodeLeaderboard

'''

import json, requests

# see README for directions on how to fill these variables
# HARDCODED TO KODSNACK BOARD FOR NOW!
LEADERBOARD_ID = "194162"
SESSION_ID = ""
SLACK_WEBHOOK = ""

# these variables do not need edited
PRIVATE_LEADERBOARD_URL = "https://adventofcode.com/2017/leaderboard/private/view/"

def formatLeaderMessage(members):
    message = "Dagens topplista:"

    # add each member to message
    for username, score, stars in members[0:15]:
        message += "\n*{}* {} Poäng, {} :star:".format(username, score, stars)

    message += "\n\n<{}{}|Se topplistan online>".format(PRIVATE_LEADERBOARD_URL, LEADERBOARD_ID)

    return message

def parseMembers(members_json):
    # get member name, score and stars
    members = [(m["name"], m["local_score"], m["stars"]) for m in members_json.values()]

    # sort members by score, decending
    members.sort(key=lambda s: -s[1])

    return members

def postMessage(message):
    payload = json.dumps({
        "icon_emoji": ":christmas_tree:",
        "username": "Advent Of Code topplista",
        "text": message
    })

    requests.post(
        SLACK_WEBHOOK,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

def main():
    # make sure all variables are filled
    if LEADERBOARD_ID == "" or SESSION_ID == "" or SLACK_WEBHOOK == "":
        print("Please update script variables before running script.\nSee README for details on how to do this.")
        exit(1)

    # retrieve leaderboard
    r = requests.get(
        "{}{}.json".format(PRIVATE_LEADERBOARD_URL, LEADERBOARD_ID),
        cookies={"session": SESSION_ID}
    )
    if r.status_code != requests.codes.ok:
        print("Error retrieving leaderboard")
        exit(1)

    # get members from json
    members = parseMembers(r.json()["members"])

    # generate message to send to slack
    message = formatLeaderMessage(members)

    # send message to slack
    postMessage(message)

if __name__ == "__main__":
    main()
