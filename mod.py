# import requests
# from bs4 import BeautifulSoup

# # make a GET request to the Google search page
# query = "who is rahul gandhi"
# url = f"https://www.google.com/search?q={query}"
# response = requests.get(url)

# # parse the HTML response
# soup = BeautifulSoup(response.text, 'html.parser')

# # extract the "People also ask" questions and answers
# questions = soup.find_all('div', {'class': 'Lt3Tzc'})
# for question in questions:
#     print(question.text)
#     answer_container = question.find_next('div', {'class': 'Lt3Tzc'})
#     if answer_container:
#         print(answer_container.text)

# answers = soup.find_all('div', {'class': 'BNeawe iBp4i AP7Wnd'})

# import requests
# from bs4 import BeautifulSoup

# # make a GET request to the Google search page
# query = "example query"
# url = f"https://www.google.com/search?q={query}"
# response = requests.get(url)

# # parse the HTML response
# soup = BeautifulSoup(response.text, 'html.parser')
# with open("quuu.txt","a",encoding="utf-8")as f:
#     f.write(str(soup))
# # extract the "People also ask" questions and answers
# questions = soup.find_all('div', {'class': 'Lt3Tzc'})
# answers = soup.find_all('div', {'class': 'Lt3Tzc'})

# for i,question in enumerate(questions):
#     print(question.text)
#     answer_span = answers[i].find('span')
#     if answer_span:
#         print(answer_span.text)
# data = {'success': True, 'correct': True, 'timedout': False, 'correctAnswerId': 4316, 'nextQuestion': {'idSigned': '4690$160360556$8fb6ffc1ee62267385567a5ea4ed2d6b037fd258', 'text': 'What song do the Plastics dance to at the Christmas Show?', 'answers': [{'id': 14073, 'idSigned': '14073$160360556$6109dbccfb8a3906a427120a2797d1cc42e7811e', 'text': 'Jingle Bell Rock'}, {'id': 14074, 'idSigned': '14074$160360556$3b05df5c87af0fa30afc17f5c27cc2afbaed8941', 'text': 'America the Beautiful'}, {'id': 14075, 'idSigned': '14075$160360556$ce2959175498475fb2ee4bd3cf7720b29d43163d', 'text': 'Enter Sandman'}]}}

# answers = data["nextQuestion"]["answers"]
# answer_ids = [answer["id"] for answer in answers]
# answer_texts = [answer["text"] for answer in answers]

# id1, id2, id3 = answer_ids
# answer1, answer2, answer3 = answer_texts

# print("Ids:", id1, id2, id3)
# print("Answers:", answer1, answer2, answer3)

# import httpx,json
# payload = {"one":1,"two":2}
# r = httpx.post("https://rahukmahato.pythonanywhere.com/items",json=payload)
# r = httpx.get("http://rahukmahato.pythonanywhere.com/items")
# print(r.text)







def count_occurrence(text, option):
    import re
    words = option.split()
    count = 0
    for word in words:
        if word not in ["of", "in", "the", "these", "was","a", "an","not","never","except"]:
            pattern = re.compile(r"\b" + word + r"\b")
            count += len(pattern.findall(text))
    return count

def get_highest_rating_index(question, options):
    import re,requests
    from bs4 import BeautifulSoup
    url = f'https://www.google.com/search?q={question}'.replace("not","").replace("never","")
    r = requests.get(url)
    doc = BeautifulSoup(r.content, "html.parser")
    all_text =doc.get_text().strip()
    text = all_text.lower()

    total_count = 0
    for option in options:
        count = count_occurrence(text, option)
        total_count += count
    highest_rating = ""
    for option in options:
        count = count_occurrence(text, option)
        if highest_rating == "" or count > count_occurrence(text, highest_rating):
            highest_rating = option

    return options.index(highest_rating) + 1
 

# total_count = 1
# for option in options:
#     count = count_occurrence(text, option)
#     total_count += count

# highest_rating = ""
# for option in options:
#     count = count_occurrence(text, option)
#     percentage = (count / total_count) * 100
#     if highest_rating == "" or count > count_occurrence(text, highest_rating):
#         highest_rating = option

# for option in options:
#     count = count_occurrence(text, option)
#     percentage = (count / total_count) * 100
#     tick = "☑️" if option == highest_rating else ""
#     print(f"{option} - {count} , {percentage:.2f}% {tick}")
