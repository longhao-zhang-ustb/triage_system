from pydub import AudioSegment
import io
import numpy as np

def convert_webm_bytes_to_pcm_bytes(
    webm_bytes: bytes, 
    sample_rate: int = 16000
) -> bytes:
    """
    将WEBM字节数据转换为PCM字节数据
    
    Args:
        webm_bytes: WEBM文件的字节数据
        sample_rate: 采样率（16000或8000）
    
    Returns:
        PCM数据的字节（原始16bit int16格式）
    """
    # 从字节读取
    audio = AudioSegment.from_file(io.BytesIO(webm_bytes), format="webm")
    
    # 转换参数
    audio = audio.set_sample_width(2)      # 16bit
    audio = audio.set_channels(1)           # 单声道
    audio = audio.set_frame_rate(sample_rate)
    
    # 导出到字节
    pcm_buffer = io.BytesIO()
    audio.export(pcm_buffer, format="s16le")
    
    return pcm_buffer.getvalue()