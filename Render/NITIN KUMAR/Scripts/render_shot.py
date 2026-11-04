import bpy, sys, time
a=sys.argv[sys.argv.index('--')+1:]
src,out,camname,pct,samples=a[0],a[1],a[2],int(a[3]),int(a[4]); mode=a[5] if len(a)>5 else 'beauty'
bpy.ops.wm.open_mainfile(filepath=src)
s=bpy.context.scene; s.camera=bpy.data.objects[camname]
s.render.resolution_percentage=pct; s.cycles.samples=samples; s.cycles.device='CPU'
try: s.cycles.denoiser='OPENIMAGEDENOISE'
except: pass
if camname in('CAM_Front','CAM_Side','CAM_Top'):
    c=s.camera.data; c.type='ORTHO'; c.ortho_scale=21; s.render.resolution_x=1080; s.render.resolution_y=1350 if camname!='CAM_Top' else 1080; s.view_settings.exposure=1.3
if mode=='clay':
    m=bpy.data.materials.new('Clay'); m.use_nodes=True; p=m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value=(0.55,0.55,0.55,1); p.inputs['Roughness'].default_value=0.55
    for o in s.objects:
        if o.type=='MESH' and o.name!='Floor':
            for sl in o.material_slots: sl.link='OBJECT'; sl.material=m
if mode=='wire':
    s.render.engine='BLENDER_WORKBENCH'; sh=s.display.shading
    sh.light='STUDIO'; sh.color_type='SINGLE'; sh.single_color=(0.75,0.75,0.78); sh.show_cavity=True
    s.render.use_freestyle=True; s.render.line_thickness=0.6
    vl=s.view_layers[0]; vl.use_freestyle=True
    ls=vl.freestyle_settings.linesets[0] if vl.freestyle_settings.linesets else vl.freestyle_settings.linesets.new('L')
    ls.select_by_visibility=True; ls.select_crease=True; ls.select_silhouette=True; ls.select_border=True
    bpy.data.objects['Floor'].hide_render=True
    s.world.color=(0.02,0.02,0.025)
s.render.filepath=out
try: s.render.image_settings.media_type='IMAGE'
except: pass
s.render.image_settings.file_format='PNG'
t=time.time(); bpy.ops.render.render(write_still=True); print("RENDER_TIME",camname,mode,round(time.time()-t,1))
