import argparse
import app


def parse_args():
    parser = argparse.ArgumentParser(description="Simple telegram bot",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--token-path", default="./token")

    return parser.parse_args()


def main():
    args = parse_args()
    with open(args.token_path, "r") as token_file:
        token = token_file.read().rstrip()
    app.init_bot(token)
    app.bot.polling()


if __name__ == "__main__":
    main()
