import datetime

HTML = ["<head>" + "\n","<title>Timing Graph</title>\n", "<!-- Plotly.js -->" + "\n", "<script src='plotly.js'></script>" + "\n",
        "</head>"+"\n","<body >"+"\n", "<div id='myDiv' style='width: 100%; height: 500px;'></div>"+"\n",
        "<script>"]
if __name__ == '__main__':
    for line in HTML:
        a= list(map(int,input("eneter")))
        print(a)