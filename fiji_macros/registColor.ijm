open("./work4/CD48364-IS-BR-21/0128.tif");
open("./work3/CD48364-IS-BR-21.tif");
run("bUnwarpJ", "source_image=CD48364-IS-BR-21.tif target_image=0128.tif registration=Accurate image_subsample_factor=0 initial_deformation=[Very Coarse] final_deformation=Fine divergence_weight=0 curl_weight=0 landmark_weight=0 image_weight=1 consistency_weight=10 stop_threshold=0.01");
selectWindow("Registered Source Image");
run("Make Substack...", " slices=1");
saveAs("Tiff", "./work5/CD48364-IS-BR-21.tif");
run("Quit");
