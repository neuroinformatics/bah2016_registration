open("./DM/work4/CD00002-IS-BR-21/0120.tif");
open("./DM/work3/CD00002-IS-BR-21.tif");
run("bUnwarpJ", "source_image=CD00002-IS-BR-21.tif target_image=0120.tif registration=Accurate image_subsample_factor=0 initial_deformation=[Very Coarse] final_deformation=Fine divergence_weight=0 curl_weight=0 landmark_weight=0 image_weight=1 consistency_weight=10 stop_threshold=0.01");
selectWindow("Registered Source Image");
run("Make Substack...", " slices=1");
saveAs("Tiff", "./work5/CD00002-IS-BR-21.tif");
run("Quit");
