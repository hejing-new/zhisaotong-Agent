import os
import time

import streamlit as st
from agent.react_agent import ReactAgent
from rag.vector_store import VectorStoreService
from utils.path_tool import get_abs_path

# 标题
st.title("智扫通机器人智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

# 初始化人工模式状态
if "is_human_mode" not in st.session_state:
    st.session_state["is_human_mode"] = False

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 定义关键词
HUMAN_MODE_KEYWORDS = ["人工", "转人工", "人工服务", "客服", "人工客服"]
EXIT_HUMAN_MODE_KEYWORDS = ["退出", "退出人工", "结束人工", "结束人工服务"]

# 预设快捷提问列表
FAQ_BUTTONS = [
    "🧹 扫地机器人的滤网多久换一次？",
    "⚠️ 机器无法自动回充怎么办？",
    "📊 请帮我生成本月使用报告",
    "🙋‍♂️ 转人工客服"
]

def process_user_input(prompt: str):
    """统一的输入处理函数，处理用户输入并生成响应"""
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    # 硬拦截逻辑
    if not st.session_state["is_human_mode"]:
        # 情景A：当前处于智能模式，检查是否要转人工
        if any(keyword in prompt for keyword in HUMAN_MODE_KEYWORDS):
            # 切换到人工模式
            st.session_state["is_human_mode"] = True
            transfer_message = "🔄 正在为您转接人工客服，请稍候..."
            st.chat_message("assistant").write(transfer_message)
            st.session_state["message"].append({"role": "assistant", "content": transfer_message})
            st.rerun()
    else:
        # 情景B：当前处于人工模式
        if any(keyword in prompt for keyword in EXIT_HUMAN_MODE_KEYWORDS):
            # 退出人工模式
            st.session_state["is_human_mode"] = False
            exit_message = "✅ 已退出人工服务，智能助手继续为您服务。"
            st.chat_message("assistant").write(exit_message)
            st.session_state["message"].append({"role": "assistant", "content": exit_message})
            st.rerun()
        else:
            # 模拟人工客服回复
            human_response = f"👩‍💻 [人工客服]：收到了您的消息：'{prompt}'，正在为您处理..."
            st.chat_message("assistant").write(human_response)
            st.session_state["message"].append({"role": "assistant", "content": human_response})
            st.rerun()

    # 只有在智能模式下且未触发人工模式时，才调用Agent
    response_messages = []
    with st.spinner("智能客服思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, cache_list):

            for chunk in generator:
                cache_list.append(chunk)

                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        st.session_state["message"].append({"role": "assistant", "content": response_messages[-1]})
        st.rerun()

def generate_chat_markdown():
    """生成对话记录的Markdown格式内容"""
    if not st.session_state["message"]:
        return "# 对话记录\n\n暂无对话内容。"

    markdown_content = "# 智扫通智能客服 - 对话记录\n\n"
    markdown_content += f"**导出时间：** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    markdown_content += f"**人工模式：** {'是' if st.session_state['is_human_mode'] else '否'}\n\n"
    markdown_content += "---\n\n"

    for message in st.session_state["message"]:
        role = message["role"]
        content = message["content"]

        if role == "user":
            markdown_content += f"### 🧑‍💻 用户 (User)\n\n{content}\n\n"
        elif role == "assistant":
            markdown_content += f"### 🤖 智扫通客服 (Assistant)\n\n{content}\n\n"

        markdown_content += "---\n\n"

    return markdown_content

# 在侧边栏添加FAQ快捷提问卡片
with st.sidebar:
    st.subheader("💡 常见问题快捷提问")
    st.markdown("点击下方按钮快速提问：")

    for question in FAQ_BUTTONS:
        if st.button(question, key=f"faq_{question}", use_container_width=True):
            st.session_state.button_prompt = question

    st.divider()

    # 知识库上传区域
    st.subheader("📚 知识库管理")
    uploaded_file = st.sidebar.file_uploader("📤 上传知识库文档", type=["txt", "pdf"])

    if uploaded_file is not None:
        if st.sidebar.button("确认上传", use_container_width=True):
            with st.spinner("正在保存并处理文档，请稍候..."):
                # 保存文件到data目录
                data_dir = get_abs_path("data")
                file_path = os.path.join(data_dir, uploaded_file.name)

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # 触发RAG服务更新
                vs = VectorStoreService()
                vs.load_document()

            st.sidebar.success("✅ 文档已成功加入知识库！")

    st.divider()

    # 导出对话记录按钮
    if st.download_button(
        label="📥 导出聊天记录 (Markdown)",
        data=generate_chat_markdown(),
        file_name=f"zhisaotong_history_{time.strftime('%Y%m%d_%H%M')}.md",
        mime="text/markdown"
    ):
        st.success("聊天记录导出成功！")

# 用户输入提示词
prompt = st.chat_input()

# 检查是否有快捷按钮触发的提问
if st.session_state.get("button_prompt"):
    prompt = st.session_state.button_prompt
    st.session_state.button_prompt = None

if prompt:
    process_user_input(prompt)
