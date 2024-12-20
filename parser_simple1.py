class Parser:
    # تهيئة المتغيرات الأساسية للمحلل
    def __init__(self):
        self.grammar = {}  # قاموس لتخزين قواعد القواعد
        self.stack = []    # قائمة لتتبع عملية التحليل
        self.input_string = []  # السلسلة المدخلة للتحليل
        self.unchecked = []     # الجزء غير المحلل من السلسلة
        
    # دالة للتحقق من أن القواعد بسيطة
    def is_simple_grammar(self):
        # التحقق من كل non-terminal وقواعده
        for non_terminal, rules in self.grammar.items():
            first_terminals = set()  # مجموعة لتخزين الحروف الأولى للقواعد
            
            for rule in rules:
                # التحقق من أن القاعدة غير فارغة
                if not rule:
                    print(f"\nThe Grammar isn't simple.")
                    print("Empty rules are not allowed.")
                    return False
                    
                # الشرط الأول: يجب أن تبدأ القاعدة بـ terminal (حرف صغير)
                if not rule[0].islower():
                    print(f"\nThe Grammar isn't simple.")
                    print(f"Rule '{rule}' doesn't start with a terminal.")
                    return False
                    
                # الشرط الثاني: التحقق من أن القواعد التي تعرف نفس الـ non-terminal تبدأ بحروف terminal مختلفة
                if rule[0] in first_terminals:
                    print(f"\nThe Grammar isn't simple.")
                    print(f"Multiple rules for {non_terminal} start with the same terminal '{rule[0]}'")
                    return False
                first_terminals.add(rule[0])
                
        print("\nThe Grammar is simple.")
        return True
        
    # دالة لإدخال قواعد القواعد من المستخدم
    def get_grammar(self):
        print("\nRecursive Descent Parsing For following grammar")
        print("Grammars")
        
        # الحصول على قواعد S
        print("\nEnter rules for S:")
        self.grammar['S'] = []
        rule1 = input("Enter rule number 1 for non-terminal 'S': ").strip()
        rule2 = input("Enter rule number 2 for non-terminal 'S': ").strip()
        self.grammar['S'].extend([rule1, rule2])
        
        # الحصول على قواعد B
        print("\nEnter rules for B:")
        self.grammar['B'] = []
        rule1 = input("Enter rule number 1 for non-terminal 'B': ").strip()
        rule2 = input("Enter rule number 2 for non-terminal 'B': ").strip()
        self.grammar['B'].extend([rule1, rule2])
        
        # التحقق من أن القواعد بسيطة قبل المتابعة
        if not self.is_simple_grammar():
            return False
        return True
        
    # دالة للتحقق من صحة السلسلة المدخلة
    def parse_string(self, input_str):
        self.input_string = list(input_str)  # تحويل السلسلة إلى قائمة من الحروف
        self.stack = []  # تفريغ المكدس
        self.unchecked = self.input_string.copy()  # نسخ السلسلة المدخلة للتحقق
        
        # عرض السلسلة المدخلة بالتنسيق المطلوب
        print("The input String: [", end='')
        for i, char in enumerate(input_str):
            if i > 0:
                print(", ", end='')
            print(f"'{char}'", end='')
        print("]")
        
        # بدء التحليل من الرمز الابتدائي S
        accepted = self.parse('S', 0)
        
        # عرض حالة المكدس والسلسلة المتبقية
        print("Stack after checking: []")
        print("The rest of unchecked string:")
        print("[]")
        
        # إرجاع نتيجة التحليل
        return accepted
        
    # دالة التحليل الرئيسية
    def parse(self, symbol, pos):
        # التحقق من تجاوز نهاية السلسلة
        if pos >= len(self.input_string):
            return False
            
        # إذا كان الرمز terminal (حرف صغير)
        if symbol not in self.grammar:
            if pos < len(self.input_string) and symbol == self.input_string[pos]:
                return True
            return False
            
        # إذا كان الرمز non-terminal (حرف كبير)
        for rule in self.grammar[symbol]:
            if not rule:  # تخطي القواعد الفارغة
                continue
                
            current_pos = pos
            match = True
            
            # التحقق من كل حرف في القاعدة
            for char in rule:
                if current_pos >= len(self.input_string):
                    match = False
                    break
                    
                if char in self.grammar:  # إذا كان الحرف non-terminal
                    if not self.parse(char, current_pos):
                        match = False
                        break
                    # حساب عدد الحروف التي تم استهلاكها
                    for r in self.grammar[char]:
                        if current_pos + len(r) <= len(self.input_string):
                            current_pos += len(r)
                            break
                else:  # إذا كان الحرف terminal
                    if char != self.input_string[current_pos]:
                        match = False
                        break
                    current_pos += 1
                    
            if match:
                return True
                
        return False
        
    # الدالة الرئيسية للبرنامج
    def main(self):
        while True:
            if not self.get_grammar():  # الحصول على القواعد
                continue
                
            while True:
                string = input("Enter the string want to be checked : ")
                
                if self.parse_string(string):  # تحليل السلسلة
                    print("Your input String is Accepted.")
                else:
                    print("Your input String is Rejected.")
                    
                print("=" * 50)
                print("1-Another Grammar.")
                print("2-Another String.")
                print("3-Exit")
                
                choice = input("Enter ur choice : ")
                if choice == "1":
                    break  # إدخال قواعد جديدة
                elif choice == "2":
                    continue  # تحليل سلسلة جديدة
                elif choice == "3":
                    return  # إنهاء البرنامج
                else:
                    print("Invalid choice!")

# نقطة بداية البرنامج
if __name__ == "__main__":
    parser = Parser()  # إنشاء كائن من الصنف Parser
    parser.main()  # تشغيل البرنامج
