import json
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib_venn import venn2, venn2_circles
import matplotlib.font_manager as fm

# ==========================================
# 1. 顶级会议作图标准配置 (CS Top Conf Style)
# ==========================================

# 设置字体：优先使用 Times New Roman (论文标准)，如果没有则回退到 Arial
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

# 解决中文显示问题 (如果环境中安装了 SimHei，否则可能会回退)
# 注意：在英文论文发表中，通常建议全英文标签。如果必须显示中文，请确保系统有对应字体。
plt.rcParams['axes.unicode_minus'] = False 

# 全局字体大小和线宽设置 (适合双栏论文)
SCALE = 1.5
plt.rcParams['font.size'] = 10 * SCALE
plt.rcParams['axes.labelsize'] = 11 * SCALE
plt.rcParams['axes.titlesize'] = 12 * SCALE
plt.rcParams['xtick.labelsize'] = 9 * SCALE
plt.rcParams['ytick.labelsize'] = 9 * SCALE
plt.rcParams['legend.fontsize'] = 9 * SCALE
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['grid.linestyle'] = '--'

# 定义黄蓝主色调 (Hex Codes for Academic Blue & Yellow)
# Blue: 稳重的深蓝 / Yellow: 醒目的金黄
COLOR_BLUE = "#2878B5"  # Academic Blue
COLOR_YELLOW = "#E6B71E" # Academic Gold/Yellow
COLOR_PALETTE = [COLOR_BLUE, COLOR_YELLOW]
PROGRAM_COLORS = {'BASc(SDS)': COLOR_BLUE, 'BSc(IM)': COLOR_YELLOW}

# ==========================================
# 2. 数据处理逻辑 (保持不变)
# ==========================================

def load_and_process_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    tools_list = []
    hard_skills_list = []
    soft_skills_list = []
    
    for _, row in df.iterrows():
        p = row['program']
        # 为了作图美观，统一 Program 名称的显示（可选）
        if p == 'BASc': p = 'BASc(SDS)'
        if p == 'BSc': p = 'BSc(IM)'
        
        for t in row['skills'].get('tools', []):
            tools_list.append({'program': p, 'skill': t.strip(), 'type': 'Tool'})
        for h in row['skills'].get('hard_skills', []):
            hard_skills_list.append({'program': p, 'skill': h.strip(), 'type': 'Hard Skill'})
        for s in row['skills'].get('soft_skills', []):
            soft_skills_list.append({'program': p, 'skill': s.strip(), 'type': 'Soft Skill'})
            
    all_skills_df = pd.DataFrame(tools_list + hard_skills_list + soft_skills_list)
    return df, all_skills_df

# ==========================================
# 3. 绘图函数 (高度定制化)
# ==========================================

def save_plot(filename):
    """保存为高清 PNG 和 PDF (矢量图，适合论文插入)"""
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _repo_root = os.path.dirname(_script_dir)
    plot_dir = os.path.join(_repo_root, "plot")
    os.makedirs(plot_dir, exist_ok=True)
    png_path = os.path.join(plot_dir, filename)
    pdf_path = os.path.join(plot_dir, filename.replace('.png', '.pdf'))
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    print(f"Saved: {png_path} & {pdf_path}")

def plot_top_tools_comparison(skills_df):
    """图表 1: Top 15 Tools (Horizontal Bar Chart)"""
    tools_df = skills_df[skills_df['type'] == 'Tool']
    tool_counts = tools_df.groupby(['program', 'skill']).size().reset_index(name='count')
    
    # 获取总频次最高的 Tools
    total_counts = tool_counts.groupby('skill')['count'].sum()
    top_tools = total_counts.nlargest(15).index.tolist()
    
    # 过滤并排序数据
    plot_data = tool_counts[tool_counts['skill'].isin(top_tools)].copy()
    # 将 skill 列转为 Categorical 类型以控制排序
    plot_data['skill'] = pd.Categorical(plot_data['skill'], categories=top_tools, ordered=True)
    
    plt.figure(figsize=(10, 6))
    
    # 使用 Seaborn 绘图
    ax = sns.barplot(
        data=plot_data, 
        y='skill', 
        x='count', 
        hue='program', 
        palette=PROGRAM_COLORS,
        edgecolor='black', # 增加边框增加质感
        linewidth=0.8,
        width=0.7
    )
    
    # 样式微调
    ax.set_title('Top 15 Technical Tools Comparison', fontweight='bold', pad=20)
    ax.set_xlabel('Frequency', fontweight='bold')
    ax.set_ylabel('') # Y轴标签如果是技能名，通常不需要"Skill Name"这个Label
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.legend(title=None, frameon=True, fancybox=False, edgecolor='black')
    sns.despine(left=True, bottom=False)
    
    save_plot('analysis_1_top_tools.png')
    plt.close()

def plot_venn_diagram(skills_df):
    """图表 2: Venn Diagram (Using Academic Colors)"""
    sds_skills = set(skills_df[skills_df['program'] == 'BASc(SDS)']['skill'].str.lower())
    im_skills = set(skills_df[skills_df['program'] == 'BSc(IM)']['skill'].str.lower())
    
    plt.figure(figsize=(6, 6))
    
    # 绘制韦恩图
    v = venn2([sds_skills, im_skills], set_labels=('BASc(SDS)', 'BSc(IM)'))
    
    # 自定义颜色 (设置 Alpha 透明度)
    if v.get_patch_by_id('10'):
        v.get_patch_by_id('10').set_color(COLOR_BLUE)
        v.get_patch_by_id('10').set_alpha(0.7)
    if v.get_patch_by_id('01'):
        v.get_patch_by_id('01').set_color(COLOR_YELLOW)
        v.get_patch_by_id('01').set_alpha(0.7)
    if v.get_patch_by_id('11'):
        # 交集部分颜色会自动混合，也可以手动指定一个中间色
        v.get_patch_by_id('11').set_color('#708090') # SlateGrey for intersection
        v.get_patch_by_id('11').set_alpha(0.5)
    
    # 绘制圆圈轮廓 (让图表更清晰)
    c = venn2_circles([sds_skills, im_skills], linestyle='-', linewidth=1.5, color='black')
    
    # 调整字体
    for text in v.set_labels:
        if text:
            text.set_fontsize(12)
            text.set_fontweight('bold')
    for text in v.subset_labels:
        if text:
            text.set_fontsize(14)
            text.set_color('white') # 内部数字用白色以增加对比度（如果背景深）或者黑色（如果背景浅）
            # 这里由于颜色较深，白色可能更好，或者黑色加粗
            text.set_color('black') 

    plt.title('Skill Set Overlap', fontweight='bold', pad=10)
    save_plot('analysis_2_skill_overlap.png')
    plt.close()

def plot_skill_category_distribution(skills_df):
    """图表 3: Grouped Bar Chart for Distribution"""
    dist_df = skills_df.groupby(['program', 'type']).size().reset_index(name='count')
    
    # 计算百分比
    total_counts = dist_df.groupby('program')['count'].transform('sum')
    dist_df['percentage'] = dist_df['count'] / total_counts
    
    plt.figure(figsize=(8, 6))
    
    # 定义类别的纹理或不同深浅的颜色，但这里我们用hue='type'，所以需要一套扩展的配色
    # 既然主要对比Program，我们这里还是用 x=Program, hue=Type 比较合适
    # 但为了保持黄蓝主色调，我们可以这样做：
    # BASc(SDS) 用不同深浅的蓝，BSc(IM) 用不同深浅的黄？
    # 或者，保持 Type 为 Hue，但选用冷暖对比色。
    
    # 方案 B：x=type, hue=program (这样可以直接用我们的黄蓝配色) -> 推荐
    ax = sns.barplot(
        data=dist_df, 
        x='type', 
        y='percentage', 
        hue='program', 
        palette=PROGRAM_COLORS,
        edgecolor='black',
        linewidth=0.8
    )
    
    ax.set_title('Distribution of Skill Types', fontweight='bold', pad=20)
    ax.set_xlabel('', fontweight='bold')
    ax.set_ylabel('Proportion', fontweight='bold')
    
    # 设置Y轴为百分比格式
    from matplotlib.ticker import PercentFormatter
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    
    ax.legend(title=None, frameon=True, edgecolor='black')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    sns.despine()
    
    save_plot('analysis_3_skill_types.png')
    plt.close()

def plot_distinctive_skills(skills_df):
    """图表 4: Diverging Bar Chart (非常适合展示差异)"""
    # 计算频次
    pivot = pd.crosstab(skills_df['skill'], skills_df['program'])
    # 归一化 (Relative Frequency) 以避免课程数量不同带来的偏差
    pivot = pivot.div(pivot.sum(axis=0), axis=1) * 1000 # 乘系数方便阅读
    
    pivot['diff'] = pivot['BASc(SDS)'] - pivot['BSc(IM)']
    
    # 取差异最大的两端
    sds_unique = pivot.sort_values('diff', ascending=False).head(10)
    im_unique = pivot.sort_values('diff', ascending=True).head(10) # 负值最大
    
    # 准备绘图数据
    top_diffs = pd.concat([sds_unique, im_unique])
    top_diffs = top_diffs.sort_values('diff') # 排序以便绘制发散条形图
    
    # 创建颜色列表：小于0为黄色，大于0为蓝色
    colors = [COLOR_YELLOW if x < 0 else COLOR_BLUE for x in top_diffs['diff']]
    
    plt.figure(figsize=(10, 8))
    
    # 绘制水平条形图
    plt.hlines(y=top_diffs.index, xmin=0, xmax=top_diffs['diff'], color=colors, alpha=0.8, linewidth=5)
    # 绘制端点圆点，增加设计感
    plt.scatter(top_diffs['diff'], top_diffs.index, color=colors, s=80, edgecolors='black', zorder=3)
    
    # 添加中心线
    plt.axvline(x=0, color='black', linestyle='-', linewidth=0.8, alpha=0.5)
    
    # 装饰
    plt.title('Most Distinctive Skills (Relative Frequency Difference)', fontweight='bold', pad=20)
    plt.xlabel('← Distinctive to BSc(IM)        Distinctive to BASc(SDS) →', fontweight='bold')
    
    # 添加注释
    plt.grid(linestyle='--', alpha=0.3)
    sns.despine(left=True, bottom=False)
    
    # 在图内添加文本标签，使得不用看Y轴也能读数 (可选)
    # 这是一个高级技巧，这里为了保持简洁，我们仅依赖Y轴
    
    save_plot('analysis_4_distinctive_skills.png')
    plt.close()

if __name__ == "__main__":
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _repo_root = os.path.dirname(_script_dir)
    input_file = os.path.join(_repo_root, "data", "course_skills_extracted.json")
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    try:
        print("--- Loading Data ---")
        df, skills_df = load_and_process_data(input_file)
        
        print("--- Generating Publication-Quality Plots ---")
        
        # 1. Top Tools (Bar)
        plot_top_tools_comparison(skills_df)
        
        # 2. Venn Diagram
        plot_venn_diagram(skills_df)
        
        # 3. Distribution (Grouped Bar)
        plot_skill_category_distribution(skills_df)
        
        # 4. Distinctive Skills (Diverging Lollipop/Bar Chart)
        plot_distinctive_skills(skills_df)
        
        print("--- Analysis Complete. Check .png and .pdf files ---")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found. Please ensure data extraction step is complete.")
    except Exception as e:
        print(f"An error occurred: {e}")