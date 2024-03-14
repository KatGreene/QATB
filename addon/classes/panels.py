# -*- coding: utf-8 -*-

#    <QATB, Blender addon for quick adding time baking.>
#    Copyright (C) <2024> <绿毛猫KatGreene>


import bpy


class QATB_SoundBakePanel(bpy.types.Panel):
    """创建一个面板在曲线视图3D的N键侧栏中"""
    bl_label = "QATB"
    bl_idname = "QATB_PT_SoundBake"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'QATB'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        sound_bake_props = scene.sound_bake

        layout.use_property_split = False
        layout.use_property_decorate = False

        box = layout.box()
        box.label(icon="OPTIONS", text="烘焙选中通道:")
        col = box.column()
        col.prop(sound_bake_props, "audio_file_path", text="文件")
        col.separator()
        col.label(text="频率范围", icon="SEQ_HISTOGRAM")
        col.prop(sound_bake_props, "low_frequency", text="起始", slider=True)
        col.prop(sound_bake_props, "high_frequency", text="截止", slider=True)
        col.separator()
        col.label(text="响应设置", icon="OUTLINER_OB_SPEAKER")
        col.prop(sound_bake_props, "attack_time", text="起音", slider=True)
        col.prop(sound_bake_props, "release_time", text="释放", slider=True)
        col.prop(sound_bake_props, "threshold", text="阈值", slider=True)
        row = box.row()
        row.scale_y = 1.5
        row.operator("qatb.sound_bake_operator", text="烘焙声音曲线", icon="SOUND")
        
        box = layout.box()
        box.label(icon="MOD_HUE_SATURATION", text="增量烘焙通道:")
        row = box.row()
        row.prop(sound_bake_props, "fc_data_path", text="")
        row.prop(sound_bake_props, "fc_index", text="")
        row = box.row()
        row.prop(sound_bake_props, "log_mode", text="", icon="MOD_OFFSET", toggle=True)
        row.label(text="启用对数频率间距")
        row = box.row()
        row.scale_y = 1.5
        row.operator("qatb.bake_selected_by_step", text="选中物体增量烘焙", icon="FILE_SOUND")

        layout.use_property_split = True
        layout.use_property_decorate = False
        box = layout.box()
        col = box.column()
        col.label(text="缩放曲线", icon="FULLSCREEN_ENTER")
        col.prop(sound_bake_props, "scale_factor", text="缩放倍数", slider=True)
        col.operator("qatb.scale_curve_value", text="应用缩放", icon="CHECKMARK")


class QATB_PT_BeatGeneratingPanel(bpy.types.Panel):
    """创建一个面板在曲线视图3D的N键侧栏中"""
    bl_label = "QATB 节奏生成"
    bl_idname = "QATB_PT_BeatGenerating"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'QATB'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        sound_bake_props = scene.sound_bake
        add_array_props = scene.add_array_props

        layout.use_property_split = True
        layout.use_property_decorate = False

        box = layout.box()
        box.label(text="快速添加立方体阵列", icon="MOD_ARRAY")
        col = box.column()
        subcol = col.column(align=True)
        subcol.prop(add_array_props, "array_count", text="阵元数量")
        subcol.prop(add_array_props, "relative_offset", text="相对间距")
        row = box.row()
        row.operator("qatb.quick_add_array", text="添加阵列", icon="ADD")

        box = layout.box()
        row = box.row()
        row.prop(sound_bake_props, "sound_bpm_value", text="设定BPM值")
        row = layout.row()
        row.operator("qatb.create_node_group", text="生成材质节点组", icon="MATERIAL")
        row = layout.row()
        row.operator("qatb.set_value_keyframe", text="设置关键帧", icon="ADD")

