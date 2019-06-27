import matplotlib.pyplot as plt
from boss.DB import DBPool
from pylab import mpl
import wordcloud


def getData():
    pool = DBPool.MySqlPool()
    sql = "SELECT education AS education, COUNT(*) FROM boss_spider_result GROUP BY education"
    sql1 = "SELECT city AS city, COUNT(*) FROM boss_spider_result GROUP BY city"
    sql2 = "SELECT workYear AS workYear, COUNT(*) FROM boss_spider_result GROUP BY workYear"
    sql3 = "SELECT industryField FROM boss_spider_result"
    sql4 = "SELECT salary FROM boss_spider_result"

    educationData = pool.query_(sql)
    cityData = pool.query_(sql1)
    workYearData = pool.query_(sql2)
    industryData = pool.query_(sql3)
    salaryData = pool.query_(sql4)

    pool.dispose()
    return educationData, cityData, workYearData, industryData, salaryData

def showView():
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    educationData, cityData, workYearData, industryData, salaryData = getData()
    educationCount = list()
    educationList = list()
    cityCount = list()
    cityList = list()
    workYearCount = list()
    workYearList = list()
    industry = ""

    for i in educationData:
        educationList.append(i[0])
        educationCount.append(i[1])

    for i in cityData:
        cityList.append(i[0])
        cityCount.append(i[1])

    for i in workYearData:
        workYearList.append(i[0])
        workYearCount.append(i[1])

    for i in industryData:
        industry = industry + i[0] + ' '

    fig = plt.figure()
    fig2 = plt.figure()
    ax1 = fig.add_subplot(221)
    ax1.set_title('职位学历分布图')
    ax1.pie(educationCount, labels=educationList, autopct='%1.1f%%')    #学历分布饼状图
    ax2 = fig.add_subplot(222)
    ax2.set_title('职位城市分布图')
    ax2.pie(cityCount, labels=cityList, autopct='%1.1f%%')              #城市饼状图
    ax3 = fig.add_subplot(223)
    ax3.set_title('工作经验分布图')
    ax3.pie(workYearCount, labels=workYearList, autopct='%1.1f%%')      #工作经验饼状图
    # ax4 = fig.add_subplot(224)
    # ax4.bar(range(len(industryList)), industryCount, tick_label=industryList)
    ax5 = fig2.add_subplot(111)                                         #行业词云图
    ax5.set_title('行业词云图')
    mywc = wordcloud.WordCloud(width=1200, height=900, font_path="Deng.ttf", collocations=False, min_font_size=25).generate(industry)
    ax5.imshow(mywc)

    plt.ion()
    # plt.pause(1)
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    showView()