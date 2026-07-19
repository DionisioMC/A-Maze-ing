from sys import argv


def main():
    with open(argv[1]) as file:
        content: list[str] = file.read().split("\n")
        print(content)


if __name__ == "__main__":
    main()
