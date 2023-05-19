import tagui as r
import pandas as pd

Review = 'Not Found'


# def click_next_page(hint):
#     if r.read("//div[@class='ui_pagination is-centered']/a") == "Next":
#         r.click("//div[@class='ui_pagination is-centered']/a")
#         hint = "Next page"
#     else:
#         hint = "No next page"


def store_data(num, data):
    global Review
    for i in range(1, num + 1):
        Review = r.read(f"(//span[@class='QewHA H4 _a'])[{i}]")
        data.append({'Review Comment': Review})
        Review = 'Not Found'


# hint= "Next page"
data = []
r.init()
r.url('https://www.tripadvisor.com.sg/Hotel_Review-g294265-d302109-Reviews-Shangri_La_Singapore-Singapore.html')
r.wait(2)
total_page = 500

for j in range(1, total_page + 1):
    print(j)
    r.wait(5)
    table_num = r.count("//span[@class='QewHA H4 _a']")
    # r.wait(1)
    print(table_num)
    store_data(table_num, data)
    print('success')
    r.wait(1)
    r.url(f'https://www.tripadvisor.com.sg/Hotel_Review-g294265-d302109-Reviews-or{j*10}-Shangri_La_Singapore-Singapore.html')

r.close()

df = pd.DataFrame(data)
df.to_excel("review5000.xlsx", index=False)