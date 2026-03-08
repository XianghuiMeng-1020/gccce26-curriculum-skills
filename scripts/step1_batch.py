import json
import time
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- 1. 引入你提供的 API 函数 (简化版，假设放在同一文件或 import 进来) ---
# 请确保你的 requestGPT4 函数定义在这里是可用的
# from your_api_script import requestGPT4 
from tools import requestGPT4

# 为了演示，我这里保留一个简单的 Wrapper
def call_llm_api(course_desc):
    """
    针对你的 requestGPT4 函数封装的 Prompt 构建器
    """
    instruction = """
    You are an expert Curriculum Analyst. Analyze the provided course description to extract professional skills.
    
    Structure your answer strictly as a JSON object with three keys:
    1. "tools": Specific software, languages, or frameworks (e.g., Python, SPSS, SQL, Tableau).
    2. "hard_skills": Technical or functional skills (e.g., Statistical Modeling, Data Mining, Policy Analysis).
    3. "soft_skills": Interpersonal or management skills (e.g., Leadership, Communication, Critical Thinking).
    
    Rules:
    - Extract ONLY from the text provided. Do not hallucinate.
    - Normalize terms (e.g., use "Python" instead of "Python programming").
    - If a category is empty, return an empty list [].
    - Output ONLY the JSON string, no markdown formatting.
    """
    
    # 你的 AK
    ak = "" 
    model = '' # 使用你定义的 best_model
    
    try:
        # 调用你的 requestGPT4 函数
        # 注意：这里假设 requestGPT4 已经在作用域内
        response = requestGPT4(instruction, course_desc, ak, 0.2, model)
        
        # 清洗返回结果，防止 LLM 加 Markdown 符号
        response = response.replace('```json', '').replace('```', '').strip()
        return json.loads(response)
    except Exception as e:
        print(f"Error parsing JSON or API fail: {e}")
        return {"tools": [], "hard_skills": [], "soft_skills": []}

# --- 2. 主处理流程 ---

def extract_all_skills(input_json_data):
    """
    输入你的 raw json data，输出带有 extracted_skills 的列表
    """
    all_courses = []
    
    # 展平数据结构：加上 Program 标签
    for course in input_json_data['BASc']:
        course['program'] = 'BASc(SDS)'
        all_courses.append(course)
    
    for course in input_json_data['BSc']:
        course['program'] = 'BSc(IM)'
        all_courses.append(course)
        
    results = []
    
    # 使用线程池并发请求 (参考你的 manyidu_pipeline)
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 提交任务
        future_to_course = {
            executor.submit(call_llm_api, course['desc']): course 
            for course in all_courses
        }
        
        for future in tqdm(as_completed(future_to_course), total=len(all_courses), desc="Extracting Skills"):
            course_original = future_to_course[future]
            try:
                skills = future.result()
                # 将提取结果合并回课程对象
                course_original['skills'] = skills
                results.append(course_original)
            except Exception as e:
                print(f"Failed task: {e}")
                course_original['skills'] = {"tools": [], "hard_skills": [], "soft_skills": []}
                results.append(course_original)
                
    return results

# --- 运行入口 ---
if __name__ == "__main__":
    import os
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _repo_root = os.path.dirname(_script_dir)
    _data_dir = os.path.join(_repo_root, "data")
    pdf_path = os.path.join(_data_dir, "pdf_data.json")
    out_path = os.path.join(_data_dir, "course_skills_extracted.json")
    # 1. 加载你的数据
    with open(pdf_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    # 2. 执行提取
    print("开始提取技能...")
    processed_data = extract_all_skills(raw_data)
    # 3. 保存结果供下一步分析
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=4, ensure_ascii=False)
    print("提取完成，结果已保存为", out_path)