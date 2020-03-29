from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
pw = "**********"


class ClassBot:
    def __init__(self, username, pw, myClass):
        self.driver = webdriver.Chrome()
        self.driver.get("http://www.cape.ucsd.edu/")
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/main/div/div[2]/section[2]/article/table/tbody/tr/td[2]/div/form/p/input').click()
        sleep(2)

        login_field = self.driver.find_element_by_id('ssousername').send_keys(username)
        pw_field = self.driver.find_element_by_id('ssopassword').send_keys(pw)
        self.driver.find_element_by_xpath('/html/body/main/div/section/div/div/div[1]/div/div[2]/form/button').click()
        sleep(10)

        if myClass != 'all':
            self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtCourse').send_keys(myClass)
            self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnSubmit').click()
            sleep(15)

            grades = []
            sum = 0.0
            count = 0.0
            table = self.driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div/form/div[4]/div[2]/table/tbody/tr')
            for row in table.find_elements_by_xpath(("//td[10]/span")):
                if row.text != 'N/A':
                    grade_num = float(row.text[row.text.find("(")+1: row.text.find(")")])
                    grades.append(grade_num)
                    sum = sum + grade_num
                    count = count + 1

            average = float(sum/count)
            print(str(average))

        else:
            dropdown = self.driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div/form/div[3]/div[1]/div[3]/div[2]/select')
            lowest_classes={}
            for option in dropdown.find_elements_by_tag_name('option'):
                if option.text != 'Select a Department':
                    option.click()
                    self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnSubmit').click()
                    sleep(15)

                    grades = {}
                    class_count = {}
                    min = 100.00
                    table = self.driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div/form/div[4]/div[2]/table/tbody')
                    rows = table.find_elements_by_tag_name("tr")
                    for row in rows:
                        grade = row.find_element_by_xpath("//td[10]/span")
                        name = row.find_element_by_xpath("//td[2]/a")
                        print(grade)
                        if grade.text != 'N/A':
                            grade_num = float(grade.text[grade.text.find("(") + 1: grade.text.find(")")])
                            if name.text in grades:
                                grades[name.text]= grades[name.text] + grade_num
                                class_count[name.text]=class_count[name.text]+1
                                print("comparing " + name.text + " with gpa " + str(grades[name.text]))
                            elif name.text not in grades:
                                grades[name.text] = grade_num
                                print("analyzing " + name.text + " with gpa " + str(grades[name.text]))
                                class_count[name.text] = 1

                    for key in grades:
                        print("current class: " + key)
                        average = float(grades[key] / class_count[key])
                        if len(lowest_classes) < 5:
                            if(average <= min):
                                min = average
                            lowest_classes[key] = average
                            print("just added " + key+ " with gpa" + str(average))
                        elif len(lowest_classes) == 5:
                            if(average <= min):
                                min = average
                                min_val = min(lowest_classes, key=lowest_classes.get)
                                del lowest_classes[min_val]
                                lowest_classes[key] = average

whatClass = input('What class?: ')
ClassBot('mmarsell', pw, whatClass)
