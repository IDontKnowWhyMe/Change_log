import sys

class Recorde:
    def __init__(self, file) -> None:
        self.commit = None
        self.merge = None
        self.author = None
        self.date = None
        self.artf = None
        self.commit_text = None
        self.prev_records = dict()
        self.change_log_file = file

    def prin_record(self):
        print("Artf: " + self.artf + "\n" +
               "Author: " + self.author + "\n" +
                "Date: " + self.date + "\n" + 
                "Commit-msg: " + self.commit_text + "\n"
             )
    
    def write_record(self):
        log = "Artf: " + self.artf + "\n" + \
               "Author: " + self.author + "\n" + \
                "Date: " + self.date + "\n" + \
                "Commit-msg: " + self.commit_text + "\n\n"
        self.change_log_file.write(log)


    def reset_record(self):
        self.commit = None
        self.merge = None
        self.author = None
        self.date = None
        self.artf = None
        self.commit_text = None

def print_help():
    help ="\nHow to run script: .\cahnge_log.py [switches] [filters] <file>\n\n\
switches: --end-version \"version\" //script is parsing all logs to given version\n\
\t  --end-commit \"commit\" //script is parsing all logs to given commit\n\
\t  --similarity-value <0-100> //how mutch % of commit_msg for artf need to be same to remove log\n\n \
\
filters: --author \"name\" //script leaves only commits created by given author <name, surname or email>\n\
\t  --date \"Month DD YY\" //script leaves only commits created on a given date Month: Jan, Feb, Mar .....)(DD: <0-31>)(YY: <2021-2022>)\n\
\t  --artf \"artf\" //script leaves only commits to given artf\n\n\
\
<file>:  File which contains git logs to parse\n"
    print(help)

def get_commit(line):
    splited_line = line.split()
    if splited_line[0] == "commit":
        return splited_line[1]
    return None

def get_merge(line):
    splited_line = line.split()
    if splited_line[0] == "Merge:":
        return ' '.join(splited_line[1::])
    return None

def get_author(line):
    splited_line = line.split()
    if splited_line[0] == "Author:":
        return ' '.join(splited_line[1::])
    return None

def get_date(line):
    splited_line = line.split()
    if splited_line[0] == "Date:":
        return ' '.join(splited_line[1::])
    return None

def get_artf(line):
    allowed_mod = {"Merge", "Revert", "Added", "Fixed"}
    splited_line = line.split()
    if splited_line[0][0] == '[':
        return (splited_line[0], line)
    if splited_line[0] in allowed_mod:
        change = splited_line[0]
        artf_start = -1
        artf_end = -1
        idx = 0
        joint = ' '.join(splited_line[1::])
        for char in joint:
            if char == '[' and artf_start and artf_start == -1:
                artf_start = idx
            if char == ']' and artf_end == -1:
                artf_end = idx
            idx += 1
        return (joint[artf_start:artf_end+1], line)
    return (None, None)

def check_end(record):
    if record.commit_text is None:
        return False
    if "--end-commit" in sys.argv:
        idx = sys.argv.index("--end-commit")
        return sys.argv[idx + 1] == record.commit
    if "--end-version" in sys.argv:
        idx = sys.argv.index("--end-version")
        return sys.argv[idx + 1] in record.commit_text
    return False

def filter_record(record):
    author = True
    date = True
    artf = True
    if "--author" in sys.argv:
        idx = sys.argv.index("--author")
        author = sys.argv[idx + 1] in record.author
    if "--date" in sys.argv:
        idx = sys.argv.index("--date")
        date_list = sys.argv[idx + 1].split()
        date = date_list[0] in record.date and \
               date_list[1] in record.date and \
               date_list[2] in record.date
    if "--artf" in sys.argv:
        idx = sys.argv.index("--artf")
        artf = sys.argv[idx + 1] in record.artf
    return author and date and artf

def check_rep(record):
    needed_sim = 80
    if "--similarity-value" in sys.argv:
        idx = sys.argv.index("--similarity-value")
        needed_sim = int(sys.argv[idx + 1])
    min_commit = 20
    if len(record.commit_text) < min_commit:
        return False
    for commit in record.prev_records[record.artf]:
        similarities = 0
        min_len = min(len(record.commit_text), len(commit))
        for i in range(min_len):
            if (record.commit_text[i] == commit[i]):
                similarities += 1
        sim_per = 100 * similarities / min_len
        if sim_per > needed_sim:
            return False
    return True

def check_duplicate(record):
    if record.artf not in record.prev_records:
        record.prev_records[record.artf] = [record.commit_text]
        return True
    else:
        if check_rep(record):
            record.prev_records[record.artf].append(record.commit_text)
            return True
    return False

def set_record(record, line):
    if line == "":
        return
    commit = get_commit(line)
    if  commit is not None:
        if record.commit is not None:
            if check_end(record):
                exit()
            if record.artf is not None and check_duplicate(record) and filter_record(record):
                record.write_record()
            record.reset_record()
        record.commit = commit
    merge = get_merge(line)
    author = get_author(line)
    date = get_date(line)
    artf, commit_msg = get_artf(line)
    if merge is not None:
        record.merge = merge
    if author is not None:
        record.author = author
    if date is not None:
        record.date = date
    if artf is not None and commit_msg is not None and record.artf is None:
        record.commit_text = commit_msg
        record.artf = artf


def parse_lines():
    change_log = open("change_log", 'a+')
    file = open(sys.argv[-1], 'r')
    lines = file.readlines()
    record = Recorde(change_log)
    for line in lines:
        set_record(record, line.strip())
    change_log.close()
    file.close()



def main():
    if sys.argv[1] == "--help":
        print_help()
        exit()
    parse_lines()

if __name__ == "__main__":
    main()
