open("/home/ikeno/BAH/data/CD03271-IS-BR-21.tif");
//run("Brightness/Contrast...");
run("Enhance Contrast", "saturated=0.35");
//run("Apply LUT");
saveAs("Tiff", "/home/ikeno/BAH/data_hc/CD03271-IS-BR-21.tif");
run("Scale...", "x=- y=- width=512 height=320 interpolation=Bilinear average create title=scaled.tif");
//setTool("text");
saveAs("Tiff", "/home/ikeno/BAH/work2/CD03271-IS-BR-21.tif");

close();
run("Quit");
