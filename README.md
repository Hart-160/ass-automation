# D4DJ-ASS-AUTOMATION

灵感来源：[Jeunette/ass-automation-java](https://github.com/Jeunette/ass-automation-java)

## 安装方式

### Release版

在release界面下载zip，解压后点击ASS-automation.exe运行

注：从v2.0开始，每次release将会有两个发行版本。

- 稳定版（Template Match）：v2.0新增，运行速度较慢，但出错率更低
- 快速版（Color Detect）：继承现有的读取方式，若无大范围错误可使用此版本

**请勿将运行轴机所需的视频、剧情文件等放在轴机文件夹目录下！！**

### 开发版

- 需求：Python 3.8+
- 克隆本仓库

```shell
    git clone https://github.com/Hart-160/ass-automation.git
```

- 安装依赖

```shell
    pip install -r requirements.txt
```

- 使用方式

```shell
    python ASS-automation.py
```

注：代码内的识别法切换于ass_writer.py内

```python
video_process_thread = ImageSections.COLOR_DETECT #定位识别法，对应快速版
vidoe_process_thread = ImageSections.TEMPLATE_MATCH #模板匹配法，对应稳定版
```

## 使用指南

若未提供所需分辨率的预设，请通过下方联系方式联系作者制作对应预设

注：苹果设备在同分辨率的情况下，有touch bar和无touch bar无法使用同预设

|   预设对应情况   |  分辨率  |            适用设备            |
| :--------------: | :-------: | :----------------------------: |
| 源码&release包含 | 1920x1440 |   iPad Air3等无touch bar设备   |
|   release包含   | 1920x888 | iPhone 12，13等有touch bar设备 |
|   release包含   | 1920x1260 |  iPad mini6等有touch bar设备  |
|   release包含   | 1920x1334 |   iPad Air5等有touch bar设备   |

- [精简版教程](https://www.bilibili.com/read/cv18462837)
- [详细版教程](https://docs.qq.com/doc/DTENkZGloYXNQZ01Y)

## 作者联系方式

- Bilibili：[广间Hiroma](https://space.bilibili.com/11889810)
- Discord：Hiroma#4993
- QQ：1287302495

## WIP

- [ ] 视频版轴机校对教程
- [ ] *更多需求请提出**issue***

## 特别鸣谢

- Jeunette：原版作者，感谢提供抖动识别算法相关的帮助
- 由理：感谢提供模板识别法的思路
- NOTE：感谢协助测试
