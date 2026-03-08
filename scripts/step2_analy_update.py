import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib_venn import venn2, venn2_circles
import matplotlib.font_manager as fm

# ==========================================
# 1. 顶级会议作图标准配置 (CS Top Conf Style)
# ==========================================

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False 

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

COLOR_BLUE = "#2878B5"
COLOR_YELLOW = "#E6B71E"
COLOR_PALETTE = [COLOR_BLUE, COLOR_YELLOW]
PROGRAM_COLORS = {'BASc(SDS)': COLOR_BLUE, 'BSc(IM)': COLOR_YELLOW}

# ==========================================
# 2. 数据处理逻辑
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

def save_plot(filename):
    import os
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _repo_root = os.path.dirname(_script_dir)
    plot_dir = os.path.join(_repo_root, "plot")
    os.makedirs(plot_dir, exist_ok=True)
    png_path = os.path.join(plot_dir, filename)
    pdf_path = os.path.join(plot_dir, filename.replace('.png', '.pdf'))
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    print(f"Saved: {png_path} & {pdf_path}")

# ==========================================
# 3. 绘图函数 (已添加数值标注)
# ==========================================

def plot_top_tools_comparison(skills_df):
    """图表 1: Top 15 Tools (带数值)"""
    tools_df = skills_df[skills_df['type'] == 'Tool']
    tool_counts = tools_df.groupby(['program', 'skill']).size().reset_index(name='count')
    
    total_counts = tool_counts.groupby('skill')['count'].sum()
    top_tools = total_counts.nlargest(15).index.tolist()
    
    plot_data = tool_counts[tool_counts['skill'].isin(top_tools)].copy()
    plot_data['skill'] = pd.Categorical(plot_data['skill'], categories=top_tools, ordered=True)
    
    plt.figure(figsize=(12, 8)) # 稍微调大一点以便显示数字
    
    ax = sns.barplot(
        data=plot_data, 
        y='skill', 
        x='count', 
        hue='program', 
        palette=PROGRAM_COLORS,
        edgecolor='black',
        linewidth=0.8,
        width=0.7
    )
    
    # [新增] 添加数值标注
    for container in ax.containers:
        ax.bar_label(container, padding=3, fmt='%d', fontsize=10, fontweight='bold')

    ax.set_title('Top 15 Technical Tools Comparison', fontweight='bold', pad=20)
    ax.set_xlabel('Frequency', fontweight='bold')
    ax.set_ylabel('')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    ax.legend(title=None, frameon=True, fancybox=False, edgecolor='black')
    sns.despine(left=True, bottom=False)
    
    save_plot('analysis_1_top_tools.png')
    plt.close()

def plot_venn_diagram(skills_df):
    """图表 2: Venn Diagram (保持不变)"""
    sds_skills = set(skills_df[skills_df['program'] == 'BASc(SDS)']['skill'].str.lower())
    im_skills = set(skills_df[skills_df['program'] == 'BSc(IM)']['skill'].str.lower())
    
    plt.figure(figsize=(6, 6))
    
    v = venn2([sds_skills, im_skills], set_labels=('BASc(SDS)', 'BSc(IM)'))
    
    if v.get_patch_by_id('10'):
        v.get_patch_by_id('10').set_color(COLOR_BLUE)
        v.get_patch_by_id('10').set_alpha(0.7)
    if v.get_patch_by_id('01'):
        v.get_patch_by_id('01').set_color(COLOR_YELLOW)
        v.get_patch_by_id('01').set_alpha(0.7)
    if v.get_patch_by_id('11'):
        v.get_patch_by_id('11').set_color('#708090')
        v.get_patch_by_id('11').set_alpha(0.5)
    
    c = venn2_circles([sds_skills, im_skills], linestyle='-', linewidth=1.5, color='black')
    
    for text in v.set_labels:
        if text:
            text.set_fontsize(12)
            text.set_fontweight('bold')
    for text in v.subset_labels:
        if text:
            text.set_fontsize(14)
            text.set_color('black') 

    plt.title('Skill Set Overlap', fontweight='bold', pad=10)
    save_plot('analysis_2_skill_overlap.png')
    plt.close()

def plot_skill_category_distribution(skills_df):
    """图表 3: Distribution (带百分比数值)"""
    dist_df = skills_df.groupby(['program', 'type']).size().reset_index(name='count')
    
    total_counts = dist_df.groupby('program')['count'].transform('sum')
    dist_df['percentage'] = dist_df['count'] / total_counts
    
    plt.figure(figsize=(9, 6))
    
    ax = sns.barplot(
        data=dist_df, 
        x='type', 
        y='percentage', 
        hue='program', 
        palette=PROGRAM_COLORS,
        edgecolor='black',
        linewidth=0.8
    )
    
    # [新增] 添加百分比数值标注
    for container in ax.containers:
        # 格式化为百分比，如 "78.5%"
        labels = [f'{v:.1%}' for v in container.datavalues]
        ax.bar_label(container, labels=labels, padding=3, fontsize=10, fontweight='bold')
    
    ax.set_title('Distribution of Skill Types', fontweight='bold', pad=20)
    ax.set_xlabel('', fontweight='bold')
    ax.set_ylabel('Proportion', fontweight='bold')
    
    from matplotlib.ticker import PercentFormatter
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    
    ax.legend(title=None, frameon=True, edgecolor='black')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    sns.despine()
    
    save_plot('analysis_3_skill_types.png')
    plt.close()

def plot_distinctive_skills(skills_df):
    """图表 4: Distinctive Skills (带数值标签)"""
    pivot = pd.crosstab(skills_df['skill'], skills_df['program'])
    # 归一化并放大系数
    pivot = pivot.div(pivot.sum(axis=0), axis=1) * 1000 
    
    pivot['diff'] = pivot['BASc(SDS)'] - pivot['BSc(IM)']
    
    sds_unique = pivot.sort_values('diff', ascending=False).head(10)
    im_unique = pivot.sort_values('diff', ascending=True).head(10)
    
    top_diffs = pd.concat([sds_unique, im_unique])
    top_diffs = top_diffs.sort_values('diff')
    
    colors = [COLOR_YELLOW if x < 0 else COLOR_BLUE for x in top_diffs['diff']]
    
    plt.figure(figsize=(12, 10)) # 增加宽度给文字留空间
    
    plt.hlines(y=top_diffs.index, xmin=0, xmax=top_diffs['diff'], color=colors, alpha=0.8, linewidth=5)
    plt.scatter(top_diffs['diff'], top_diffs.index, color=colors, s=80, edgecolors='black', zorder=3)
    
    # [新增] 添加数值标注逻辑
    # 获取X轴范围，用于动态调整文字位置
    x_range = top_diffs['diff'].max() - top_diffs['diff'].min()
    offset = x_range * 0.02 # 动态计算偏移量
    
    for i, (idx, val) in enumerate(top_diffs['diff'].items()):
        # 如果值在右边(>0)，文字显示在点的右侧，左对齐
        # 如果值在左边(<0)，文字显示在点的左侧，右对齐
        ha_align = 'left' if val > 0 else 'right'
        text_offset = offset if val > 0 else -offset
        text_color = COLOR_BLUE if val > 0 else "#B8860B" # Deep Gold for readability
        
        plt.text(
            val + text_offset, 
            i, 
            f'{abs(val):.1f}', # 显示绝对值或原值均可，这里显示数值
            va='center', 
            ha=ha_align,
            fontsize=10,
            fontweight='bold',
            color=text_color
        )
    
    plt.axvline(x=0, color='black', linestyle='-', linewidth=0.8, alpha=0.5)
    plt.title('Most Distinctive Skills (Relative Frequency Difference)', fontweight='bold', pad=20)
    plt.xlabel('← Distinctive to BSc(IM)        Distinctive to BASc(SDS) →', fontweight='bold')
    
    plt.grid(linestyle='--', alpha=0.3)
    sns.despine(left=True, bottom=False)
    
    save_plot('analysis_4_distinctive_skills.png')
    plt.close()

if __name__ == "__main__":
    import os
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _repo_root = os.path.dirname(_script_dir)
    input_file = os.path.join(_repo_root, "data", "course_skills_extracted.json")
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    try:
        print("--- Loading Data ---")
        df, skills_df = load_and_process_data(input_file)
        
        print("--- Generating Plots with Labels ---")
        
        # 1. Top Tools (Bar with Numbers)
        plot_top_tools_comparison(skills_df)
        
        # 2. Venn Diagram (Standard)
        plot_venn_diagram(skills_df)
        
        # 3. Distribution (Bar with Percentages)
        plot_skill_category_distribution(skills_df)
        
        # 4. Distinctive Skills (Diverging with Numbers)
        plot_distinctive_skills(skills_df)
        
        print("--- Analysis Complete. Check .png and .pdf files ---")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found. Please ensure data extraction step is complete.")
    except Exception as e:
        print(f"An error occurred: {e}")