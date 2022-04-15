# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import random

import urllib3


from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


from code_to_comment.code_to_com import code_to_com 
from name_helper.name_creater import name_creater 
from comment_to_code.com_to_code import com_to_code
import requests
import json
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CodeToCommentSection(Action):

    def name(self) -> Text:
        return "action_code_to_comment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        headers = {
        }
        
        # url = 'https://newsapi.org/v2/top-headlines?q=crypto&apiKey=45a95279caaa429e8951aaab6a90086f'

        # response = requests.get(url, headers=headers, verify=False)
        # # json_data = json.dumps(response.json())
        # # obj = json.loads(json_data)
        # obj = json.loads(response.text)

        # index = random.randint(0, obj['totalResults'])

        
        # output = obj['articles'][index]['title'] + ' too read further ' + obj['articles'][index]['url']
        text=tracker.latest_message['text']
        output = code_to_com(text)
        dispatcher.utter_message(text=output)

        return []

class CodeHelper(Action):

    def name(self) -> Text:
        return "action_name_create"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        headers = {
        }
        
        # url = 'https://newsapi.org/v2/top-headlines?q=crypto&apiKey=45a95279caaa429e8951aaab6a90086f'

        # response = requests.get(url, headers=headers, verify=False)
        # # json_data = json.dumps(response.json())
        # # obj = json.loads(json_data)
        # obj = json.loads(response.text)

        # index = random.randint(0, obj['totalResults'])

        
        # output = obj['articles'][index]['title'] + ' too read further ' + obj['articles'][index]['url']
        text=tracker.latest_message['text']
        output = name_creater(text)
        dispatcher.utter_message(text=output)

        return []

class CommentToCode(Action):

    def name(self) -> Text:
        return "action_comment_to_code"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        headers = {
        }
        
        # url = 'https://newsapi.org/v2/top-headlines?q=crypto&apiKey=45a95279caaa429e8951aaab6a90086f'

        # response = requests.get(url, headers=headers, verify=False)
        # # json_data = json.dumps(response.json())
        # # obj = json.loads(json_data)
        # obj = json.loads(response.text)

        # index = random.randint(0, obj['totalResults'])

        
        # output = obj['articles'][index]['title'] + ' too read further ' + obj['articles'][index]['url']
        text=tracker.latest_message['text']
        output = com_to_code(text)
        dispatcher.utter_message(text=output)

        return []

# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
