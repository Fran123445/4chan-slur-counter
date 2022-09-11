import requests
import bs4

def get_threads(boards):
    """All active threads on each board"""

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
                page +=1

        board_dict[board] = page_list
        page_list = []
        page = 0
        print(f"{amount} out of {len(boards)} boards requested")
        amount += 1

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

if __name__ == '__main__':
    boards = ["3", "a", "adv", "an", "b", "bant", "biz", "c", "cgl", "ck", "cm", "co", "d", "diy",
              "e", "f", "fa", "fit", "g", "gd", "gif", "h", "hc", "hm", "hr", "i", "ic", "int", "jp",
              "k", "lgbt", "lit", "m", "mlp", "mu", "n", "news", "o", "out", "p", "po", "pol", "r",
              "r9k", "s4s", "s", "sci", "soc", "sp", "t", "tg", "toy", "trv", "tv", "u", "v", "vg",
              "vp", "vr", "vt", "w", "wg", "wsg", "wsr", "x", "xs", "y"]

    thread_list = get_threads(boards)
