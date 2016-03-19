import vtk
#import matplotlib.cm as cm
import sys

LABEL_NAMES = [\
'olfactory bulb',
'cerebral cortex',
'lateral septal nuclei',
'striatum',
'globus pallidus',
'thalamus',
'hypothalamus',
'hippocampal formation',
'superior colliculus',
'inferior colliculus',
'cerebellum',
'fimbria',
'internal capsule',
'ventricle',
'ventricle',
'corpus callosum',
'subcommissural organ',
'anterior commissure',
'paraflocculus',
'deep mesencephalic nucleus',
'fornix',
'aqueaduct',
'pineal gland',
'substantia nigra',
'brainstem (remainder)',
'pontine gray',
'fasciculus retroflexus',
'amygdala',
'interpeduncular nucleus',
'periacueductal gray',
'nucleus accumbens',
'optic chiasm',
'supraoptic decussation',
'optic tract',
'lateral lemniscus',
'epithalamus',
'mammillary nucleus',
'cochlear nuclei and nerve'
]

def read_intensity_data(filename):
    int_data = {}
    fp = open(filename, 'r')
    lines = fp.readlines()
    for line in lines:
        splited = line.strip().split(',')
        int_data[int(splited[0])] = float(splited[1])

    return int_data


def draw_scene(int_filename, color_mode=0, screen_name=None):
    ###############################################################################
    # read polydata file
    #
    offscreen = False
    draw_axes = False
    
    segs = []
    segs_mapper = []
    segs_actor = []
    transforms = []
    transforms_filter = []

    seg_fileformat = '/mnt/data1/bah2015/seg2/seg%05d.vtk'
    #seg_fileformat = '/media/nebula/data/bah/vtk/seg%05d.vtk'
    #int_filename = '../matching_area/result.txt'

    int_data = read_intensity_data(int_filename)
    int_sum = sum(int_data.values())
    int_average = int_sum / 39
    int_data_sorted = {}
    
    transform = vtk.vtkTransform()
    transform.RotateWXYZ(90, 0, 1, 0)
    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetTransform(transform)
        

    for i in range(1, 39):
        segs.append(vtk.vtkPolyDataReader())
        segs[-1].SetFileName(seg_fileformat % i)

        transforms.append(vtk.vtkTransform())
        #transforms[-1].RotateWXYZ(90., 0, 1, 0)
        transforms_filter.append(vtk.vtkTransformPolyDataFilter())
        transforms_filter[-1].SetTransform(transforms[-1])
        transforms_filter[-1].SetInputConnection(segs[-1].GetOutputPort())
        transforms_filter[-1].Update()

        segs_mapper.append(vtk.vtkPolyDataMapper())
        #segs_mapper[-1].SetInputConnection(segs[-1].GetOutputPort())
        segs_mapper[-1].SetInputConnection(transforms_filter[-1].GetOutputPort())
        segs_actor.append(vtk.vtkActor())
        segs_actor[-1].SetMapper(segs_mapper[-1])
        segs_actor[-1].GetProperty().SetOpacity(0.1)
        #segs_actor[-1].GetProperty().SetColor(color[0], color[1], color[2])


    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(64)
    lut.SetHueRange(0.66667, 0.0)
    lut.SetSaturationRange(1, 1)
    lut.SetValueRange(1, 1)
    lut.Build()
    scalar_bar = vtk.vtkScalarBarActor()
    scalar_bar.SetLookupTable(lut)
    scalar_bar.SetNumberOfLabels(4)

    i = 0
    for k, v in sorted(int_data.items(), key=lambda x:x[1], reverse=True):
        if i < 6:
            segs_actor[k-1].GetProperty().SetOpacity(0.7)

            rgb = [0.0, 0.0, 0.0]
            val = float(v - int_average)/(max(int_data.values())-int_average)
            lut.GetColor(val, rgb)
            segs_actor[k-1].GetProperty().SetColor(rgb)

            print ' Rank %d : %s (%d) = %d (%f)' % (i+1, LABEL_NAMES[k-1], k, v, val)
            #print color
            i += 1
            #int_data_sorted[k] = v
        #print 'Lank %5d : %d (%d)' % (i, k, v)

    ###############################################################################
    # draw axis
    #
    if draw_axes:
        axesActor = vtk.vtkAxesActor()


    ###############################################################################
    # prepare rendering
    #
    ren = vtk.vtkRenderer()
    ren.SetBackground(0.0, 0.0, 0.0)

    if draw_axes:
        ren.AddActor(axesActor)

    for seg in segs_actor:
        ren.AddActor(seg)

    ren.AddActor(scalar_bar)

    renWin = vtk.vtkRenderWindow()
    if offscreen:
        renWin.SetOffScreenRendering(True)
    renWin.AddRenderer(ren)
    renWin.SetWindowName('Mouse Brain Viewer 2 + (%s)' % screen_name)
    renWin.SetSize(1600, 1600)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()

    renWin.Render()
    get_screenshot(renWin, screen_name + '_1.png')

    
    for trans in transforms:
        trans.RotateWXYZ(90., 0, 1, 0)
    for trans_filter in transforms_filter:
        trans_filter.Update()
    renWin.Render()
    get_screenshot(renWin, screen_name + '_2.png')

    for trans in transforms:
        trans.RotateWXYZ(90., 0, 1, 0)
    for trans_filter in transforms_filter:
        trans_filter.Update()
    renWin.Render()
    get_screenshot(renWin, screen_name + '_3.png')

    #iren.Start()

def get_screenshot(renWin, filename):
    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(renWin)
    w2if.Update()
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(filename)
    writer.SetInput(w2if.GetOutput())
    writer.Write()
    renWin.Render()



if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    filename = ''

    if(argc >= 2):
        filename = argvs[1]
    else:
        filename = '../matching_area/result.txt'
    
    if(argc >= 3):
        color_mode = int(argvs[2])
    else:
        color_mode = 1

    if(argc >= 4):
        gene_name = argvs[3]
    else:
        gene_name = 'GENE_NAME'

    print '************ %s ************' % gene_name
    draw_scene(filename, color_mode, gene_name)
