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
    with open("slides.md", "r", encoding='utf8') as f:
        slides = f.read().split('---\n---')
    markdowns = [Markdown(slide) for slide in slides]
    console = Console()
    curr_slide = 0
    while True:
        console.clear()
        console.print(markdowns[curr_slide])
        key = wait_for_key()
        if key == "q":
            return
        if key == 'r':
            parsed_items = markdowns[curr_slide].parsed
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
            curr_slide = len(markdowns) - 1           
        else:
            curr_slide = curr_slide + 1
            if curr_slide == len(markdowns):
                curr_slide = len(markdowns) - 1


if __name__ == "__main__":
    main()
