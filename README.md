# 智扫通机器人智能客服 🤖

> 基于 LangChain ReAct Agent + RAG + Streamlit 的扫地机器人智能客服系统

---
# 使用必看

请务必安装好相关配置环境，其中config/agent.yml文件中的gaodekey需要改为实际申请的高德key(也可以根据个人需要更改为更加隐式的办法)

## 📖 项目简介

**智扫通机器人智能客服**是一款面向扫地机器人/扫拖一体机器人用户的企业级 AI 智能体应用。系统以前端 Streamlit 为交互载体，后端基于现代化的 LangChain 架构构建 ReAct（Reasoning + Acting）Agent。

本项目不仅实现了传统的 RAG 知识检索，更引入了**状态路由机制**与**多模态交互**，完美解决了 AI 客服常见的“死循环”、“啰嗦”以及“无法平滑移交”等痛点，提供媲美真人的丝滑服务体验。

## ✨ 核心特性与全新升级


1.🎧 **状态路由与人工无缝转接 (State Routing)**：

物理级隔离逻辑：基于 st.session_state 的状态路由，当触发 [HANDOFF_TRIGGER] 时，彻底切断 AI 调用流，停止 Token 消耗。

双向平滑切换：支持“一键退出人工”指令，通过 st.rerun() 瞬间重构 UI 状态，将控制权交回 AI 智能体。

2.🧠 **优雅的“深度思考”折叠 (Thought Folding)**：

采用 Streamlit 原生 st.status 容器封装 LangChain 的 ReAct 循环，完美折叠 Thought/Action/Observation 过程。

彻底解决了由于 CallbackHandler 兼容性导致的 IndexError 报错，确保界面只展示最简洁、准确的最终回复（Final Answer）。

3.🗺️ **高精度地理与环境感知 (Context Awareness)**：

环境适配建议：结合实时天气与空气湿度，AI 会主动给出当前环境是否适合扫拖一体机工作的专业建议（如避开潮湿天气进行大面积拖地）。

4.📚 **RAG 增强检索与排障**：

深度集成 Chroma 向量数据库，优先从产品手册、常见问题集、维护指南中检索权威答案。

防死循环机制：通过 Prompt 工程优化，确保 Agent 在追问故障细节与调用 RAG 工具之间保持逻辑连贯，避免复读机式的无效回复。

5.📊 **智能总结汇报模式 (Report Middleware)**：

动态提示词切换：中间件自动识别用户分析意图，动态将 System Prompt 从“对话模式”切换为“分析模式”。

结构化报告生成：结合外部 CSV 数据，一键生成包含使用时长、清扫面积、故障统计的专业 Markdown 格式报告。

6.📜 **商业级日志与追溯系统**：

具备完善的结构化日志记录（File + Console），支持对 Agent 每一轮 ReAct 决策过程的离线回溯与 Debug。

---

## 🏗 系统架构图 (System Architecture)
```text
┌────────────────────────────────────────────────────────┐
│               Streamlit 交互前端 (app.py)                │
│ ┌─────────────────────────┐      ┌───────────────────┐ │
│ │   对话输入 (Text Only)   │      │  流式 Markdown 渲染 │ │
│ └────────────┬────────────┘      └─────────▲─────────┘ │
└──────────────│─────────────────────────────│──────────┘
               │                             │
┌──────────────▼─────────────────────────────┴──────────┐
│                  状态路由器 (State Router)               │
│  [human_mode = True] ─────► 人工接手 & 工单打包渲染        │
│  [human_mode = False] ────► 激活 LangChain Agent        │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│            ReAct Agent (agent/react_agent.py)          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ System Prompt: 极简输出、防死循环、动态报告模式切换  │  │
│  └──────────────────────────────────────────────────┘  │
│  工具集：rag_summarize / get_weather / get_location /   │
│         transfer_to_human (人工触发器)                  │
└─────┬───────────────────────────┬──────────────────────┘
      │                           │
┌─────▼───────────────┐   ┌───────▼──────────────────────┐
│ Chroma 向量数据库     │   │ 外部 API 矩阵                 │
│ (PDF/TXT 维护指南)    │   │ 高德地图 (国内) / 阿里云 Qwen │
└─────────────────────┘   └──────────────────────────────┘
```


## 📂 目录结构
```bash
zhisaotong-Agent/
├── app.py                 # Streamlit 前端入口
├── agent/                 # Agent 核心逻辑
│   ├── react_agent.py     # ReAct Agent 核心编排
│   ├── tools/             # 工具函数定义
│   │   ├── agent_tools.py # 工具具体实现
│   │   └── middleware.py  # Agent 中间件 (监控/日志/切换)
│   ├── rag/               # RAG 检索摘要服务
│   │   ├── rag_service.py # 检索服务逻辑
│   │   └── vector_store.py# Chroma 向量库管理
│   ├── model/             # 模型工厂
│   │   └── factory.py     # LLM + Embedding 实例化
│   └── utils/             # 通用工具
│       ├── config_handler.py # YAML 配置加载
│       ├── logger_handler.py # 日志工具
│       ├── path_tool.py      # 路径管理
│       ├── file_handler.py   # 文档加载 (PDF/TXT)
│       └── prompt_loader.py  # 提示词加载
├── config/                # 配置文件目录
│   ├── agent.yml          # 高德 Key/外部路径配置
│   ├── rag.yml            # 模型名称配置
│   ├── chroma.yml         # 向量库参数配置
│   └── prompts.yml        # 提示词路径映射
├── prompts/               # 提示词文本
│   ├── main_prompt.txt    # 主 ReAct 提示词
│   ├── rag_summarize.txt  # RAG 摘要提示词
│   └── report_prompt.txt  # 报告生成提示词
├── data/                  # 原始数据
│   ├── 扫地机器人100问.pdf
│   ├── 故障排除.txt
│   └── external/
│       └── records.csv    # 用户清扫记录 (外部数据)
├── chroma_db/             # Chroma 持久化目录 (自动生成)
├── logs/                  # 系统日志目录 (自动生成)
├── md5.text               # 文档 MD5 去重记录
└── README.md
```

⚙️ **配置指南**

1. 阿里云百炼平台凭证
   
系统通过 DashScope SDK 调用通义千问模型，请配置环境变量：

# 建议在 .env 或系统环境变量中配置

```bash
export DASHSCOPE_API_KEY="your_dashscope_api_key"
```
注意：若使用 OpenAI 兼容格式调用，请确保变量名与代码中 ChatOpenAI 或相关封装一致。

2. 高德地图 Web 服务配置
编辑 config/agent.yml，接入实时地理位置与天气能力：

# config/agent.yml
```bash
gaodekey: "你的高德API_KEY"         # 需申请 "Web服务" 类型 Key
gaode_base_url: https://restapi.amap.com
```

🛠 **核心工具集 (Tools)**

Agent 动态调用的 7 项核心技能：

RAG 专家库 (rag_summarize): 检索本地 .pdf/.txt 文档，解决专业售后问题。

环境感知 (get_weather / get_user_location): 基于 IP 定位提供针对性的扫拖环境建议。

用户画像 (get_user_id / get_current_month / fetch_external_data): 联动外部 CSV 数据库，获取清扫面积、时长等原始数据。

模式切换 (fill_context_for_report): 意图识别的“道岔”，触发从“对话模式”向“报告模式”的逻辑跳转。

🔄 **中间件与状态流转机制**

系统通过三层中间件实现对 Agent 执行全生命周期的精准监控：

```text
graph TD
    A[用户输入] --> B{中间件层}
    
    subgraph Middleware_Logic
    B1[monitor_tool] -->|监控| C1[记录调用参数/状态/耗时]
    B1 -->|拦截| C2[检测 Report 信号并更新 Context]
    
    B2[log_before_model] -->|预处理| C3[记录消息队列状态与 Token 预估]
    
    B3[report_prompt_switch] -->|路由| C4{动态 Prompt 判定}
    C4 -->|context:report=True| D1[载入报告生成提示词]
    C4 -->|context:report=False| D2[载入主 ReAct 提示词]
    end
    
    D1 & D2 --> E[模型生成回复]
```
<img width="2512" height="1448" alt="4b9e855dc1cae8df1cfa8695e2ab20a5" src="https://github.com/user-attachments/assets/38e6c5bd-1f9d-4787-b140-954405f699a9" />

📚 **知识库管理 (RAG)**
系统具备增量入库功能，支持 .txt 与 .pdf 格式。

自动同步：放置文件于 data/ 目录，重启即自动向量化。

智能去重：通过 MD5 哈希校验机制，确保已入库文档不会重复处理，节省计算资源。

涵盖内容：包含从《选购指南》到《故障排除》的完整售后知识链路。
