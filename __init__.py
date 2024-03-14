# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


bl_info = {
    "name" : "QATB",
    "author" : "KatGreene",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Animation"
}


import bpy
from .addon.classes import core as co
from .addon.classes import panels as pa
from .addon.classes import properties as pr


classes = (
    pa.QATB_SoundBakePanel,
    pa.QATB_PT_BeatGeneratingPanel,
    pr.QATB_SoundBakeProperties,
    pr.QATB_AddArrayProperties,
    co.QATB_OT_SoundBakeOperator,
    co.QATB_OT_BakeSelectedByStep,
    co.QATB_OT_ScaleCurveValue,
    co.QATB_OT_CreateNodeGroup,
    co.QATB_OT_SetValueKeyframe,
    co.QATB_OT_QuickAddArray,
)


properties = [
    ("sound_bake", bpy.props.PointerProperty(type=pr.QATB_SoundBakeProperties)),
    ("add_array_props", bpy.props.PointerProperty(type=pr.QATB_AddArrayProperties)),
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    for prop_name, prop_value in properties:
        setattr(bpy.types.Scene, prop_name, prop_value)

    print("QATB Registered")


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    for prop_name, _ in properties:
        delattr(bpy.types.Scene, prop_name)


if __name__ == "__main__":
    register()

