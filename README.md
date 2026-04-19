# 简历优化Agent

一个基于AI的简历优化应用，帮助用户分析简历与目标岗位的匹配度，并提供优化建议。

## 功能特性

- 📝 上传或输入简历内容
- 🎯 输入目标职位描述（JD）
- 🔍 AI分析简历与JD的匹配度
  - 匹配亮点
  - 主要缺口
  - 具体优化建议
- ✨ 一键生成优化后的简历
- 📥 支持优化结果下载
- 🐳 支持Docker容器化部署

## 技术栈

- **后端**: Python Flask
- **AI服务**: DeepSeek API
- **前端**: HTML5, CSS3, JavaScript
- **部署**: Docker, Docker Compose
- **Web服务器**: Gunicorn

## 快速开始

### 环境要求

- Docker 和 Docker Compose
- DeepSeek API Key (从[DeepSeek官网](https://platform.deepseek.com/)获取)

### 1. 克隆仓库

```bash
git clone <repository-url>
cd resume-optimizer-agent
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
# 复制示例配置文件
cp .env.example .env
```

编辑 `.env` 文件：

```env
# DeepSeek API配置
DEEPSEEK_API_KEY=sk-your-api-key-here

# Flask配置（可选，开发环境会自动生成）
# FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=false
```

### 3. 使用Docker Compose启动

```bash
# 构建并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

服务将在 http://localhost:5000 启动。

### 4. 直接使用Docker运行

```bash
# 构建镜像
docker build -t resume-optimizer-agent .

# 运行容器
docker run -d \
  -p 5000:5000 \
  -e DEEPSEEK_API_KEY=sk-your-api-key-here \
  # -e FLASK_SECRET_KEY=your-secret-key-here \  # 可选，未设置时会自动生成
  --name resume-optimizer \
  resume-optimizer-agent
```

### 5. 本地开发模式

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export DEEPSEEK_API_KEY=sk-your-api-key-here
# export FLASK_SECRET_KEY=your-secret-key-here  # 可选，开发环境会自动生成

# 启动开发服务器
python app.py
```

访问 http://localhost:5000

## 使用指南

### 第一步：输入简历和职位描述

1. 访问应用首页 (http://localhost:5000)
2. 在"简历内容"区域粘贴您的简历文本，或点击"上传文件"按钮上传文本文件
3. 在"目标职位描述"区域粘贴职位描述（JD）
4. 点击"分析简历匹配度"按钮

### 第二步：查看分析结果

AI将分析您的简历与目标职位的匹配度，结果显示：
- ✅ **匹配亮点**: 简历中与职位要求高度匹配的部分
- ⚠️ **主要缺口**: 简历中缺少或不足的职位要求
- 💡 **具体优化建议**: 如何修改简历以更好地匹配该职位

### 第三步：优化简历

1. 查看分析结果后，点击"优化简历"按钮
2. AI将根据分析结果生成优化后的简历内容
3. 优化后的简历将显示在页面上

### 第四步：下载结果

- 点击"下载优化简历"按钮，将优化后的简历保存为文本文件
- 或点击"复制到剪贴板"按钮，直接复制内容

## API接口

### 分析简历匹配度

```http
POST /analyze
Content-Type: application/json

{
  "resume_text": "简历内容文本",
  "job_description": "职位描述文本"
}
```

**响应示例**:
```json
{
  "analysis": "分析结果文本...",
  "resume_text": "原始简历内容",
  "job_description": "原始职位描述"
}
```

### 生成优化简历

```http
POST /optimize
Content-Type: application/json

{
  "confirm": true
}
```

**响应示例**:
```json
{
  "optimized_resume": "优化后的简历内容..."
}
```

### 下载优化简历

```http
GET /download
```

返回优化后的简历文本文件。

## 环境变量说明

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|---------|------|
| `DEEPSEEK_API_KEY` | 是 | 无 | DeepSeek API密钥 |
| `DEEPSEEK_API_BASE` | 否 | `https://api.deepseek.com/v1` | DeepSeek API基础URL |
| `DEEPSEEK_MODEL` | 否 | `deepseek-chat` | 使用的模型名称 |
| `FLASK_SECRET_KEY` | 否 | 自动生成（开发环境） | Flask会话密钥，未设置时会自动生成随机密钥 |
| `FLASK_DEBUG` | 否 | `false` | 调试模式 |
| `PORT` | 否 | `5000` | 应用端口 |

## 项目结构

```
resume-optimizer-agent/
├── app.py                 # 主应用文件
├── requirements.txt       # Python依赖
├── Dockerfile            # Docker构建文件
├── docker-compose.yml    # Docker Compose配置
├── .env.example          # 环境变量示例
├── README.md             # 本文档
├── templates/            # HTML模板
│   ├── index.html       # 主页面
│   ├── result.html      # 结果页面
│   └── error.html       # 错误页面
└── static/              # 静态文件目录
```

## 测试数据

### 示例简历

```
张三
电话：13800138000 | 邮箱：zhangsan@example.com
教育背景：
- 北京大学，计算机科学与技术，本科，2020-2024
工作经历：
- 2024.07-至今：字节跳动，后端开发工程师
  - 负责微服务架构设计与开发
  - 使用Python和Go开发高并发系统
  - 参与AI相关项目开发
技能：
- 编程语言：Python, Go, JavaScript
- 框架：Flask, Django, React
- 数据库：MySQL, Redis, MongoDB
```

### 示例职位描述（JD）

```
AI Agent 开发工程师

岗位职责：
- 参与 AI 智能体（Agent）系统的设计与开发
- 构建基于大语言模型的记忆、工具调用与多智能体协作能力
- 参与设计 AI 驱动的交互流程
- 探索 Agent 在真实业务场景中的落地

技术栈：
- Python / JavaScript / TypeScript
- OpenAI / Claude / DeepSeek 等主流大模型 API
- 向量数据库、工具调用、智能体框架

任职要求：
- 本科及以上在读，计算机相关专业优先
- 熟悉至少一门编程语言（Python / JavaScript / TypeScript）
- 对大语言模型（LLM）和 AI Agent 有好奇心
- 逻辑清晰，态度认真，能与团队顺畅沟通
```

## 故障排除

### 常见问题

1. **应用无法启动**
   - 检查Docker是否正常运行：`docker --version`
   - 检查端口5000是否被占用：`netstat -tuln | grep 5000`
   - 查看Docker日志：`docker-compose logs resume-optimizer`

2. **API调用失败**
   - 检查DeepSeek API密钥是否正确
   - 确认API密钥有足够的余额
   - 检查网络连接，确保可以访问DeepSeek API

3. **上传文件失败**
   - 目前仅支持文本文件（.txt）
   - 对于PDF或Word文件，请先转换为文本格式

### 日志查看

```bash
# Docker Compose方式
docker-compose logs -f

# Docker方式
docker logs resume-optimizer-agent -f
```

## 安全说明

- API密钥通过环境变量传递，不在代码中硬编码
- 会话数据存储在服务器内存中，重启后丢失
- 建议在生产环境中使用HTTPS
- 定期更新依赖包以确保安全

## 许可证

MIT

## 贡献

欢迎提交Issue和Pull Request！

## 联系

如有问题或建议，请通过GitHub Issues联系我们。