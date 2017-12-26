open("/home/ikeno/BAH/data_hc/CD03271-IS-BR-21.tif");
run("8-bit");
run("Auto Threshold", "method=Percentile white");
run("Invert");
run("Scale...", "x=- y=- width=512 height=320 interpolation=Bilinear average create title=CD03271-IS-BR-21.tif");
saveAs("Tiff", "/home/ikeno/BAH/work1/CD03271-IS-BR-21.tif");
close();
run("Quit");
