import pyecharts.charts
import pypinyin
import streamlit as st
import streamlit_echarts as st_echarts
import requests
from bs4 import BeautifulSoup
import jieba
from pyecharts.charts import Bar, WordCloud,Map
# steamlit中嵌入pyechats前端代码
import streamlit.components.v1 as components
from pyecharts import options as opts
# 汉字转拼音
from pypinyin import pinyin, Style
import gopup as gp
import re # 正则表达式库
# from nltk.corpus import stopwords # 停用词库

def remove_stopwords(text):
    # stop_words = set(stopwords.words('english'))
    stop_words = {'my', 'not', 'couldn', "mustn't", 'and', 'why', "weren't", 'its', 'same', 'hasn', 'again', 'being', "you'd", 'hers', 'don', "wasn't", 'more', "isn't", 'when', 'ma', 'were', 't', 'by', 're', "couldn't", 'we', 'that', "hadn't", 'she', 'down', 's', 'themselves', 'each', 'because', 'having', "you're", 'herself', 'a', 'those', 'them', 'above', 'how', 'only', 'shouldn', 've', 'itself', 'be', 'out', 'up', 'until', 'whom', 'yours', 'did', 'our', 'through', 'below', 'won', "won't", 'nor', 'now', 'off', 'while', "should've", 'wouldn', 'll', 'needn', "mightn't", 'didn', 'hadn', 'an', "wouldn't", 'from', 'in', 'all', 'yourselves', 'both', 'after', 'he', 'few', "you've", 'at', 'these', 'him', "aren't", "haven't", 'his', 'has', 'you', 'myself', 'aren', 'with', 'it', 'will', 'any', "shan't", 'than', 'some', 'haven', 'mustn', "shouldn't", 'theirs', 'been', 'their', 'about', 'on', "you'll", 'm', 'into', 'himself', 'yourself', 'doesn', 'are', 'such', 'your', 'against', 'to', 'mightn', 'doing', 'further', 'over', 'as', 'they', 'during', 'so', 'there', 'between', 'which', 'once', 'me', 'had', 'here', 'under', 'most', 'can', 'but', 'before', 'wasn', "that'll", 'd', 'just', "she's", "it's", 'other', 'have', 'no', 'i', "didn't", 'her', "don't", 'ours', 'very', 'the', 'should', 'too', "needn't", 'if', 'of', 'was', 'isn', 'own', 'what', 'where', 'ourselves', 'or', 'this', 'ain', 'then', 'for', 'weren', 'do', 'who', 'is', "hasn't", "doesn't", 'shan', 'am', 'o', 'y', 'does'}
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

# 使用正则表达式去掉标点符号
def remove_punctuations(text):
    # 使用正则表达式去掉标点符号
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return cleaned_text

def crawlingFn(url):
    # 发送GET请求并获取响应
    response = requests.get(url)
    # 确定编码
    encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
    # 使用BeautifulSoup解析响应文本
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding=encoding)
    # 获取文本内容
    text_content = soup.text
    # 对文本内容清洗
    text_content = remove_punctuations(text_content)
    text_content = remove_stopwords(text_content)
    return text_content
def page_home():
    # 这是主页面
    st.title('欢迎使用网页词频可视化工具! 👋')
    input_url= st.text_input("Enter URL:")
    if input_url.strip() == "":
        return
    else:
        text = crawlingFn(input_url)
        words = jieba.lcut(text)  # 使用精确模式对文本进行分词
        word_counts = {}
        # 获取词频字典
        for word in words:
            if len(word) == 1:
                continue
            else:
                word_counts[word] = word_counts.get(word, 0) + 1
        # 字典按值从大到小取前20个
        word_counts_20 = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20])
        bar = Bar()
        val = list(map(int, word_counts_20.values()))
        wordList = list(word_counts_20.keys())
        bar.add_xaxis(wordList)
        bar.add_yaxis("关键词", val)
        # 设置 x 轴标签旋转角度为 45 度
        bar.set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45))
        )
        # 使用 st_echarts.st_pyecharts() 方法将图表渲染到 Streamlit 中
        st_echarts.st_pyecharts(bar)
def page_ciyun():
    # 词云数据
    st.title('欢迎使用网页词频可视化工具! 👋')
    input_url = st.text_input("Enter URL:")
    if input_url.strip() == "":
        return
    else:
        text = crawlingFn(input_url)
        words = jieba.lcut(text)  # 使用精确模式对文本进行分词
        word_counts = {}
        # 获取词频字典
        for word in words:
            if len(word) == 1:
                continue
            else:
                word_counts[word] = word_counts.get(word, 0) + 1
        # 字典按值从大到小取前20个
        word_counts_20 = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20])
        # [()]
        word_list = [(x,y) for x,y in word_counts_20.items()]
        wordcloud = WordCloud()
        wordcloud.add("", word_list, word_size_range=[20, 100])
        st_echarts.st_pyecharts(wordcloud)
def page_pie():
    # 饼状图页面
    st.title('欢迎使用网页词频可视化工具! 👋')
    input_url = st.text_input("Enter URL:")
    if input_url.strip() == "":
        return
    else:
        text = crawlingFn(input_url)
        words = jieba.lcut(text)  # 使用精确模式对文本进行分词
        word_counts = {}
        # 获取词频字典
        for word in words:
            if len(word) == 1:
                continue
            else:
                word_counts[word] = word_counts.get(word, 0) + 1
        # 字典按值从大到小取前20个
        word_counts_20 = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20])
        # [()]
        word_list = [(x,y) for x,y in word_counts_20.items()]
        pie = pyecharts.charts.Pie()
        pie.add("",word_list, radius=["40%", "75%"])
        pie.set_global_opts(title_opts=opts.TitleOpts(title=""))
        st_echarts.st_pyecharts(pie)
def page_broken():
    # 这是折线图
    st.title('欢迎使用网页词频可视化工具! 👋')
    input_url= st.text_input("Enter URL:")
    if input_url.strip() == "":
        return
    else:
        text = crawlingFn(input_url)
        words = jieba.lcut(text)  # 使用精确模式对文本进行分词
        word_counts = {}
        # 获取词频字典
        for word in words:
            if len(word) == 1:
                continue
            else:
                word_counts[word] = word_counts.get(word, 0) + 1
        # 字典按值从大到小取前20个
        word_counts_20 = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20])
        val = list(map(int, word_counts_20.values()))
        wordList = list(word_counts_20.keys())
        line = pyecharts.charts.Line()
        line.add_xaxis(wordList)
        line.add_yaxis("关键词",val)
        # 设置 x 轴标签旋转角度为 45 度
        line.set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45))
        )
        st_echarts.st_pyecharts(line)
def page_point():
    # 这是折线图
    st.title('欢迎使用网页词频可视化工具! 👋')
    input_url= st.text_input("Enter URL:")
    if input_url.strip() == "":
        return
    else:
        text = crawlingFn(input_url)
        words = jieba.lcut(text)  # 使用精确模式对文本进行分词
        word_counts = {}
        # 获取词频字典
        for word in words:
            if len(word) == 1:
                continue
            else:
                word_counts[word] = word_counts.get(word, 0) + 1
        # 字典按值从大到小取前20个
        word_counts_20 = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20])
        val = list(map(int, word_counts_20.values()))
        wordList = list(word_counts_20.keys())
        size_data = [10, 20, 30, 40, 50, 60]
        es = pyecharts.charts.EffectScatter()
        es.add_xaxis(wordList)
        es.add_yaxis("关键词",val,symbol_size=size_data)
        # 设置 x 轴标签旋转角度为 45 度
        es.set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45))
        )
        st_echarts.st_pyecharts(es)
def page_movie():
    df_index = gp.douban_movie_list()
    df_index2 = gp.douban_week_praise_list()
    dataList = list()
    for item in df_index2.iterrows():
        temList = list()
        temList.append(item[1][0])
        temList.append(item[1][3])
        temList.append(item[1][2])
        temList.append(item[1][1])
        dataList.append(temList)
    dataList = sorted(dataList, key=lambda x: x[1])
    titleList = list()
    scoreList = list()
    imgList = list()
    linkList = list()
    for item in df_index.iterrows():
        # print(item[1][2],item[1][0],item[1][5])
        titleList.append(item[1][2])
        scoreList.append(float(item[1][0]))
        imgList.append(item[1][4])
        linkList.append(item[1][5])
    bar = Bar()
    bar.add_xaxis(titleList)
    bar.add_yaxis("豆瓣评分", scoreList)
    # 设置 x 轴标签旋转角度为 45 度
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=20))
    )
    st.title("豆瓣新片榜")
    st_echarts.st_pyecharts(bar)
    expander_1 = st.expander('观看入口：')
    # 循环遍历图片列表并显示图片
    for i in range(len(imgList)):
        # unsafe_allow_html允许write插入html标签
        expander_1.write(f"<a href={linkList[i]}>{titleList[i]}</a>", unsafe_allow_html=True)
    st.title("豆瓣一周口碑榜")
    headers = ['影片', '排名', '趋势',"链接"]
    # 编写HTML代码，包括表头和数据行
    table_html = f"<table><thead><tr>{''.join(f'<th>{header}</th>' for header in headers)}</tr></thead><tbody>"
    for row in dataList:
        table_html += f"<tr>{''.join(f'<td>{data}</td>' for data in row)}</tr>"
    table_html += "</tbody></table>"
    # 使用st.write()函数显示自定义表格
    st.write(table_html, unsafe_allow_html=True)
def page_weather():
    # openweathermap api-key
    api_key = "12b2817fbec86915a6e9b4dbbd3d9036"

    def get_weather(city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        return data

    def get_temperatureAll():
        # 使用pypinyin库将中文省份名称转换为对应的拼音形式，并去掉代表“省”、“市”等的后缀，最终得到了一个包含所有省份拼音名称的列表
        provinces = ['北京市', '天津市', '河北省', '山西省', '吉林省', '黑龙江省', '上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省',
                     '湖北省', '湖南省', '广东省', '海南省', '重庆市', '四川省', '贵州省', '西藏自治区', '陕西省', '甘肃省', '青海省', '新疆', '香港特别行政区',
                     '台湾省']
        # provinces = ['北京市', '天津市', '河北省', '山西省', '吉林省', '黑龙江省',]
        temperature_data = []
        for i in range(len(provinces)):
            # 去除后缀
            province_name = provinces[i].replace('自治区', '').replace('特别行政区', '').replace('省', '').replace('市', '')
            # 将中文转为拼音
            city_pinyin = ''.join(p[0] for p in pinyin(province_name, style=Style.NORMAL))
            temperature = get_weather(city_pinyin)["main"]["temp"]
            # 要获取温度的城市列表
            temperature_data.append((provinces[i], temperature))
        return temperature_data

    def visualize_weather(data):
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        bar = (
            Bar()
            .add_xaxis(["温度", "湿度", "风速"])
            .add_yaxis("天气数据", [temperature, humidity, wind_speed])
            .set_global_opts(title_opts=opts.TitleOpts(title="中国天气可视化"))
        )
        return bar

    def main():
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.title("中国天气可视化")
        city = st.text_input("请输入城市名：")
        if st.button("查询"):
            pinyin_list = pypinyin.lazy_pinyin(city)
            pinyin_city = ''.join(pinyin_list)
            weather_data = get_weather(pinyin_city)
            bar = visualize_weather(weather_data)
            st_echarts.st_pyecharts(bar)
        # 数据示例
        # data = [("北京市", 111)]

        data = get_temperatureAll()

        map_chart = (
            Map()
            .add("数据系列名称", data, "china")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts(title="中国各地温度"),
                visualmap_opts=opts.VisualMapOpts(
                    max_=300,
                    min_=0,
                    is_piecewise=True,
                    pieces=[
                        {"min": -273.15, "max": 0},
                        {"min": 0, "max": 100},
                        {"min": 101, "max": 200},
                        {"min": 201, "max": 300},
                    ]

                ),
                tooltip_opts=opts.TooltipOpts(formatter="{b}: {c}"),
            )
        )

        cities = [
            "北京",
            "上海",
            # 其他城市...
        ]

        for city in cities:
            try:
                weather_data = get_weather(city)
                temperature = weather_data["main"]["temp"]
                map_chart.add("", [(city, temperature)])
            except:
                pass

        htmlcode = map_chart.render_embed()  # 嵌入式渲染
        components.html(htmlcode, width=1000, height=600)
    main()


def main():
    # 设置初始页面为Home
    session_state = st.session_state
    session_state['page'] = '条形图'
    # 导航栏
    page = st.sidebar.selectbox('导航栏', ['条形图', '词云','饼状图','折线图','散点图','影视推荐','国内天气'])

    if page == '条形图':
        # 在Home页面中显示数据和功能组件
        page_home()
    elif page == '词云':
        # 在About页面中显示数据和功能组件
        page_ciyun()
    elif page == '饼状图':
        # 在About页面中显示数据和功能组件
        page_pie()
    elif page == '折线图':
        page_broken()
    elif page == '散点图':
        page_point()
    elif page == '影视推荐':
        page_movie()
    elif page == "国内天气":
        page_weather()

if __name__ == '__main__':
    main()