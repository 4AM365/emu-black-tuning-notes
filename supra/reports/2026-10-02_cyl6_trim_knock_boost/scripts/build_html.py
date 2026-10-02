"""Embed data/report_data.json into template.html -> ../report.html (standalone page)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
import json
d = json.load(open(os.path.join(HERE, "..", "data", "report_data.json"), encoding="utf-8"))
d["q"] = json.load(open(os.path.join(HERE, "..", "data", "questions.json"), encoding="utf-8"))
d = json.dumps(d, separators=(",", ":"))
head, body = t.split("</style>", 1)
page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head + "</style>\n</head>\n<body>" + body.replace("__DATA__", d) + "</body>\n</html>\n")
open(os.path.join(HERE, "..", "report.html"), "w", encoding="utf-8").write(page)
print("wrote report.html", len(page) // 1000, "kB")
