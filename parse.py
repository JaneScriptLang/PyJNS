import os


class Parser:
    def __init__(self, code):
        self.code = code
        print(".")
        self._imports = []
        self.path = [os.getcwd(), os.path.dirname(os.path.abspath(__file__))+"/include"]
        self.parse(self.code)

    def parse(self, code, ret=False):
        code = self.parseComments(code)
        code = self.ParseImports(code)
        code = self.parsePragmas(code)
        code = self.ParseKeywords(code)
        code = self.parseBraces(code)
        if ret:
            return code
        with open("outs.py", "w") as f:
            f.write(code)

    def parseBraces(self, code: str) -> str:
        leftBracesAmount = 0
        for line in code.splitlines():
            if "{" in line:
                lineChars = list(line)
                stringCount = 0
                for i in range(len(lineChars)):
                    if lineChars[i] == '"' or lineChars[i] == "'":
                        stringCount += 1
                    if lineChars[i] == "{":
                        if stringCount % 2 == 0 and stringCount != 0:
                            leftBracesAmount += 1
                            break
        rightBracesAmount = 0
        for line in code.splitlines():
            if "}" in line:
                lineChars = list(line)
                stringCount = 0
                for i in range(len(lineChars)):
                    if lineChars[i] == '"' or lineChars[i] == "'":
                        stringCount += 1
                    if lineChars[i] == "}":
                        if stringCount % 2 == 0 and stringCount != 0:
                            rightBracesAmount += 1
                            break

        if leftBracesAmount != rightBracesAmount:
            Error(("Braces amount is not equal"))

        newCode = ""
        splitLines = code.splitlines();
        for line in splitLines:
            if ";" in line and not self.StrContains(";", line):
                lineChars = list(line)
                stringCount = 0
                for i in range(len(lineChars)):
                    if lineChars[i] == '"' or lineChars[i] == "'":
                        stringCount += 1
                    if lineChars[i] == ";":
                        if stringCount % 2 == 0:
                            lineChars[i] = "\n"
                            break
                line = "".join(lineChars)
            if "class" in line:
                if not self.StrContains("class", line):
                    line = "\n"+" ".join(line.split())
            if "function" in line:
                if line.partition("function")[0].count("\"") != 0 and line.partition("function")[0].count("\"") % 2 == 0:
                    words = line.split()
                    for wordNo, word in enumerate(words):
                        if word == "function":
                            speechCount = line.partition("function")[2].count("\"")
                            otherCount = line.partition("function")[2].count("'")
                            if speechCount % 2 == 0 and otherCount % 2 == 0:
                                words[wordNo] = "def"
                                break
                    line = " ".join(words)
            leftBraceExpression = ''.join(line.split())
            if not self.StrContains("{", leftBraceExpression):
                if ''.join(line.split()).startswith(("{")):
                    newCode += ":\n"
            if not self.StrContains("}", line):
                    line = line.replace("}", "#endindent")
            if not self.StrContains("{", line):
                line = line.replace("{", "#startindent")
            line += "\n"
            newCode += line
            line += "\n"

        return code

    def parseComments(self, code):
        for line in code.splitlines():
            words = line.split()
            for idx, word in enumerate(words):
                if word.startswith("//") and not self.StrContains("//", line):
                    code = code.replace(line, line.split("//")[0])
        return code

    def parsePragmas(self, code):
        for line in code.splitlines():
            words = line.split()
            for idx, word in enumerate(words):
                if word == "#pragma" and not self.StrContains("#pragma", line):
                    pragmaName = words[idx+1]
                    val = words[idx+2:]
                    setattr(self, pragmaName, val)
                    code = code.replace(line, "")
                elif word == "#parse":
                    self.parse(line[1:], True)

        return code

    def ParseKeywords(self, code):
        for line in code.splitlines():
            words = line.split()
            for idx, word in enumerate(words):
                code = code.replace(line, line.replace("else if", "elif"))
                if word == "fn" and not self.StrContains("fn", line):
                    code = code.replace(line, line.replace("fn", "def"))
                if word == "structure" and not self.StrContains("structure", line):
                    code = code.replace(line,  line.replace("structure", "class"))
                
                if word == "const" and not self.StrContains("const", line):
                    varname = words[idx+1]

                    code = code.replace(line, line.replace(f"const {varname}", varname.upper()))
                    for l in code.splitlines():
                        if varname in l and not self.StrContains(varname,l):
                            code = code.replace(l, l.replace(varname, varname.upper()))
            
        return code

    def ParseImports(self, code):
        for line in code.splitlines():
            words = line.split()
            for idx, word in enumerate(words):
                if word == "from" and not self.StrContains("from", line):
                    if words[idx+1] == "native":
                        if words[idx+2] == "import":
                            import_name = words[idx+3]
                            code = code.replace(line, f"from {import_name} import *")

                        elif words[idx+2] == "reference":
                            import_name = words[idx+3]
                            code = code.replace(line, f"import {import_name}")

                elif word == "#include" and not self.StrContains("#include", line):
                    importName = words[idx+1].strip("<>")
                    for i in self.path:
                        if os.path.exists(i+"/"+importName+".jns"):
                            if importName in self._imports: continue
                            with open(i+"/"+importName+".jns","r") as f:
                                nc = self.parse(f.read(), True)
                                if not nc in code:
                                    code = code.replace(line, nc)
                            self._imports.append(importName)
        return code
    
    
    def StrContains(self, pattern, line):
        if not pattern in line: return False

        if not "\"" in line: return False
        else:
            firstquote = line.find('"')
            qc = 1
            lastquote = -1
            for l in range(len(line[firstquote+1:])):
                if line[l] == '"':
                    lastquote = l

            return pattern in line[firstquote:lastquote]
