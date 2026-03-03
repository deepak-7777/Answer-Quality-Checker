import os
os.environ["LANGUAGE_TOOL_PYTHON_CACHE_DIR"] = r"C:\lt_cache"

import language_tool_python

print("Loading LanguageTool...")
tool = language_tool_python.LanguageTool("en-US")
print("Loaded!")

text = "This are bad sentence with error."
matches = tool.check(text)

print("Errors:", len(matches))
for m in matches[:3]:
    print("-", m.message)