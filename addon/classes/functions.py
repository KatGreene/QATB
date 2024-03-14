# -*- coding: utf-8 -*-

#    <QATB, Blender addon for quick adding time baking.>
#    Copyright (C) <2024> <绿毛猫KatGreene>


import bpy


def qatb_bake_sound():
    scene = bpy.context.scene
    sound_bake_props = scene.sound_bake
    
    bpy.ops.graph.sound_bake(filepath=sound_bake_props.audio_file_path,
                            low=sound_bake_props.low_frequency,
                            high=sound_bake_props.high_frequency,
                            attack=sound_bake_props.attack_time,
                            release=sound_bake_props.release_time,
                            threshold=sound_bake_props.threshold)


def qatb_add_frequency():
    scene = bpy.context.scene
    sound_bake_props = scene.sound_bake

    sound_bake_props.low_frequency += sound_bake_props.freq_step
    sound_bake_props.high_frequency += sound_bake_props.freq_step


def qatb_delete_all_fcurve_modifiers():
    for obj in bpy.context.selected_objects:
        if not obj.type == 'MESH':
                continue
        
        if obj.animation_data:
            for fcurve in obj.animation_data.action.fcurves:
                if fcurve.modifiers:
                    envelop_modifiers = [modifier for modifier in fcurve.modifiers if modifier.type == 'ENVELOPE']
                    for modifier in envelop_modifiers:
                        fcurve.modifiers.remove(modifier)


def qatb_create_location_animation_channel():
    bpy.ops.anim.keyframe_insert_by_name(type="Location")


def qatb_select_z_channel(obj):
    # 选择“Location”关键帧通道的Z通道
    action = obj.animation_data.action
    for fcu in action.fcurves:
        if fcu.data_path == "location":
            if fcu.array_index == 2:  # Z通道的索引是2
                fcu.select = True
            else:
                fcu.select = False


def qatb_insert_keyframe():
    obj = bpy.context.active_object
    scene = bpy.context.scene
    sound_bake_props = scene.sound_bake

    # 从字符串转换为数值
    index_mapping = {"X": 0, "Y": 1, "Z": 2}
    fc_index = index_mapping.get(sound_bake_props.fc_index, 0)

    # 插入关键帧
    obj.keyframe_insert(data_path=sound_bake_props.fc_data_path, index=fc_index, frame=0)

    return {'FINISHED'}


def qatb_create_material():
    # 创建一个新材质
    mat = bpy.data.materials.new(name="QATM_F-Curve")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    # 清除默认节点
    for node in nodes:
        nodes.remove(node)
    
    # 添加QATB_NodeValues节点组
    qatb_group = nodes.new('ShaderNodeGroup')
    qatb_group.node_tree = bpy.data.node_groups.get("QATB_ValueNodesGroup")
    
    # 找到标签为"QATB01"的节点
    for node in qatb_group.node_tree.nodes:
        if node.label == "Value 0":
            qatb01_node = node
            break
    else:
        print("未找到标签为'Value 0'的节点")
        return

    # 为QATB01节点的第一个输出创建F-Curve动画
    qatb_material_animation(mat, qatb01_node, 0)


def qatb_material_animation(material, node, output_index):
    # 获取或创建动画数据
    anim_data = material.node_tree.animation_data_create()
    # 获取或创建操作
    fcurves = anim_data.action.fcurves if anim_data.action else anim_data.action_new().fcurves
    
    # 创建一个新的F-Curve
    data_path = f'nodes["{node.name}"].outputs[{output_index}].default_value'
    fcurve = fcurves.new(data_path, index=0)  # 假设是单值输出，如float类型
    
    # 在第一帧和第三十帧插入关键帧
    fcurve.keyframe_points.insert(frame=1, value=1.0)  # 示例值
    fcurve.keyframe_points.insert(frame=30, value=0.5)  # 示例值


def qatb_get_active_fcurve():
    # 获取激活的通道
    obj = bpy.context.active_object
    if obj and obj.animation_data and obj.animation_data.action:
        fcurves = obj.animation_data.action.fcurves
        for fcurve in fcurves:
            if fcurve.select:  # 检查F-Curve是否被选中
                print(f"激活的F-Curve是: {fcurve.data_path}, index: {fcurve.array_index}")
                return fcurve
    
    return None
    

def qatb_get_selected_fcurves():
    # 获取选中的通道
    selected_fcurves = []
    obj = bpy.context.active_object
    if obj and obj.animation_data and obj.animation_data.action:
        fcurves = obj.animation_data.action.fcurves
        for fcurve in fcurves:
            if fcurve.select:
                selected_fcurves.append(fcurve)
                print(f"选中的F-Curve: {fcurve.data_path}, index: {fcurve.array_index}")

    return selected_fcurves

