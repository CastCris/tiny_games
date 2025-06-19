import random

def check_score(answer_user_list, answer_list):
    score = 0
    for i in range(len(answer_list)):
        if answer_user_list[i] == answer_list[i]:
            score += 1
    return score

def get_valid_answer(question_text, key):
    while True:
        answer = input(f"\n{key}. {question_text}").lower()
        if answer in ["a", "b", "c", "d", "e"]:
            return answer
        else:
            print("Please enter a valid option: a, b, c, d, or e.")


print("Welcome to the interactive quiz!\nYou'll answer a bunch of questions and at the end you'll receive your score based on your corrected answers.")

i = "y"
while i == "y":
    answer_user_list = []

    bank_questions = {
        "What's the largest animal species currently alive?\na) African elephant\nb) Colossal squid\nc) Great white shark\nd) Blue whale\ne) Sperm whale\n\nAnswer: ": "d",
        "What animal must sleep standing up?\na) Kangoroo\nb) Elephant\nc)Horse\nd) Frog\ne) Monkey: ": "c",

        "What's the capital of Australia?\na) Canberra\nb) Melbourne\nc) Sydney\nd) Brisbane\ne) Perth\n\nAnswer: ": "a",

        "Who wrotes the play Romeo and Julieta?\na) Edgar Allan Poe\nb) Jane Austen\nc) Charles Dickens\nd) Leo Tolstoy\ne) William Shakespeare\n\nAnswer: ": "e",

        "What does HTTP stand in a website adress?\na) Hyper Text Transmission Protocol\nb) Hyper Tool Transfer Protocol\nc) Hyperlink and Text Transfer Protocol\nd) Hyper Terminal Transfer Protocol\ne) Hyper Text Transfer Protocol\n\nAnswer: ": "e",

        "What does HTTPS add to HTTP?\na) Faster loading\nb) Encryption using SSL/TLS\nc) Compatibility with firewalls\nd) Data compression\ne) Mobile optimization\n\nAnswer: ": "b",
        "What's the primary goal of a DDoS attack?\na) Encrypt data for ransom\nb) Overload a system to disrupt service availability\nc) Gain unauthorized acess to user accounts\nd) Redirect traffic to malicious websites\ne) Intercept private messages\n\nAnswer: ": "b",

        "How does the cluster size affect disk performance?\na) Larger clusters cause slow read/write speeds\nb) Smaller clusters always improve speed by storing more files per cluster\nc) Smaller clusters cause more fragmentation and slow down the disk\nd) Larger clusters improve speed by reducing the number of clusters to manage\ne) Cluster size has no effect on disk speed\n\nAnswer: ": "d",

        "What's the main cause of wasted disk space in relation to cluster size?\na) Files being compressed incorrectly\nb) Files too large to fit into a single cluster\nc) Files smaller than the cluster size occuping a full cluster\nd) Overlapping files in the file system\ne) Defragmentation process\n\nAnswer: ": "c",

        "What is the purpose of file system journaling?\na) To speed up file retrieval times\nb) To keep track of changes made to the file system to recover from crashes\nc) To compress files for storage efficiency\nd) To store file metadata only\ne) To fragment files for better performance\n\nAnswer: ": "b",

        "Which of the following is an example of a block-level storage system?\na) Hard drive\nb) SSD (Solid State Drive)\nc) Cloud storage\nd) File server\ne) Optical disk\n\nAnswer: ": "b",

        "What does RAID 5 configuration offer?\na) Faster read/write speeds\nb) Data redundancy with parity information\nc) No data redundancy\nd) Independent disks with no mirroring\ne) All of the above\n\nAnswer: ": "b",

        "Which is the primary advantage of using a solid-state drive (SSD) over a traditional hard disk drive (HDD)?\na) Higher capacity\nb) Faster read/write speeds\nc) Cheaper storage\nd) Better durability\ne) Easier to repair\n\nAnswer: ": "b",

        "Which file system type is commonly used for external drives in Windows?\na) NTFS\nb) FAT32\nc) exFAT\nd) EXT4\ne) APFS\n\nAnswer: ": "c",

        'What does the term "block size" refer to in a file system?\na) The physical size of the hard drive\nb) The size of the smallest unit of storage on a disk\nc) The amount of space used for file system metadata\nd) The speed of data access\ne) The size of a file when compressed\n\nAnswer: ': 'b',

        "What is the main advantage of using a file system with journaling?\na) Faster data transfer speeds\nb) Enhanced security for stored files\nc) Protection against data loss during crashes or power outages\nd) Compression of files for reduced storage\ne) Increased file fragmentation\n\nAnswer: ": "c",

        'In terms of storage, what does the term "latency" refer to?\na) The amount of space used by files\nb) The time it takes for a storage device to retrieve data\nc) The speed of data transfer between devices\nd) The size of a file in the system\ne) The encryption level of files stored\n\nAnswer: ': 'b',

        "Which of the following is an example of a file system optimized for large storage volumes, like those used in servers?\na) FAT32\nb) NTFS\nc) EXT4\nd) ZFS\ne) APFS\n\nAnswer: ": "d",

        "What is the primary purpose of a storage area network (SAN)?\na) To provide direct access to physical storage devices over a network\nb) To back up files to an external cloud storage system\nc) To reduce network traffic by caching files locally\nd) To monitor storage health in real time\ne) To compress and store data for faster access\n\nAnswer: ": "a",

        "What is the main benefit of using a file system with encryption?\na) Faster data access\nb) Reduced disk fragmentation\nc) Enhanced data security\nd) Increased file size\ne) Better compression\n\nAnswer: ": "c"
    }

    questions_play = random.sample(list(bank_questions.keys()), 10)
    answer_list = [bank_questions[key] for key in questions_play]

    key = 0
    for q in questions_play:
        key += 1
        answer_user_list.append(get_valid_answer(q, key))


    answer_list_dic = []
    answer_user_list_dic = []
    for i in range(len(answer_list)):
        answer_list_dic.append({f"{i + 1}.": answer_list[i]})
        answer_user_list_dic.append({f"{i + 1}.": answer_user_list[i]})

    print("\nYour answers:\n", answer_user_list_dic)

    score = check_score(answer_user_list, answer_list)
    print(f"\n=============\nScore: {score} /", len(questions_play), "\n=============\n")

    i = input("\nPress (y) to play again\nPress (a) to view the answer list\nPress any key to exit\n").lower()

    if i == "a":
        print("\nCorrect answers:\n", answer_list_dic)
        i = input("\nPress (y) to play again\nPress any key to exit\n").lower()
