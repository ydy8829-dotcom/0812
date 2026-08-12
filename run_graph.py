import sys
from graph import graph

def run(user_input: str, mode: str = "recommendation"):
    return graph.invoke({"user_input": user_input, "mode": mode, "context": {}, "trace": []})

if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) or "다음 달 반도체 장비회사 면접인데 뭘 준비해야 할지 모르겠어"
    result = run(text)
    print(result["final_response"])
