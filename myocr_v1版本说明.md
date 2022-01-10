作者：康
更新时间：2022.1.4

# 一、项目介绍

## （一）项目动机

1.主要是为了解决工作中需要批量图片转文字的需求，且是免费的，不限次数，不限流量。

2.降低免费OCR的使用门槛，达到操作简单，性能稳定，个性化等要求。

## （二）项目核心技术

1.该项目是一个简单的OCR小工具，借鉴了网上开源的OCR项目（agentOCR）,AgentOCR 是一个基于 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 和 [ONNXRuntime](https://github.com/microsoft/onnxruntime) 项目开发的一个使用简单、调用方便的 OCR 项目。项目地址：https://pypi.org/project/agentocr/

## （三）项目使用方法

1.先安装requirements.txt文件里的第三方库。使用pip方法

2.打开项目主程序文件ocr_main.py，修改 if __name = '__main__':下的目标文件目录，然后运行即可。

## （四）项目特点

1.支持批量化识别，只需选择目标目录即可。

2.支持CPU和GPU，由于核心是机器学习模型，因此采用GPU会快很多。

3.支持png,jpg,pdf和长图等格式。

4.支持识别多种语音，包括中文，英文，日语等。

## （四）本版本更新内容

1.支持了长图

2.删除了中间文件

3.合并了识别内容

4.优化了代码结构
