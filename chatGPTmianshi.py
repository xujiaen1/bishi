# -*- codeing = utf-8 -*-
# @time : 2023/6/10
# @Author : 徐家恩
# @File : chatGPTmianshi.py
# @Software : PyCharm
import openai
import pandas as pd
import re
import spacy
from typing import List
# 设置 OpenAI API 密钥
openai.api_key = "OpenAI API 密钥"

# 加载英语模型
nlp = spacy.load("en_core_web_sm")


# 生成面试问题
def generate_questions(name: str, company: str, job_title: str, skills: List[str],
                       field: str, experience: int, education: str,
                       num_questions: int = 10) -> List[str]:
    # 将所有技能拼接成一个字符串
    skills_str = ' '.join([skill.lower() for skill in skills])

    # 根据职位推断应该问的问题类型
    if "engineer" in job_title.lower():
        question_prefix = "How did you develop your technical skills?"
    elif "designer" in job_title.lower():
        question_prefix = "Can you walk me through your design process?"
    elif "data scientist" in job_title.lower():
        question_prefix = "What was the most challenging data science project you worked on and how did you solve it?"
    else:
        question_prefix = "Tell me about your previous experience."

    # 构建 OpenAI GPT 的生成文本所需的 prompt
    prompt = f"Interview questions for {name} at {company}. " \
             f"{question_prefix} " \
             f"What skills do you have that are relevant to the {field} field? " \
             f"How many years of experience do you have in {field}? " \
             f"What is your highest level of education? " \
             f"Skills: {skills_str}. " \
             f"Experience: {experience} years. " \
             f"Education: {education}. "

    # 使用 OpenAI GPT 模型生成问题
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt,
                                        temperature=0.7, max_tokens=150, n=num_questions)

    # 将生成的问题保存到一个列表中并返回
    questions = [choice.text.strip() for choice in response.choices]
    return questions


# 评估答案的质量
def evaluate_answer(answer: str, skills: List[str], job_title: str) -> float:
    # 将技能列表中的所有技能以及工作职位中的关键词作为评估答案的关键词
    keywords = skills + re.findall(r'\w+', job_title.lower())
    total_keywords_count = len(keywords)
    if total_keywords_count == 0:
        return 0.0

    # 对答案进行分词和标记
    doc = nlp(answer.lower())
    answer_tokens = [token for token in doc if not token.is_stop and token.is_alpha]

    # 对关键词在答案中出现的次数求和
    keyword_count = sum([1 for token in answer_tokens if token.text in keywords])

    # 如果没有关键词出现在答案中，则返回 0
    if keyword_count == 0:
        return 0.0

    # 除以关键词总数后返回百分比得分
    return round((keyword_count/total_keywords_count)*100)


# 简历评估
def evaluate_resume(resume: str, skills: List[str], job_title: str) -> str:
    # 生成针对技能和职位的关键词列表
    keywords = skills + re.findall(r'\w+', job_title.lower())

    # 对简历进行分词和标记
    doc = nlp(resume.lower())
    resume_tokens = [token for token in doc if not token.is_stop and token.is_alpha]

    # 对关键词在简历中出现的次数求和
    keyword_count = sum([1 for token in resume_tokens if token.text in keywords])

    # 如果没有关键词出现在简历中，则返回建议修改
    if keyword_count == 0:
        return "Improve your resume by highlighting your relevant skills and experience."

    # 根据关键词出现的次数作出评估
    if keyword_count <= 2:
        return "Your resume shows room for improvement. Consider highlighting your skills and relevant experience more clearly."
    elif keyword_count <= 4:
        return "Your resume is good, but could be stronger. Consider expanding on your skills and highlighting relevant projects you’ve worked on."
    else:
        return "Your resume looks great! You appear to have all the necessary skills and experience."


# 生成提纲
def generate_outline(text: str) -> List[str]:
    # 构建 OpenAI GPT 的生成文本所需的 prompt
    prompt = f"Generate an outline of the following text: {text}"

    # 使用 OpenAI GPT 模型生成提纲
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt,
                                        temperature=0.7, max_tokens=150, n=5)

    # 将生成的提纲保存到一个列表中并返回
    outline = [choice.text.strip() for choice in response.choices]
    return outline