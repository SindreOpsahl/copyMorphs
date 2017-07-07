# A simple script for batch transferring Morph Maps from one mesh to the other.
# Simply select the mesh you want to transfer to, and then the mesh you want to copy from. The order is important.
# 
# By Sindre Opsahl Skaare 
# https://github.com/SindreOpsahl/copyMorphs

#python
import modo

def transferMaps(target, source):
	#check if the source mesh has any morph maps
	if len(source.geometry.vmaps.morphMaps) >= 1:	
		
		#recreate the morph maps of the source to the target
		for morph in source.geometry.vmaps.morphMaps:
			with target.geometry as mesh:
				mesh.vmaps.addMorphMap(morph.name)
		
		#hide all other other items so we only have a foreground and background mesh for the Transfer tool
		lx.eval('hide.unsel')
		#select the target to be our foreground mesh	
		scene.select(target)
		
		#run the Transfer Vertex Map tool for each of the morph maps
		for morph in source.geometry.vmaps.morphMaps:
			lx.eval('select.vertexMap %s morf replace' % (morph.name))
			lx.eval('vertMap.transfer %s space:local method:distance flip:off completion:true' % (morph.name))
		
		#unhide the previosly hidden items				
		lx.eval('unhide')

	#if the source mesh has no morph maps throw an error and do nothing
	else:	
		modo.dialogs.alert(	'copyMorphs: No Morph Maps', 
							'The source mesh has no Morph Maps', 
							dtype='error')

#establish some shorthands and initate the target and source variables
scene = modo.Scene()
geo = scene.selected
target = 0
source = 0

#establish what is the source and target, based on selection order
if len (geo) == 2:
	target = geo[0]
	source = geo[1]
	transferMaps(target, source)
#throw an error if too many meshes are selected
elif len(geo) > 2:
	modo.dialogs.alert(	'copyMorphs: Too Much Selected', 
						'You can only select two objects. \nThe target first, and the source second', 
						dtype='error')
#throw an error if only one mesh is selected
elif len(geo) == 1:
	modo.dialogs.alert(	'copyMorphs: Only One Mesh Selected', 
						'You need to select two objects. \nThe target first, and the source second', 
						dtype='error')
#throw an error if nothing is selected
elif len(geo) == 0:
	modo.dialogs.alert(	'copyMorphs: Nothing Selected', 
						'You need to select two objects. \nThe target first, and the source second', 
						dtype='error')
