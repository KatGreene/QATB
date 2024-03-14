from typing import Set
import bpy
from math import log, exp

from bpy.types import Context, Operator
from . import functions as func


class QATB_OT_SoundBakeOperator(Operator):
    bl_label = "Bake Sound"
    bl_idname = "qatb.sound_bake_operator"
    
    def execute(self, context):           
        func.qatb_bake_sound()

        self.report({'INFO'}, "已烘焙关键帧曲线")
        bpy.ops.ed.undo_push(message="QATB: 烘焙曲线")
        return {'FINISHED'}


class QATB_OT_BakeSelectedByStep(bpy.types.Operator):
    bl_label = "Bake Selected"
    bl_idname = "qatb.bake_selected_by_step"
    
    def execute(self, context):
        area = context.area.type
        scene = bpy.context.scene
        sound_bake_props = scene.sound_bake

        if bpy.context.area.type != 'GRAPH_EDITOR':
            bpy.context.area.type = 'GRAPH_EDITOR'

        if not sound_bake_props.audio_file_path:
            self.report({'ERROR'}, "请选择音频")
            return {'CANCELLED'}

        selected_objects = sorted(bpy.context.selected_objects, key=lambda obj: obj.name)

        object_count = len(selected_objects)
        low_frequency = sound_bake_props.low_frequency
        high_frequency = sound_bake_props.high_frequency
        if sound_bake_props.log_mode:
            frequency_step = (log(high_frequency) - log(low_frequency)) / object_count
        else:
            frequency_step = (high_frequency - low_frequency) / object_count
        
        for obj in selected_objects:
            if not obj.type == 'MESH':
                continue

            sound_bake_props = scene.sound_bake

            if sound_bake_props.log_mode:
                high_frequency = exp(log(low_frequency)+frequency_step)
            else:
                high_frequency = low_frequency + frequency_step

            bpy.context.view_layer.objects.active = obj

            bpy.context.scene.frame_set(scene.frame_current)
            # fc_data_path = "scale"
            # fc_index = 2  # X轴为0，Y轴为1，Z轴为2
            # obj.keyframe_insert(data_path=fc_data_path, index=fc_index, frame=0)
            func.qatb_insert_keyframe()
            
            bpy.ops.graph.sound_bake(filepath=sound_bake_props.audio_file_path,
                                    low=low_frequency,
                                    high=high_frequency,
                                    attack=sound_bake_props.attack_time,
                                    release=sound_bake_props.release_time,
                                    threshold=sound_bake_props.threshold)
            
            action = obj.animation_data.action
            for fcu in action.fcurves:
                fcu.select = False

            if sound_bake_props.log_mode:
                low_frequency = exp(log(low_frequency)+frequency_step)
            else:
                low_frequency += frequency_step
            
            bpy.context.view_layer.update()

        bpy.context.area.type = area

        self.report({'INFO'}, "批量烘焙已完成")
        bpy.ops.ed.undo_push(message="QATB: 批量烘焙")
        return {'FINISHED'}
    

class QATB_OT_ScaleCurveValue(bpy.types.Operator):
    bl_label = "Scale Curve"
    bl_idname = "qatb.scale_curve_value"
    
    def execute(self, context):
        scene = bpy.context.scene
        sound_bake_props = scene.sound_bake

        scale_factor = sound_bake_props.scale_factor
        selected_objects = sorted(bpy.context.selected_objects, key=lambda obj: obj.name)

        # bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        data_path = sound_bake_props.fc_data_path
        index_mapping = {"X": 0, "Y": 1, "Z": 2}
        index = index_mapping.get(sound_bake_props.fc_index, 0)

        func.qatb_delete_all_fcurve_modifiers()

        for obj in selected_objects: 
            if not obj.type == 'MESH':
                continue

            action = obj.animation_data.action
            fcurves = obj.animation_data.action.fcurves
            fcurve = fcurves.find(data_path, index=index)
            
            if fcurve is None:
                fcurve = fcurves.new(data_path, index=index)

            for fcu in action.fcurves:
                fcu.select = True

            bpy.ops.graph.fmodifier_add(type='ENVELOPE')
                
            # 获取最新添加的修改器
            for mod in fcurve.modifiers:
                if mod.type == 'ENVELOPE':
                    envelope_modifier = mod
                    break
            else:
                raise Exception("ENVELOPE修改器没有被成功添加")
                
            # 设置修改器的属性，如默认值和控制点
            envelope_modifier.default_min = -1.0
            envelope_modifier.default_max = 1.0

            # 添加控制点，需要给定帧(frame) 和 控制点的最小值(min) 和 最大值(max)
            control_point = envelope_modifier.control_points.add(0)
            control_point.min = -scale_factor
            control_point.max = scale_factor

            for fcu in action.fcurves:
                fcu.select = False

        bpy.ops.ed.undo_push(message="QATB: 缩放曲线")
        return {'FINISHED'}
    

# 操作按钮
class QATB_OT_CreateNodeGroup(bpy.types.Operator):
    """创建一个新的材质和节点组并将节点依次链接到组输出"""
    bl_idname = "qatb.create_node_group"
    bl_label = "生成节点组 Values"

    def execute(self, context):
        # 获取选中物体数量，用于创建相应数量的Value节点
        selected_objects = context.selected_objects
        num_values = len(selected_objects)
        
        # 创建一个新的节点组
        node_tree = bpy.data.node_groups.new(name='QATB_ValueNodesGroup', type='ShaderNodeTree')
        
        # 创建组输出节点，并添加足够数量的输出插槽
        group_output_node = node_tree.nodes.new('NodeGroupOutput')
        group_output_node.location = (200, 0)
        for i in range(num_values):
            node_tree.outputs.new('NodeSocketFloat', 'QATM_Value {}'.format(i+1))
        
        # 创建Value节点，并将它们链接到组输出的相应插槽
        for i in range(num_values):
            value_node = node_tree.nodes.new('ShaderNodeValue')
            value_node.location = (-200, i * -200)   # 设置每个节点的位置，沿Y轴排列
            value_node.label = "Value " + f"{i}"
            # 链接从Value节点输出到组输出的对应插槽
            links = node_tree.links
            link = links.new(value_node.outputs[0], group_output_node.inputs[i])
        
        # 更新节点位置，使其更加紧凑
        node_tree.nodes.update()
        
        self.report({'INFO'}, "Nodes created and linked.")
        bpy.ops.ed.undo_push(message="QATB: 添加节点")
        return {'FINISHED'}
    

class QATB_OT_SetValueKeyframe(bpy.types.Operator):
    """为节点组内的节点设置关键帧"""
    bl_idname = "qatb.set_value_keyframe"
    bl_label = "设置关键帧"

    def execute(self, context):
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

        data_path = bpy.data.node_groups["QATB_ValueNodesGroup"].nodes["值(明度)"].outputs[0].default_value

        anim_data = mat.node_tree.animation_data_create()
        fcurves = anim_data.action.fcurves
        fcurve = fcurves.new(data_path, index=0)  # 假设是单值输出，如float类型
        
        # 在第一帧和第三十帧插入关键帧
        fcurve.keyframe_points.insert(frame=1, value=1.0)  # 示例值
        fcurve.keyframe_points.insert(frame=30, value=0.5)  # 示例值

        bpy.ops.ed.undo_push(message="QATB: 添加关键帧")
        return {'FINISHED'}
        

class QATB_OT_QuickAddArray(Operator):
    """快速添加立方体阵列"""
    bl_idname = "qatb.quick_add_array"
    bl_label = "添加阵列"

    def execute(self, context):
        scene = bpy.context.scene
        add_array_props = scene.add_array_props
        # 新建一个立方体
        bpy.ops.mesh.primitive_cube_add()
        cube = bpy.context.object

        # 添加阵列修改器，设置数量为10，相对间距为1.5
        array_modifier = cube.modifiers.new(name="Array", type='ARRAY')
        array_modifier.count = add_array_props.array_count
        array_modifier.relative_offset_displace[0] = add_array_props.relative_offset

        # 应用阵列修改器
        bpy.context.view_layer.objects.active = cube
        bpy.ops.object.modifier_apply(modifier="Array")

        # 按松散块分量网格
        bpy.ops.object.editmode_toggle()  # 切换到编辑模式
        bpy.ops.mesh.separate(type='LOOSE')  # 按松散块分割
        bpy.ops.object.editmode_toggle()  # 切换回对象模式

        selected_objects = bpy.context.selected_objects

        # 新建一个空物体
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        empty_object = bpy.context.object
        empty_object.name = "QATB_阵列"

        # 将所有分离出的物体的父级设置为这个新的空物体
        for obj in selected_objects:
            if obj != empty_object:
                obj.parent = empty_object
    

        self.report({'INFO'}, "已添加立方体阵列")
        bpy.ops.ed.undo_push(message="QATB: 添加阵列")
        return {'FINISHED'}