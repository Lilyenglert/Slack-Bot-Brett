#  CODE ADAPTED FROM  https://www.fullstackpython.com/blog/build-first-slack-bot-python.html


import os
import time
import re
from slackclient import SlackClient

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
#EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_event(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            print(event["channel"])
            if event["channel"] == "DH51YLLJX" or "DH5F2SWLD":
                print("in channel")
                text = event["text"]
                channel = "CH289F6SX"
                if text != None:
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=channel,
                        text=text
                        )
                    slack_client.api_call(
                        "chat.update",
                        channel=channel,
                        ts=timestamp,
                        text="dontknow"
                        )
                time.sleep(RTM_READ_DELAY)
                return text, "CH289F6SX", event["ts"]
            return event["text"], event["channel"], event["ts"]
    return None, None, None

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            text, channel, timestamp = parse_event(slack_client.rtm_read())
            # print(channel)
            # if text != None:
            #     x = input("Say something: ")
            #     string = "{}".format(text, str(x))
                
                    
            #     slack_client.api_call(
            #         "chat.postMessage",
            #         channel=channel,
            #         text=x
            #         )
            #     slack_client.api_call(
            #         "chat.update",
            #         channel=channel,
            #         ts=timestamp,
            #         text="dontknow"
            #         )
            # time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
