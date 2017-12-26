open("./work5/CD09503.1-Foxp1.tif");
open("./SB_bin/Reslice_WHS_0.6.1_Labels_fixed_bin0111.tif");
run("bUnwarpJ", "source_image=CD09503.1-Foxp1.tif target_image=Reslice_WHS_0.6.1_Labels_fixed_bin0111.tif registration=Accurate image_subsample_factor=0 initial_deformation=[Very Coarse] final_deformation=Fine divergence_weight=0 curl_weight=0 landmark_weight=0 image_weight=1 consistency_weight=10 stop_threshold=0.01");
selectWindow("Registered Source Image");
run("Make Substack...", " slices=1");
saveAs("Tiff", "./work6/CD09503.1-Foxp1.tif");
run("Quit");
