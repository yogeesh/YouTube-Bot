import schedule
import time
from YouTubeAPI import YouTubeAPI

class RunJob:

    def __init__(self):
        self.YouTubeAPI_Obj = YouTubeAPI()

    def welcome_message_every_hour(self):
        print("[WIP]  Sending Welcome message...")
        live_chat_id = self.YouTubeAPI_Obj.getLiveChatId()
        messages = [
            "Hi",
            "Hello",
            "Oi",
            "Salut",
            "Привет",
            "Namaste",
            "Salve",
            "Welcome Brawlers :)",
            "SUBSCRIBE and stay connected :D"
        ]

        # messages = [""]
        for message in messages:
            self.YouTubeAPI_Obj.send_message(live_chat_id, message)
        
        print("[DONE] Sent Welcome message!")

    def run_jobs(self):
        schedule.every(2).hours.do(self.welcome_message_every_hour)

        while True:
            try:
                schedule.run_pending()
            except Exception as e:
                print("[Error] Expection : \n %s"%e)
            print("[Hold] ...")
            time.sleep(60)

def main1():
    runJob = RunJob()
    runJob.run_jobs()

if __name__ == "__main__":
    main1()