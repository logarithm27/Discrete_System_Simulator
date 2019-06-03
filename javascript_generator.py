HTML = ["<head>" + "\n","<title>Timing Graph</title>\n", "<!-- Plotly.js -->" + "\n", "<script src='plotly.js'></script>" + "\n",
        "</head>"+"\n","<body onload='hideLogo()' >"+"\n", "<div id='timing_graph' style='width: 100%; height: 500px;'></div>"+"\n",
        "<div id='probabilities' style='width: 100%; height: 500px;'></div>\n",
        "<script>"]
if __name__ == '__main__':
    for line in HTML:
        a= list(map(int,input("eneter")))
        print(a)