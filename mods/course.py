import requests
from bs4 import BeautifulSoup

# 課程餘額
# return: course
# {name: 課程名稱, limit: 人數上限, enrollment: 修課人數, remaining: 人數餘額}
def person(selectno: int):
    try: 
        course = {}
        url = 'https://alcat.pu.edu.tw/choice/q_person.php'
        data = {
            'selectno': selectno
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            course_name = soup.find('h2', string=lambda text: text and '科目名稱：' in text).text
            course["name"] = str(course_name.replace('科目名稱：', ''))
            rows = soup.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    if key == '人數上限':
                        course["limit"] = value
                    elif key == '修課人數':
                        course["enrollment"] = value
                    elif key == '人數餘額':
                        course["remaining"] = value
            try:
                course["remaining"] = int(course["limit"]) - int(course["enrollment"])
            except Exception as e:
                print(f"Error calculating remaining seats: {e}")
                course["enrollment"] = int(course["limit"]) - int(course["remaining"])
        return course
    except Exception as e:
        print(f"Error retrieving course information: {e}")
        return course

# 課程綱要
# return: course
# {name: 課程名稱, instructor: 授課教師, time: 上課時段, description: 中文版課程簡介, grading: 評分方式及比重, evaluation: PUHub 課程評論, url: PUHub 課程評論網址, ai_mes: AI 分析}
def syllabus(year: str, selectno: str):
    try: 
        course = {}
        url = f"https://alcat.pu.edu.tw/2011courseAbstract/main.php?ls_yearsem={year}&selectno={selectno}&weekday=&section=&cus_select=&classattri=1&subjname=&teaname=&opunit=&opclass=&lessonlang=&search=%E6%90%9C%E5%B0%8B&click_ok=Y"
        response = requests.get(url)
        if response.status_code == 200:    
            soup = BeautifulSoup(response.text, "html.parser")     
            all_a_elements = soup.find_all('a', href=True)
            for a_element in all_a_elements:
                href = a_element['href'] 
                if "list_abstract_content_100.php?pkey=" in href:
                    new_href = href.replace("..", "https://alcat.pu.edu.tw/")
                    response = requests.get(new_href)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # 課程名稱
                    course_name_element = soup.find(string="課程名稱")
                    course["name"] = course_name_element.find_next('td').get_text(strip=True) if course_name_element else "未找到課程名稱"
                    # 授課教師
                    instructor_element = soup.find(string="授課教師")
                    course["instructor"] = instructor_element.find_next('td').get_text(strip=True) if instructor_element else "未找到授課教師"
                    # 上課時段
                    class_time_element = soup.find(string="上課時段")
                    course["time"] = class_time_element.find_next('td').get_text(strip=True) if class_time_element else "未找到上課時段"
                    # 中文版課程簡介
                    course["description"] = soup.find('th', string='中文版課程簡介Course Description（Chinese Version）').find_next('td').text.strip()
                    if len(course["description"]) > 500:
                        course["description"] = course["description"][:500] + "\n\n...略"
                    # 評分方式及比重
                    course["grading"] = soup.find('th', string="評分方式及比重Grading Methods and Ratio ").find_next('td').text.strip() or "NULL"
                    # PUHub 課程評論
                    course["url"] = f"http://puhub.org/api/course_evaluation.php?course={course['name']}&teacher={course['instructor']}"
                    response = requests.get(course["url"])
                    datas = response.json()
                    course["evaluation"] = "```NULL```"
                    if datas:
                        course["evaluation"] = " ".join([f"```{data[6]}```" for data in datas])
                    # AI 分析
                    course["ai_mes"] = f"以下是課程綱要，請提供我約 100~200 字修課分析，請不要列點、不要標題。\n- 課程名稱：{course['name']}\n- 授課教師：{course['instructor']}\n- 上課時段：{course['time']}\n- 課程簡介：{course['description']}\n- 評分方式：{course['grading']}"
                    return course
        else:
            raise Exception("Failed to retrieve syllabus information. Response status code: " + str(response.status_code))
    except Exception as e:
        print("Error retrieving syllabus information: " + str(e))
        return course

# 課程查詢
# return: course_data, url
#  [{選課代號: course_code, 上課班級: class_name, 修別: course_type, 科目名稱: course_name, 學分數: credit, 授課老師: teacher, 上課時間地點: schedule}]        
def search(year: str, course_teacher: str, keyword: str):
    try: 
        if course_teacher == "課程":
            url = f"https://alcat.pu.edu.tw/2011courseAbstract/main.php?ls_yearsem={year}&selectno=&weekday=&section=&cus_select=&classattri=1&subjname={keyword}&teaname=&opunit=&opclass=&lessonlang=&search=%E6%90%9C%E5%B0%8B&click_ok=Y"
        else:
            url = f"https://alcat.pu.edu.tw/2011courseAbstract/main.php?ls_yearsem={year}&selectno=&weekday=&section=&cus_select=&classattri=1&subjname=&teaname={keyword}&opunit=&opclass=&lessonlang=&search=%E6%90%9C%E5%B0%8B&click_ok=Y"
        response = requests.get(url)
        if response.status_code == 200:    
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find('table', class_='table_info')
            rows = table.find_all('tr')
            course_data = []
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 8: 
                    course_code, class_name, course_type, course_name, _, credit, teacher, schedule = [cell.text.strip() for cell in cells[:8]]
                    course_info = {
                        '選課代號': course_code,
                        '上課班級': class_name,
                        '修別': course_type,
                        '科目名稱': course_name,
                        '學分數': credit,
                        '授課老師': teacher,
                        '上課時間地點': schedule
                    }   
                    course_data.append(course_info)
            return course_data, url
        else:
            raise Exception(f"Failed to retrieve course information. Response status code: {response.status_code}")
    except Exception as e:
        print(f"Error retrieving course information: {e}")
        return course_data, url
