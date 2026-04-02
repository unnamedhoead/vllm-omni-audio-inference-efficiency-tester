import os
import shutil
from pathlib import Path

def flatten_librispeech(src_dir, dest_dir):
    # 创建目标文件夹
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"创建目录: {dest_dir}")

    src_path = Path(src_dir)
    count = 0

    print("正在搜寻并移动音频文件...")
    
    # 递归查找所有 .flac 文件
    for flac_file in src_path.rglob('*.flac'):
        # 保持原文件名，移动到目标根目录
        # 如果担心重名（LibriSpeech基本不会），可以用 flac_file.parent.name + "_" + flac_file.name
        target_file = os.path.join(dest_dir, flac_file.name)
        
        # 使用 copy2 比较保险（保留元数据），如果你磁盘空间紧张可以用 shutil.move
        shutil.copy2(flac_file, target_file)
        count += 1
        
        if count % 500 == 0:
            print(f"已处理 {count} 个文件...")

    print(f"完成！共提取 {count} 个音频文件到 {dest_dir}")

if __name__ == "__main__":
    # 根据你截图中的路径结构调整
    source = "./test-clean/LibriSpeech/test-clean" 
    destination = "./LibriSpeech-test"
    
    flatten_librispeech(source, destination)