import random

questions_dict = {
    0: "What's the largest animal species currently alive?",
    1: "What animal must sleep standing up?",
    2: "What's the capital of Australia?",
    3: "Who wrotes the play Romeo and Julieta?",
    4: "What does HTTP stand in a website adress?",
    5: "What does HTTPS add to HTTP?",
    6: "What's the primary goal of a DDoS attack?",
    7: "How does the cluster size affect disk performance?",
    8: "What's the main cause of wasted disk space in relation to cluster size?",
    9: "What is the purpose of file system journaling?",
    10: "Which of the following is an example of a block-level storage system?",
    11: "What does RAID 5 configuration offer?",
    12: "Which is the primary advantage of using a solid-state drive (SSD) over a traditional hard disk drive (HDD)?",
    13: "Which file system type is commonly used for external drives in Windows?",
    14: 'What does the term "block size" refer to in a file system?',
    15: "What is the main advantage of using a file system with journaling?",
    16: 'In terms of storage, what does the term "latency" refer to?',
    17: "Which of the following is an example of a file system optimized for large storage volumes, like those used in servers?",
    18: "What is the primary purpose of a storage area network (SAN)?",
    19: "What is the main benefit of using a file system with encryption?"
}

answers_ID = {
    0: "d",
    1: "c",
    2: "a",
    3: "e",
    4: "e",
    5: "b",
    6: "b",
    7: "d",
    8: "c",
    9: "b",
    10: "b",
    11: "b",
    12: "b",
    13: "c",
    14: "b",
    15: "c",
    16: "b",
    17: "d",
    18: "a",
    19: "c"

}

answers_text_list = [
    ["African elephant", "Colossal squid", "Great white shark", "Blue whale", "Sperm whale"],
    ["Kangoroo", "Elephant", "Horse", "Frog", "Monkey"],
    ["Canberra", "Melbourne", "Sydney", "Brisbane", "Perth"],
    ["Edgar Allan Poe", "Jane Austen", "Charles Dickens", "Leo Tolstoy", "William Shakespeare"],
    ["Hyper Text Transmission Protocol", "Hyper Tool Transfer Protocol", "Hyperlink and Text Transfer Protocol", "Hyper Terminal Transfer Protocol", "Hyper Text Transfer Protocol"],
    ["Faster loading", "Encryption using SSL/TLS", "Compatibility with firewalls", "Data compression", "Mobile optimization"],
    ["Encrypt data for ransom", "Overload a system to disrupt service availability", "Gain unauthorized acess to user accounts", "Redirect traffic to malicious websites", "Intercept private messages"],
    ["Larger clusters cause slow read/write speeds", "Smaller clusters always improve speed by storing more files per cluster", "Smaller clusters cause more fragmentation and slow down the disk", "Larger clusters improve speed by reducing the number of clusters to manage", "Cluster size has no effect on disk speed"],
    ["Files being compressed incorrectly", "Files too large to fit into a single cluster", "Files smaller than the cluster size occuping a full cluster", "Overlapping files in the file system", "Defragmentation process"],
    ["To speed up file retrieval times", "To keep track of changes made to the file system to recover from crashes", "To compress files for storage efficiency", "To store file metadata only", "To fragment files for better performance"],
    ["Hard drive", "SSD (Solid State Drive)", "Cloud storage", "File server", "Optical disk"],
    ["Faster read/write speeds", "Data redundancy with parity information", "No data redundancy", "Independent disks with no mirroring", "All of the above"],
    ["Higher capacity", "Faster read/write speeds", "Cheaper storage", "Better durability", "Easier to repair"],
    ["NTFS", "FAT32", "exFAT", "EXT4", "APFS"],
    ["The physical size of the hard drive", "The size of the smallest unit of storage on a disk", "The amount of space used for file system metadata", "The speed of data access", "The size of a file when compressed"],
    ["Faster data transfer speeds", "Enhanced security for stored files", "Protection against data loss during crashes or power outages", "Compression of files for reduced storage", "Increased file fragmentation"],
    ["The amount of space used by files", "The time it takes for a storage device to retrieve data", "The speed of data transfer between devices", "The size of a file in the system", "The encryption level of files stored"],
    ["FAT32", "NTFS", "EXT4", "ZFS", "APFS"],
    ["To provide direct access to physical storage devices over a network", "To back up files to an external cloud storage system", "To reduce network traffic by caching files locally", "To monitor storage health in real time", "To compress and store data for faster access"],
    ["Faster data access", "Reduced disk fragmentation", "Enhanced data security", "Increased file size", "Better compression"]
]

answers_list = [3, 2, 0, 4, 4, 1, 1, 3, 2, 1, 1, 1, 1, 2, 1, 2, 1, 3, 0, 2]


def check_score(answers_user_list, answers_list):
    score = 0
    for i in range(len(answers_list)):
        if answers_user_list[i] == answers_list[i]:
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
    user_answers_list = []










    score = check_score(user_answers_list, randomic_answers_list)
    print(f"\n=============\nScore: {score} /", len(question_play), "\n=============\n")

    i = input("\nPress (y) to play again\nPress (a) to view the answer list\nPress any key to exit\n").lower()

    if i == "a":
        print("\nCorrect answers:\n", answer_list_dic)
        i = input("\nPress (y) to play again\nPress any key to exit\n").lower()




    # randomic_questions_list = random.sample(list(questions_dict.keys()), 10)
    # randomic_answers_list = [randomic_questions_list[key] for key in randomic_questions_list]

    # key = 0
    # for q in randomic_questions_list:
    #     key += 1
    #     user_answers_list.append(get_valid_answer(q, key))


    # answers_list_dict = []
    # answers_user_list_dic = []
    # for i in range(len(answer_list)):
    #     answers_list_dict.append({f"{i + 1}.": answer_list[i]})
    #     answers_user_list_dic.append({f"{i + 1}.": answers_user_list[i]})

    # print("\nYour answers:\n", answers_user_list_dic)