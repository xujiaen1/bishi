# -*- codeing = utf-8 -*-
# @time : 2023/6/10
# @Author : 徐家恩
# @File : mianshiceshi.py
# @Software : PyCharm
questions = generate_questions("John", "ABC Company", "Data Scientist", ["Python", "Machine Learning"], "Data Science", 5, "Master's Degree")
print(questions)

answer = "I have 3 years of experience in Python programming and machine learning. I worked on a challenging data science project where we analyzed large datasets and built predictive models."
score = evaluate_answer(answer, ["Python", "Machine Learning"], "Data Scientist")
print(score)

resume = "I have a Master's Degree in Data Science and 5 years of experience working with Python and machine learning. I have worked on various data science projects and have a strong understanding of statistical modeling and data analysis techniques."
evaluation = evaluate_resume(resume, ["Python", "Machine Learning"], "Data Scientist")
print(evaluation)

text = "This is a sample text. It contains some important information. We need to generate an outline based on this text."
outline = generate_outline(text)
print(outline)
