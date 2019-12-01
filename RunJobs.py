import schedule
import time

class RunJob:

    def __init__(self):
        pass

    def send_his_welcome_message(self):
        print("Works")

    def run_jobs(self):
        schedule.every(2).hour.do(self.send_his_welcome_message)

        while True:
            schedule.run_pending()
            time.sleep(1)

def main1():
    runJob = RunJob()
    runJob.run_jobs()

if __name__ == "__main__":
    main1()