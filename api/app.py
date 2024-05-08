# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 17:22:00 2023

@author: C
"""

from openai import OpenAI
import gradio as gr
from gradio.components import Textbox
import os
import requests
import json
# import pandas as pd
import tempfile



BASE_URL = os.getenv('baseurl')
API_SECRET_KEY = os.getenv('apikey')


# 定义函数-内容生成模块

def 内容生成(password, input1, input2, count):

    client = OpenAI(api_key=password, base_url=BASE_URL)

    query = "这是我的论文标题：{title}\n我现在要进行如下章节的写作：{section}\n请给我逻辑清晰、表述规范的论文段落，字数大约为{count}字。直接给出论文段落即可，不必说除了论文段落以外的任何信息。".format(title = input1, section = input2, count = count)

    try:
        resp = client.chat.completions.create(
                        model="gpt-4-0125-preview",
                        messages=[
                            {"role": "system", "content": "你现在是一名专业的经管领域的教授，你要进行论文写作。"},
                            {"role": "user", "content": query},
                        ],
                        n = 1,
                        #temperature=0.5,
                        #frequency_penalty=0, #frequency_penalty越高，回答重复词越少
                        presence_penalty=-1, #presence_penalty越低，回答越不跑题
                        stream = True,
                )
                
        reply = ""
        for chunk in resp:
            if chunk.choices[0].delta.content is not None:
                reply = reply+chunk.choices[0].delta.content
                yield reply
    except Exception as e:
        yield reply + e


# 定义函数-内容扩写模块

def 内容扩写(password, input1):

    client = OpenAI(api_key=password, base_url=BASE_URL)

    query = "这是我的论文中的一段内容，请你把这段内容进行扩写，把这段内容描述得更详细，必须保持句子原来的意思不变。论文段落为：" + input1
    
    try:
        resp = client.chat.completions.create(
                model="gpt-4-0125-preview",   # 模型名字要从上一步获取得到
                        messages=[
                            {"role": "system", "content": "你现在是一名专业的经管领域的教授，你要进行论文写作。"},
                            {"role": "user", "content": query},
                        ],
                        n = 1,
                        #temperature=0.5,
                        #frequency_penalty=0, #frequency_penalty越高，回答重复词越少
                        presence_penalty=0, #presence_penalty越低，回答越不跑题
                        stream = True,
                )
        
        print(resp)
        
        #流式响应
        reply = ""
        for chunk in resp:
            if chunk.choices[0].delta.content is not None:
                reply = reply+chunk.choices[0].delta.content
                yield reply


    except Exception as e:

        yield reply + e


# 定义函数-文献综述模块
def 文献综述(password, theme, file_obj):
    # print('临时文件夹地址：{}'.format(tmpdir))
    # print('上传文件的地址：{}'.format(file_obj.name)) # 输出上传后的文件在gradio中保存的绝对地址
    pd = []
    try:
        df = pd.read_excel(file_obj.name)
    except:
        return "文件类型错误，请上传Excel文件（后缀名为.xlsx或.xls）。"

    try:
        df = df[['作者', '年份', '标题', '摘要']]
    except:
        return "列名设置错误，请检查你的excel文件列名是否符合模板规范。\n\n规范列名为：['作者', '年份', '标题', '摘要']\n\n当前列名为：" + str(list(df.columns))

    df_str = str(df.to_dict(orient = "records"))

    client = OpenAI(api_key=password, base_url=BASE_URL)
    query = "以下是我整理的文献，包括每篇文献的作者，年份，标题，摘要。这些文献的主题是：{theme}。请帮我生成一篇关于这些文献的综述，要求字数不少于1000字。这个综述必须包括每一篇文献，不得遗漏任何一篇文献。在综述文献的时候，要对文献进行归纳整理，可以将这些文献分成几种类型，在每个类型中总结文献的共性。在提到相关文献时必须附带文章的作者和年份。以下是整理的文献：\n\n{content}".format(content = df_str, theme = theme)
    
    try:
        resp = client.chat.completions.create(
                model="gpt-4-0125-preview",   # 模型名字要从上一步获取得到
                        messages=[
                            {"role": "system", "content": "你现在是一名专业的经管领域的教授，你要进行论文写作。"},
                            {"role": "user", "content": query},
                        ],
                        n = 1,
                        presence_penalty=0, #presence_penalty越低，回答越不跑题
                        stream = True,
                )
        
        print(resp)
        
        #流式响应
        reply = ""
        for chunk in resp:
            if chunk.choices[0].delta.content is not None:
                reply = reply+chunk.choices[0].delta.content
                yield reply


    except Exception as e:

        yield reply + e


# 定义函数-内容提炼模块
def 内容提炼(password, content, theme):

    client = OpenAI(api_key=password, base_url=BASE_URL)
    query = "以下是我的开题报告内容，请你根据报告中的内容，从这份报告中提炼出：{theme}，每部分内容写不超过300字即可。以下是我的开题报告：\n\n{content}".format(content = content, theme = theme)
    
    try:
        resp = client.chat.completions.create(
                model="gpt-4-0125-preview",   # 模型名字要从上一步获取得到
                        messages=[
                            {"role": "system", "content": "你现在是一名专业的经管领域的教授，你要进行论文写作。"},
                            {"role": "user", "content": query},
                        ],
                        n = 1,
                        presence_penalty=0, #presence_penalty越低，回答越不跑题
                        stream = True,
                )
        
        print(resp)
        
        #流式响应
        reply = ""
        for chunk in resp:
            if chunk.choices[0].delta.content is not None:
                reply = reply+chunk.choices[0].delta.content
                yield reply


    except Exception as e:

        yield reply + e



# 定义函数-额度查询模块
def 额度查询(key):
    url_usage = 'https://qianduduo.hermapi.com/api/total?key='
    url_usage = url_usage + key
    response = requests.get(url_usage)
    if response.status_code == 200:
        usage_balance = json.loads(response.text)['total_usage']/100
        usage_balance = round(usage_balance, 4)
        usage_balance = int(usage_balance*25000)
    else:
        return('请求失败，请检查网络连接或密码是否正确')


    url_total = 'https://qianduduo.hermapi.com/api/balance?key='
    url_total = url_total + key
    response = requests.get(url_total)
    if response.status_code == 200:
        total_balance = json.loads(response.text)['soft_limit_usd']
        total_balance = round(total_balance, 4)
        total_balance = int(total_balance*25000)
    else:
        return('请求失败，请检查网络连接或密码是否正确')

    remain_balance = total_balance - usage_balance

    return {
        '总额度': total_balance,
        '已用额度': usage_balance,
        '剩余额度': remain_balance
    }




def start_web():
  ##% 制作界面
  #模块1-生成段落
  input_password_app1 = Textbox(lines=1, label="请输入密码")
  input1_app1 = Textbox(lines=1, label="请输入你的论文标题，例如“上市公司财务造假识别研究——以易见股份为例”")
  input2_app1 = Textbox(lines=2, label="请输入你要写作的章节，例如“研究背景与动机”")
  output1_app1 = Textbox(lines=12, label="来自【凯泽助手】的生成段落")
  slider_字数控制 = gr.Slider(300, 1500, step = 100, value=300, label="字数", info="选择生成的字数，范围在300-1500之间")
  with gr.Blocks() as app1: 
      gr.Interface(fn=内容生成, inputs=[input_password_app1, input1_app1, input2_app1, slider_字数控制], outputs=output1_app1, title="段落生成",
              # description="凯泽论文助手",
              theme=gr.themes.Default(),
              flagging_dir=r"D:/",
              #concurrency_limit=10,
              #template=custom_template
              )


  #模块2-扩写段落
  input_password_app2 = Textbox(lines=1, label="请输入密码")
  input1_app2 = Textbox(lines=8, label="请输入你要扩写的论文段落")
  output1_app2 = Textbox(lines=12, label="来自【凯泽助手】的扩写段落")
  with gr.Blocks() as app2: 
      gr.Interface(fn=内容扩写, inputs=[input_password_app2, input1_app2], outputs=output1_app2, title="段落扩写",
              # description="凯泽论文助手",
              theme=gr.themes.Default(),
              flagging_dir=r"D:/",
              #concurrency_limit=10,
              #template=custom_template
              )


  #模块3-文献综述
  global tmpdir
  with tempfile.TemporaryDirectory(dir='.') as tmpdir:
      # 定义输入和输出
      input_password_app3 = Textbox(lines=1, label="请输入密码")
      input1_app3 = Textbox(lines=1, label="请输入文献综述的主题。例如：财务造假的识别与预测")
      input2_app3 = gr.components.File(label="上传文件")
      output1_app3 = gr.Textbox(label="输出内容")

      # 创建 Gradio 应用程序g
      app3 = gr.Interface(fn=文献综述, 
                        inputs=[input_password_app3, input1_app3, input2_app3], 
                        outputs=output1_app3, 
                        title="文献综述",
                        description="使用方法：下载模板文件，按要求整理好excel文件后，上传文件生成文献综述。\n\n模板文件[点击此处](https://www.modelscope.cn/api/v1/studio/chenmh/KaizePaperAssistant/repo?Revision=master&FilePath=%E6%96%87%E7%8C%AE%E7%BB%BC%E8%BF%B0%E6%95%B4%E7%90%86%E6%A8%A1%E6%9D%BF.xlsx)下载。\n\n建议：不要一次性将文献全部导入，而是将文献的主题归纳整理好之后，分批次导入。例如将文献分为：财务造假的识别与预测、财务造假的动因与影响因素、财务造假的经济后果与监管措施，分三次生成综述。"
      )



  #模块4-报告内容提炼
  input_password_app4 = Textbox(lines=1, label="请输入密码")
  input1_app4 = Textbox(lines=8, label="请输入你要提炼的开题报告全文")
  input2_app4 = Textbox(lines=2, label="请输入提炼的主题（多个主题可用逗号隔开）")
  output1_app4 = Textbox(lines=12, label="来自【凯泽助手】的提炼内容")
  with gr.Blocks() as app4: 
      gr.Interface(fn=内容提炼, inputs=[input_password_app4, input1_app4, input2_app4], outputs=output1_app4, title="开题报告内容提炼（v0.1测试版）",
              # description="凯泽论文助手",
              theme=gr.themes.Default(),
              flagging_dir=r"D:/",
              #concurrency_limit=10,
              #template=custom_template
              )


  #模块5-余额查询
  input_password_app5 = Textbox(lines=1, label="请输入密码")
  output_app5 = Textbox(lines=1, label="额度查询结果")
  with gr.Blocks() as app5: 
      gr.Interface(fn=额度查询, inputs=input_password_app5, outputs=output_app5, title="额度查询",
              # description="凯泽论文助手",
              theme=gr.themes.Default(),
              flagging_dir=r"D:/",
              #concurrency_limit=10,
              #template=custom_template
              )
  demo = gr.TabbedInterface([app1, app2, app3, app4, app5],
                            tab_names=["段落生成", "段落扩写", "文献综述", "开题报告内容提炼（v0.1测试版）", "额度查询"],
                            title="凯泽教育论文写作助手",
                            #description = "AI时代，你不应该和汽车比赛跑，而是应该考个驾照。"
                            )

  demo.queue(concurrency_count=10).launch()

start_web()