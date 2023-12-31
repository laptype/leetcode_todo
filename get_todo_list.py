from bs4 import BeautifulSoup
import random
import os

def get_todo(element_path, out_dir):

    with open(element_path, 'r', encoding='utf-8') as f:
        line = f.readline()

    soup = BeautifulSoup(line, 'html.parser')
    tbody = soup.find('tbody')
    trs = tbody.find_all('tr')

    out_rows = []

    for tr in trs:
        # 找 <td></td> 标签
        tds = tr.find_all('td')
        problem_a = tds[2].find_all('a')[0]
        problem_source = tds[1].find_all('a')[0]
        problem_index = tds[0].text.strip()
        problem_title = problem_a.text.strip()
        problem_href = problem_a.get('href')
        problem_source_text = problem_source.text.strip()
        problem_source_href = problem_source.get('href')
        difficulty = tds[3].find_all('div')[0].get('difficulty')

        out_rows.append(f"- [ ] {problem_index}: \t [{problem_title}]({problem_href}) \n")

        print(f"{problem_index}: difficulty: {int(float(difficulty))} : {problem_title}: {problem_href}")

    random.seed(2023)
    random.shuffle(out_rows)
    # new_list = [(i + random.random()*len(out_rows), x) for i, x in enumerate(out_rows)]
    # out_rows = [x for i, x in sorted(new_list)]

    k = 20
    split_len = int(len(out_rows) / k)
    print(split_len)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    for i in range(k):
        with open(os.path.join(out_dir, f"todo_list_{i}.md"), "w", encoding='utf-8') as f:
            f.write(f'# ToDo list {i}: \n\n\n')
            end = (i+1)*split_len if i < k-1 else len(out_rows)
            for row in out_rows[i*split_len:end]:
                f.write(row)

if __name__ == '__main__':
    tag = '1600-1900'
    element_path = f"element/element_{tag}.txt"
    get_todo(element_path, f"todo_list_{tag}")