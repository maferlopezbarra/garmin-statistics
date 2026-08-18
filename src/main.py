from src.activities import running
from src.hrv import hrv
from src.sleep import sleep


def main():
    running()
    hrv()
    sleep()
    print("Analysis completed successfully.")


if __name__ == "__main__":
    main()
