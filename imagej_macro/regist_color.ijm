arg = getArgument();

if(arg==""){
    print("set filename");
    exit;
}

filename_base = substring(arg, 0, 16);
filename = substring(arg, 0, 20);
slice_id = substring(arg, 21, 25);
print("Arg=[" + filename + "] [" + slice_id + "]");


HomeDir = "/data/registration/Test/";
GrayFilePath = HomeDir+"work4/"+filename_base+"/"+slice_id+".tif";
ColorFilePath = HomeDir+"work3/"+filename;

GrayFileName = slice_id+".tif";
ColorFileName = filename;
OutputFilePath = "work5/"+filename;

print(GrayFilePath);
print(ColorFilePath);
print(GrayFileName);
print(ColorFileName);

open(GrayFilePath);
open(ColorFilePath);

list = getList("image.titles");
print(list.length);
print(list[0]);
print(list[1]);

//exec_args = "source_image="+ColorFileName+" target_image="+GrayFileName+" registration=Accurate image_subsample_factor=0 initial_deformation=[Very Coarse] final_deformation=Fine divergence_weight=0 curl_weight=0 landmark_weight=0 image_weight=1 consistency_weight=10 stop_threshold=0.01";

exec_args = "source_image="+list[1]+" target_image="+list[0]+" registration=Accurate image_subsample_factor=0 initial_deformation=[Very Coarse] final_deformation=Fine divergence_weight=0 curl_weight=0 landmark_weight=0 image_weight=1 consistency_weight=10 stop_threshold=0.01";
print(exec_args);

run("bUnwarpJ", exec_args);

//selectWindow("Registered Source Image");
//run("Make Substack...", "  slices=1");
//saveAs("Tiff", OutputFilePath);
