import requests
import bs4
import time
import multiprocessing


def get_threads(board_dict, board):
    """Get all active (non-archived) threads on each board"""

    page = 0
    thread_list = []
    page_list = []

    # Do a request for each page on each board
    while page < 11:
        page_list.append(requests.get(f"https://boards.4chan.org/{board}/{page}"))
        if page == 0:
            #print(f"Page 1 out of 10. Current board: /{board}/")
            page += 2
        else:
            #print(f"Page {page} out of 10. Current board: /{board}/")
            page += 1

    board_dict[board] = page_list
    page = 0

    # Get each thread number
    while page < 10:
        soup = bs4.BeautifulSoup(board_dict[board][page].text, "html.parser")
        for tag in soup.findAll("span", class_="postNum desktop"):
            thread_list.append(str(tag).split("#")[0].split("/")[1])
            thread_list = list(dict.fromkeys(thread_list))
        page += 1

    print(f"/{board}/ - Requesting done")
    board_dict[board] = thread_list

def count(board_dict, board):
    """Count the amount of slurs per board"""

    slur_list = {"nigga": 0, "nigger": 0, "fag": 0, "troon": 0, "tranny": 0, "(((them)))": 0, "kike": 0, "argie": 0,
                 "bri'ish": 0, "dyke": 0, "chink": 0, "ching chong": 0, "pajeet": 0, "goy": 0, "gypsy": 0, "tard": 0,
                 "schizo": 0}


    for thread in board_dict[board]:
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

    board_dict[board] = slur_list

    print(f"/{board}/ - Counting done")

    return board_dict


def log_to_file(board_slur_list, current_time):
    """Log each board's slur count on a file"""

    time = f"{current_time.tm_hour}:{current_time.tm_min}\t{current_time.tm_mday}/{current_time.tm_mon}/{current_time.tm_year}"

    with open("slur_log.txt", "a") as log:
        log.write(f"{time}\n\n")

        for board in board_slur_list:
            log.write(f"/{board}/\n")
            for slur in board_slur_list[board]:
                log.write(f'"{slur}": {board_slur_list[board][slur]},\t')
            log.write("\n\n")

        log.write("\n\n\n")

    log.close()

def multiproc(board_dict, func):

    get_pages = multiprocessing.Process(target=func)
    processes = []
    manager = multiprocessing.Manager()
    cuack = manager.dict(board_dict)

    for board in board_dict:
        get_pages = multiprocessing.Process(target=func, args=(cuack, board))
        processes.append(get_pages)
        get_pages.start()

    for proc in processes:
        proc.join()

    return cuack



if __name__ == '__main__':
    boards = ["3", "a", "adv", "an", "b", "bant", "biz", "c", "cgl", "ck", "cm", "co", "d", "diy",
              "e", "f", "fa", "fit", "g", "gd", "gif", "h", "hc", "hm", "hr", "i", "ic", "int", "jp",
              "k", "lgbt", "lit", "m", "mlp", "mu", "n", "news", "o", "out", "p", "po", "pol", "r",
              "r9k", "s4s", "s", "sci", "soc", "sp", "t", "tg", "toy", "trv", "tv", "u", "v", "vg",
              "vp", "vr", "vt", "w", "wg", "wsg", "wsr", "x", "xs", "y"]

    board_dict = dict.fromkeys(boards)

    board_dict = multiproc(board_dict, get_threads)
    print("\n-Starting count process-\n")
    board_dict = multiproc(board_dict, count)

    current_time = time.localtime(time.time())

    log_to_file(board_dict, current_time)
