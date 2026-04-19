import os
import re
from flask import Flask, render_template, request, jsonify, session
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

# 配置DeepSeek API
openai.api_key = os.getenv('DEEPSEEK_API_KEY')
openai.api_base = os.getenv('DEEPSEEK_API_BASE', 'https://api.deepseek.com/v1')
model = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')

def analyze_resume_with_gpt(resume_text, job_description):
    """调用DeepSeek API分析简历与职位描述的匹配度"""
    prompt = f"""
你是一个专业的简历优化专家。请分析以下简历与目标职位的匹配情况，并给出详细报告。

简历内容：
{resume_text}

目标职位描述：
{job_description}

请从以下三个方面提供分析报告：
1. 匹配亮点：简历中与职位要求高度匹配的部分
2. 主要缺口：简历中缺少或不足的职位要求
3. 具体优化建议：如何修改简历以更好地匹配该职位

请使用清晰的结构输出，每个部分使用标题，并提供具体的例子和建议。
"""

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个专业的职业顾问和简历优化专家。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"分析过程中出现错误: {str(e)}"

def optimize_resume_with_gpt(resume_text, job_description, analysis):
    """调用DeepSeek API生成优化后的简历"""
    prompt = f"""
基于以下简历、职位描述和已进行的分析，请生成一份优化后的简历。

原始简历：
{resume_text}

目标职位描述：
{job_description}

已进行的分析：
{analysis}

请生成一份优化后的简历，要求：
1. 保持原始简历的基本信息（姓名、联系方式、教育背景等）
2. 根据职位描述调整工作经验和技能描述，突出相关能力
3. 使用更专业、更有力的语言
4. 添加或修改内容以弥补分析中指出的缺口
5. 保持合理的篇幅，重点突出与目标职位相关的经历

请直接输出优化后的简历内容，不需要额外解释。
"""

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个专业的简历优化专家，擅长根据职位描述调整简历内容。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"优化过程中出现错误: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    resume_text = data.get('resume_text', '').strip()
    job_description = data.get('job_description', '').strip()

    if not resume_text or not job_description:
        return jsonify({'error': '简历内容和职位描述不能为空'}), 400

    # 保存到session
    session['resume_text'] = resume_text
    session['job_description'] = job_description

    # 调用分析函数
    analysis_result = analyze_resume_with_gpt(resume_text, job_description)

    # 保存分析结果到session
    session['analysis_result'] = analysis_result

    return jsonify({
        'analysis': analysis_result,
        'resume_text': resume_text,
        'job_description': job_description
    })

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.json
    confirm = data.get('confirm', False)

    if not confirm:
        return jsonify({'error': '需要确认才能优化简历'}), 400

    # 从session获取数据
    resume_text = session.get('resume_text', '')
    job_description = session.get('job_description', '')
    analysis_result = session.get('analysis_result', '')

    if not resume_text or not job_description:
        return jsonify({'error': '数据丢失，请重新分析简历'}), 400

    # 调用优化函数
    optimized_resume = optimize_resume_with_gpt(resume_text, job_description, analysis_result)

    # 保存优化结果到session
    session['optimized_resume'] = optimized_resume

    return jsonify({
        'optimized_resume': optimized_resume
    })

@app.route('/result')
def result():
    optimized_resume = session.get('optimized_resume', '')
    if not optimized_resume:
        return render_template('error.html', message='未找到优化后的简历，请重新开始流程')
    return render_template('result.html', optimized_resume=optimized_resume)

@app.route('/download')
def download():
    optimized_resume = session.get('optimized_resume', '')
    if not optimized_resume:
        return jsonify({'error': '未找到优化后的简历'}), 404

    # 创建一个简单的文本文件供下载
    from flask import Response
    return Response(
        optimized_resume,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=optimized_resume.txt"}
    )

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)