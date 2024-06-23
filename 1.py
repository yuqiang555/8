#这段代码的主要目的是创建一个网页应用，用户可以通过选择不同的迪士尼园区和月份，
# 来查看该园区的游客评价数据。代码首先加载了三个不同地区迪士尼乐园的数据和一个评价样本数据，
# 然后通过Streamlit库创建了一个交互式的网页界面。
# 用户可以在界面上选择园区和月份，代码会根据用户的选择展示对应的好评率和差评率曲线，以及所选月份的评价分布饼图。

# 导入需要的库
import streamlit as st  # Streamlit是用来创建网页应用的库
import pandas as pd  # Pandas是用来处理表格数据的库
import matplotlib.pyplot as plt  # Matplotlib是用来画图的库

# 设置图表中的字体为微软雅黑，这样图表中就可以显示中文了
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

# 定义一个函数来加载数据
def load_data():
    # 读取加州迪士尼的数据
    california_data = pd.read_excel('Disneyland_California.xlsx')
    # 读取香港迪士尼的数据
    hongkong_data = pd.read_excel('Disneyland_HongKong.xlsx')
    # 读取巴黎迪士尼的数据
    paris_data = pd.read_excel('Disneyland_Paris.xlsx')
    # 读取随机抽取的评价样本数据
    reviews_data = pd.read_excel('Sampled_DisneylandReviews.xlsx')
    # 返回一个包含所有数据的字典
    return {'California': california_data, 'HongKong': hongkong_data, 'Paris': paris_data}, reviews_data

# 调用函数，把数据加载到变量里
data, reviews_data = load_data()

# 设置Streamlit应用的标题
st.title("Disneyland 游玩建议")

# 在应用中显示一张图片
st.image('pic.png')

# 让用户选择一个迪士尼园区
region = st.selectbox("选择园区", ["California", "HongKong", "Paris"])

# 让用户选择一个月份
month = st.selectbox("选择月份", data[region]['Month'].unique())

# 根据用户的选择，获取对应的数据
region_data = data[region]

# 准备画图
fig, ax = plt.subplots(1, 2, figsize=(14, 6))  # 创建一个画布，上面有两个子图

# 在第一个子图上画好评率和差评率的曲线
ax[0].plot(region_data['Month'], region_data['positive_rate'], label='好评率', marker='o')  # 画好评率曲线
ax[0].plot(region_data['Month'], region_data['negative_rate'], label='差评率', marker='o')  # 画差评率曲线
ax[0].set_xlabel('月份')  # 设置X轴标题
ax[0].set_ylabel('百分比')  # 设置Y轴标题
ax[0].set_title(f'{region}园区 评价曲线')  # 设置图表标题
ax[0].legend()  # 显示图例

# 在第二个子图上画选择月份的评价分布饼图
month_data = region_data[region_data['Month'] == month].iloc[0]  # 获取选择月份的数据
labels = '正面评价', '负面评价', '中立评价'  # 饼图的标签
sizes = [month_data['positive'], month_data['negative'], month_data['neutral']]  # 饼图的每个部分的大小
colors = ['#ff9999','#66b3ff','#99ff99']  # 饼图的每个部分的颜色
explode = (0.1, 0, 0)  # 让正面评价部分突出显示

ax[1].pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',  # 画饼图
        shadow=True, startangle=140)  # 设置饼图的阴影和起始角度
ax[1].axis('equal')  # 确保饼图是圆的
ax[1].set_title(f'{month} 月份评价分布')  # 设置图表标题

# 在 Streamlit 页面中显示图表
st.pyplot(fig)

# 显示随机评论
st.subheader("随机抽取的评论")

# 筛选评论数据
# 从reviews_data中选择与用户选定的园区和月份匹配的评论
filtered_reviews = reviews_data[(reviews_data['Branch'] == 'Disneyland_' + region) & (reviews_data['Month'] == month)]
# 从筛选后的评论中随机抽取评论
# 使用sample函数随机选择最多10条评论，如果评论数量少于10条，则选择所有评论
# random_state=42确保每次运行代码时都能得到相同的随机结果
random_reviews = filtered_reviews.sample(min(10, len(filtered_reviews)), random_state=42)

# 显示评论
# 遍历随机选择的评论列表
for i, review in enumerate(random_reviews['Review_Text'].tolist()):
    st.write(f"{i+1}. {review}")

# 显示 Excel 文件内容
excel_file_path = 'recommended_reviews_new_user_670801368.xlsx'
excel_data = pd.read_excel(excel_file_path)
#显示得到的surprise推荐的高分评论
st.subheader("迪士尼高分评论")
st.write(excel_data)




