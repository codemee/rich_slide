slides = [
r"""
# LLM 是住在封閉圖書館內的小孩

```

       o
      / \
     -----
    /     \
   ---------  
__/         \__
 |_    []   _|
 |_   /||\  _|
 |_    /\   _|
--------------- 
///////////////

```
""",
r"""
# 各開發商幫 LLM 裝了可以跟外界交談的電話

```

       o             +---------+
      / \            | claude  |
     -----        +--+ ChatGPT |
    /     \       |  |   ...   |
   ---------      |  +---------+    
__/         \__   |
 |_    []   _|[---+  +---------+
 |_   /||\  _|       |         |
 |_    /\   _|[------+ LLM API |
---------------      |         |
///////////////      +---------+

```
""",
r"""
# 跟外界溝通的兩個問題

```

       o             +---------+
      / \            | claude  | 無法獲取外部資訊
     -----        +--+ ChatGPT | 無法執行實際動作
    /     \       |  |   ...   | 無止盡的複製貼上
   ---------      |  +---------+    
__/         \__   |
 |_    []   _|[---+  +---------+
 |_   /||\  _|       |         | 先問 LLM 要做什麼 
 |_    /\   _|[------+ LLM API | 再把指示轉換成動作
---------------      |         | 複雜而且具不穩定性
///////////////      +---------+

```
""",
r"""
# OpenAI 嘗試幫 LLM 生出感官與手腳

```

       o             +---------+       Remote
      / \            |         |     +---------+
     -----        +--+ ChatGPT +[----+ actions |
    /     \       |  |         |     +---------+
   ---------      |  +---------+    
__/         \__   |                     Local
 |_    []   _|[---+  +------------------------------+
 |_   /||\  _|       |         +------------------+ |
 |_    /\   _|[------+ OpenAI  | Function calling | |
---------------      | API     +------------------+ |
///////////////      +------------------------------+

```
""",
r"""
# 但這有兩個問題

```

       o             +---------+       Remote（碰不到使用者的電腦）
      / \            |         |     +---------+
     -----        +--+ ChatGPT +[----+ actions +-----> 規格不同
    /     \       |  |         |     +---------+       無法互通
   ---------      |  +---------+                          ^
__/         \__   |                     Local（無法分享） |
 |_    []   _|[---+  +------------------------------+     |
 |_   /||\  _|       |         +------------------+ |     |
 |_    /\   _|[------+ OpenAI  | Function calling | +-----+
---------------      | API     +------------------+ |
///////////////      +------------------------------+

```
""",
r"""
# claude 制訂 MCP 想要一統江湖

```
                             MCP Host                           remote/local
       o             +-----------------------+                 +-------------+
      / \            | claude  +-----------+ |                 | MCP Server  |
     -----        +--+ ChatGPT | MCP client+-+--+           +--+ Tools:      |
    /     \       |  |   ...   +-----------+ |  |  +-----+  |  | run cmd...  |
   ---------      |  +-----------------------+  |  |     |  |  +-------------+
__/         \__   |                             +--+ MCP +--+--+ ...  
 |_    []   _|[---+  +-----------------------+  |  |     |  |  +-------------+
 |_   /||\  _|       |         +-----------+ |  |  +-----+  |  | MCP Server  |
 |_    /\   _|[------+ LLM API | MCP client+-+--+           +--+ Tools:      |
---------------      |         +-----------+ |                 | fetch web...|
///////////////      +-----------------------+                 +-------------+

```
""",
r""""
# 按 `r` 可以執行 Python 程式

```python
print("Hello World")
```
"""
]

from typing import List
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import print
from getchar import getkeys

def wait_for_key():
    while True:
        keys = getkeys()
        if len(keys) > 0:
            return keys[0].lower()
            

def main():
    makrdowns = [Markdown(slide) for slide in slides]
    console = Console()
    curr_slide = 0
    while True:
        console.clear()
        console.print(makrdowns[curr_slide])
        key = wait_for_key()
        if key == "q":
            return
        if key == 'r':
            parsed_items = makrdowns[curr_slide].parsed
            for parsed_item in parsed_items:
                if (parsed_item.tag == "code" and 
                    parsed_item.info == "python"):
                    result = eval(parsed_item.content)
                    print(Panel.fit(str(result), title="執行結果"))
                    wait_for_key()
                    continue
        if key in ["b", '\x00k', '\x00h']:
            curr_slide = 0 if curr_slide == 0 else curr_slide - 1
        elif key == '\x00g':
            curr_slide = 0
        elif key == '\x00o':
            curr_slide = len(makrdowns) - 1           
        else:
            curr_slide = curr_slide + 1
            if curr_slide == len(makrdowns):
                curr_slide = len(makrdowns) - 1


if __name__ == "__main__":
    main()
