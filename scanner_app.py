import re
import tkinter as tk
from tkinter import scrolledtext

# قائمة أنواع الرموز (التوكنز) باستخدام التعبيرات المنتظمة
TOKEN_PATTERNS = {
    'NUMBER': r'\d+(\.\d*)?',       # الأرقام
    'IDENTIFIER': r'[A-Za-z_]\w*',  # المعرفات
    'ASSIGN': r'=',                 # علامة الإسناد
    'TERMINATOR': r';',             # نهاية الجملة البرمجية
    'OPERATOR': r'[+\-*/]',         # العمليات الحسابية
    'WHITESPACE': r'\s+',           # المسافات
    'NEWLINE': r'\n',               # سطر جديد
    'LPAREN': r'\(',                # قوس فتح
    'RPAREN': r'\)',                # قوس غلق
    'COMMENT': r'#.*',              # التعليقات
    'UNKNOWN': r'.'                 # أي رمز غير معروف
}

# تجميع الأنماط في تعبير منتظم واحد
TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_PATTERNS.items())

def analyze_code(input_code):
    """
    تحليل الشيفرة المدخلة وإرجاع قائمة بالتوكنز
    """
    tokens_list = []
    current_line = 1

    for match in re.finditer(TOKEN_REGEX, input_code):
        token_type = match.lastgroup
        token_value = match.group(token_type)

        if token_type == 'WHITESPACE' or token_type == 'COMMENT':
            continue  # تجاهل المسافات والتعليقات
        if token_type == 'NEWLINE':
            current_line += 1
            continue
        if token_type == 'UNKNOWN':
            tokens_list.append(("ERROR", f"Unknown token '{token_value}'", current_line))
        else:
            tokens_list.append((token_type, token_value, current_line))
    
    return tokens_list

class CodeScannerApp:
    def __init__(self, master):
        master.title("Code Token Analyzer")
        master.geometry("600x400")
        
        # إدخال الشيفرة البرمجية
        self.code_input_area = scrolledtext.ScrolledText(master, width=70, height=10)
        self.code_input_area.pack(pady=10)
        
        # زر التحليل
        self.scan_btn = tk.Button(master, text="Analyze Code", command=self.execute_analysis)
        self.scan_btn.pack(pady=5)
        
        # مخرجات التحليل
        self.result_area = scrolledtext.ScrolledText(master, width=70, height=10, state='disabled')
        self.result_area.pack(pady=10)
        
    def execute_analysis(self):
        # الحصول على الشيفرة المدخلة من المستخدم
        input_code = self.code_input_area.get("1.0", tk.END)
        
        # تحليل الرموز
        tokens = analyze_code(input_code)
        
        # عرض النتائج
        self.result_area.config(state='normal')
        self.result_area.delete("1.0", tk.END)
        
        if tokens:
            for token_type, token_value, line in tokens:
                self.result_area.insert(tk.END, f"Type: {token_type}, Value: '{token_value}', Line: {line}\n")
        else:
            self.result_area.insert(tk.END, "No tokens found.")
        
        self.result_area.config(state='disabled')

if __name__ == "__main__":
    window = tk.Tk()
    CodeScannerApp(window)
    window.mainloop()
