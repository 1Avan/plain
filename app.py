import pyecharts.charts
import streamlit as st
import streamlit_echarts as st_echarts
import requests
from bs4 import BeautifulSoup
import jieba
from pyecharts.charts import Bar, WordCloud
from pyecharts import options as opts
import re # 正则表达式库
from nltk.corpus import stopwords # 停用词库

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
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
def main():
    # 设置初始页面为Home
    session_state = st.session_state
    session_state['page'] = '条形图'
    # 导航栏
    page = st.sidebar.radio('导航栏', ['条形图', '词云','饼状图','折线图','散点图'])

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

if __name__ == '__main__':
    main()