open("/home/ikeno/BAH/work1/CD03271-IS-BR-21.tif");
rename("bin");
open("/home/ikeno/BAH/work2/CD03271-IS-BR-21.tif");
imageCalculator("AND create", "CD03271-IS-BR-21.tif","bin");
selectWindow("Result of CD03271-IS-BR-21.tif");
saveAs("Tiff", "/home/ikeno/BAH/work3/CD03271-IS-BR-21.tif");
run("Quit");

