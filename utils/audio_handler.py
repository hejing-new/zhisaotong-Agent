"""
语音处理模块，包含语音转文字功能
"""

import os
from typing import Optional

# TODO: 后续接入阿里云 DashScope 语音识别 API
# 需要安装 dashscope 包: pip install dashscope
# from dashscope.audio.asr import SenseVoice

def speech_to_text(audio_bytes: bytes) -> str:
    """
    将音频 bytes 数据转换为文字

    当前为 Mock 实现，直接返回测试文本。
    后续需要接入阿里云 DashScope 的 SenseVoice 模型或标准 HTTP API。

    Args:
        audio_bytes: 音频文件的 bytes 数据

    Returns:
        识别出的文字内容
    """
    # Mock 实现 - 返回测试文本
    # 实际使用时，这里应该调用 DashScope API
    #
    # 示例代码（待实现）：
    # import dashscope
    # from dashscope.audio.asr import Recognition
    #
    # # 配置 API Key
    # dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
    #
    # # 使用 SenseVoice 模型进行识别
    # rec = Recognition(model='sensevoice-v1')
    # result = rec.call(audio_bytes)
    # return result.text

    print(f"收到音频数据，大小: {len(audio_bytes)} bytes")
    return "测试语音识别内容"