from an_adventure import start
import argparse

def main():

    parser = argparse.ArgumentParser(description="Starts an adventure!")
    parser.add_argument("-s", "--skip-intro", dest="skipIntro", action="store_true", default=False, help="skip the introduction")

    args = vars(parser.parse_args())

    start(**args)

if __name__ == "__main__":
    main()
    