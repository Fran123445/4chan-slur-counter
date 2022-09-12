import requests
import bs4


def get_threads(boards):
    """Get all active (non-archived) threads on each board"""

    amount = 1
    page = 0
    thread_list = []
    page_list = []
    board_dict = dict.fromkeys(boards)

    # Do a request for each page on each board
    for board in boards:
        while page < 11:
            page_list.append(requests.get(f"https://boards.4chan.org/{board}/{page}"))
            if page == 0:
                print(f"Page 1 out of 10")
                page += 2
            else:
                print(f"Page {page} out of 10")
                page += 1

        board_dict[board] = page_list
        page_list = []
        page = 0
        print(f"{amount} out of {len(boards)} boards requested")
        amount += 1

    # Get each thread number
    for board in board_dict:
        while page < 10:
            soup = bs4.BeautifulSoup(board_dict[board][page].text, "html.parser")
            for tag in soup.findAll("span", class_="postNum desktop"):
                thread_list.append(str(tag).split("#")[0].split("/")[1])
                thread_list = list(dict.fromkeys(thread_list))
            page += 1

        board_dict[board] = thread_list
        thread_list = []
        page = 0

    return board_dict


def count(thread_dict):
    """Count the amount of slurs per board"""

    amount = 1
    slur_list = {"nigga": 0, "nigger": 0, "fag": 0, "troon": 0, "tranny": 0, "(((them)))": 0, "kike": 0, "argie": 0,
                 "bri'ish": 0, "dyke": 0, "chink": 0, "ching chong": 0, "pajeet": 0, "goy": 0, "gypsy": 0, "tard": 0,
                 "schizo": 0}

    for board in thread_dict:
        # Iterate through each board

        for thread in thread_dict[board]:
            # Iterate through each thread on the current board

            request = requests.get(f"https://boards.4chan.org/{board}/thread/{thread}")
            soup = bs4.BeautifulSoup(request.text, "html.parser")
            for tag in soup.findAll("blockquote", class_="postMessage"):
                # Iterate through each reply on the current thread

                tag_list = str(tag).split()
                for word in tag_list:
                    # Iterate through each word on the current reply

                    if any(slur in word.lower() for slur in slur_list):
                        # Check if any slur is contained in any of those words

                        for slur in slur_list:
                            if slur in word.lower():
                                slur_list[slur] += 1
                                break

            print(f"{amount} out of {len(thread_dict[board])}")
            amount += 1

        thread_dict[board] = slur_list
        slur_list = dict.fromkeys(slur_list, 0)
        amount = 1

    return thread_dict


def log_to_file(board_slur_list):
    """Log each board's slur count on a file"""

    with open("slur_log.txt", "a") as log:

        for board in board_slur_list:
            log.write(f"/{board}/\n")
            for slur in board_slur_list[board]:
                log.write(f'"{slur}": {board_slur_list[board][slur]}, ')
            log.write("\n")

        log.write("\n")

    log.close()


if __name__ == '__main__':
    boards = ["3", "a", "adv", "an", "b", "bant", "biz", "c", "cgl", "ck", "cm", "co", "d", "diy",
              "e", "f", "fa", "fit", "g", "gd", "gif", "h", "hc", "hm", "hr", "i", "ic", "int", "jp",
              "k", "lgbt", "lit", "m", "mlp", "mu", "n", "news", "o", "out", "p", "po", "pol", "r",
              "r9k", "s4s", "s", "sci", "soc", "sp", "t", "tg", "toy", "trv", "tv", "u", "v", "vg",
              "vp", "vr", "vt", "w", "wg", "wsg", "wsr", "x", "xs", "y"]

    thread_dict = get_threads(boards)
    board_slur_list = count(thread_dict)
    log_to_file(board_slur_list)
