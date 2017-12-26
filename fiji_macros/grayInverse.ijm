open("/home/ikeno/BAH/work2/CD03271-IS-BR-21.tif");
run("8-bit");
run("Invert");
//run("Brightness/Contrast...");
run("Enhance Contrast", "saturated=0.35");
run("Apply LUT");
saveAs("Tiff", "/home/ikeno/BAH/work2gray_inv/CD03271-IS-BR-21.tif");
run("Quit");
