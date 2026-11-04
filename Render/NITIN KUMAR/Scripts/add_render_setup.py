# Adds a camera rig, lights and floor for rendering (the original camera points away from the model and the HDRI file is missing)
import bpy, sys, math
from mathutils import Vector
src,out=sys.argv[sys.argv.index('--')+1:][:2]
bpy.ops.wm.open_mainfile(filepath=src)
s=bpy.context.scene
C=Vector((0,0,10))
def look(o,t):
    d=(Vector(t)-o.location); o.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
col=bpy.data.collections.new('Render_Setup'); s.collection.children.link(col)
def cam(name,loc,lens,tgt=C):
    cd=bpy.data.cameras.new(name); cd.lens=lens; cd.clip_end=500
    o=bpy.data.objects.new(name,cd); o.location=loc; col.objects.link(o); look(o,tgt); return o
cf=cam('CAM_Final',(36,-42,17),56,(0,-0.5,10.0)); cf.data.dof.use_dof=True; cf.data.dof.focus_distance=(Vector(cf.location)-C).length-3; cf.data.dof.aperture_fstop=5.6
cam('CAM_Front',(0,-60,10),50); cam('CAM_Side',(60,0,10),50,(0,0,10)); cam('CAM_Top',(0,0,70),50,(0,0,0))
cam('CAM_Close_Valvetrain',(12,-14,21),50,(0,0,15.5)); cam('CAM_Close_Crank',(14,-16,9),50,(0,0,7.8))
def light(name,typ,loc,energy,size,color,tgt=C):
    ld=bpy.data.lights.new(name,typ); ld.energy=energy; ld.color=color
    if typ=='AREA': ld.size=size
    o=bpy.data.objects.new(name,ld); o.location=loc; col.objects.link(o); look(o,tgt); return o
light('Key_Area','AREA',(24,-30,24),16000,12,(1,0.93,0.85))
light('Rim_Area','AREA',(-18,20,24),12000,8,(0.75,0.85,1))
light('Fill_Area','AREA',(-30,-24,10),4500,16,(0.9,0.95,1))
bpy.ops.mesh.primitive_plane_add(size=400,location=(0,0,1.3)); fl=bpy.context.object; fl.name='Floor'
for c in fl.users_collection: c.objects.unlink(fl)
col.objects.link(fl)
m=bpy.data.materials.new('M_Floor'); m.use_nodes=True; p=m.node_tree.nodes['Principled BSDF']
p.inputs['Base Color'].default_value=(0.03,0.03,0.035,1); p.inputs['Roughness'].default_value=0.35; fl.data.materials.append(m)
# world: missing HDRI -> dark gradient-free grey
nt=s.world.node_tree; bg=[n for n in nt.nodes if n.type=='BACKGROUND'][0]
for l in list(nt.links):
    if l.to_node==bg: nt.links.remove(l)
bg.inputs['Color'].default_value=(0.012,0.012,0.015,1); bg.inputs['Strength'].default_value=1
for o in list(s.objects):
    if o.type=='LIGHT' and o.name=='Light': o.data.energy=2
s.camera=cf
s.render.resolution_x=1920; s.render.resolution_y=1080
s.view_settings.view_transform='AgX'
try: s.view_settings.look='AgX - Medium High Contrast'
except: pass
s.cycles.device='CPU'; s.cycles.samples=64; s.cycles.use_denoising=True
s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
print("SAVED",out)
