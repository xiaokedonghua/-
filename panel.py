import bpy
from . import global_var
import os

class BAC_PT_Panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "小柯动画"
    bl_label = "小柯动画插件"
   
    def draw(self, context):
        layout = self.layout
        
        scene = context.scene

        # BUTTONS
        layout.row().prop(scene, "mode_table", expand=True)
        layout.separator()

        # BUTTONS
        layout.row().prop(scene, "role_table", expand=True)
        layout.separator()

        if scene.mode_table == 'USER':
        
            # 选中的是角色框
            if scene.role_table == 'ROLE':
                # 选择预设
                row = layout.row()
                row.prop(scene, "char_table", text='映射类型')
                

                # # 选择角色类型
                # if scene.char_table == 'CART-M':
                #     scene.mblab_character_name = 'f_as01'

                # elif scene.char_table == 'CART-W':
                #     scene.mblab_character_name = 'f_an02'


                # 一键生成角色
                row = layout.row()
                row.prop(scene, "mblab_character_name", text='角色类型')

                # 一键生成角色

                row = layout.row()
                row.operator('xkdh.new_cartman01', text='卡通男-平和', icon='USER')

                row = layout.row()
                row.operator('xkdh.new_cartman02', text='卡通男-高冷', icon='USER')

                row = layout.row()
                row.operator('xkdh.new_cartwoman01', text='卡通女-平和', icon='USER')

                row = layout.row()
                row.operator('xkdh.new_cartwoman02', text='卡通女-高冷', icon='USER')

                row = layout.row()
                row.operator('xkdh.new_realman01', text='写实男-白人', icon='USER')

                row = layout.row()
                row.operator('xkdh.new_realwoman01', text='写实女-白人', icon='USER')

                # bpy.types.Scene.fbx_name = use_action.get_fbx_file('./data/user_action/')
                # box = layout.box()
                # s = bpy.context.object.xkdh
                # box.template_list(listtype_name='XKDH_UL_mappings', list_id='', dataptr=bpy.context.scene, propname='fbx_name', active_dataptr=s, active_propname='active_mapping')
              
                pass

            elif scene.role_table == 'ACTION':
                if context.object != None and context.object.type == 'ARMATURE':
                    s = bpy.context.object.xkdh
                    
                    split = layout.row().split(factor=0.25)
                    split.column().label(text='映射目标:')
                    split.column().label(text=context.object.name, icon='ARMATURE_DATA')
                    # layout.prop(s, 'mybone_source', text='我的骨骼', icon='ARMATURE_DATA')
                    layout.prop(s, 'selected_source', text='动作来源', icon='ARMATURE_DATA')
                    layout.separator()
                    
                    if s.source == None:
                        layout.label(text='选择另一骨架对象作为动作来源以继续操作', icon='INFO')

                    # 骨骼显示在前
                    row = layout.row()
                    row.operator('xkdh.display_front', text='骨骼显示在前/后', icon='CONSTRAINT_BONE')

                    # 导入一个动作FBX
                    row = layout.row(heading="动作导入", align=True)
                    row.prop(scene, "import_name", text='动作')
                    row.operator('xkdh.import_fbx', text='导入', icon='CONSTRAINT_BONE')
                    # row.operator('import_scene.fbx', text='导入', icon='CONSTRAINT_BONE')

                    # 骨骼约束
                    # 运动方向应该判定位移骨骼约束是否完成, 做标志位=1时展示
                    # if '复制位置' in bpy.context.object.pose.bones['root'].constraints.keys():
                    # row = layout.row(heading="绑定运动方向", align=True)
                    # row.prop(bpy.context.object.pose.bones['root'].constraints, "use_x", text="X", toggle=True)
                    # row.prop(bpy.context.object.pose.bones['root'].constraints, "use_y", text="Y", toggle=True)
                    # row.prop(bpy.context.object.pose.bones['root'].constraints, "use_z", text="Z", toggle=True)
                    row = layout.row(heading="骨骼约束", align=True)
                    row.operator('xkdh.add_action', text='绑定', icon='CONSTRAINT_BONE')
                    row.operator('xkdh.clear', text='解绑', icon='CONSTRAINT_BONE')

                    
                    # 插帧
                    row = layout.row(heading="插帧范围", align=True)
                    row.prop(scene, "copy_starttime", text='起始帧')
                    row.prop(scene, "copy_endtime", text='结束帧')
                    row = layout.row()
                    row.operator('xkdh.insert_keyframe', text='插帧', icon='CONSTRAINT_BONE')
                    row.operator('xkdh.clear_keyframe', text='清空', icon='CONSTRAINT_BONE')


                else:
                    layout.label(text='未选中骨架对象', icon='ERROR')

            elif scene.role_table == 'EXPRESSION':
                
                if context.object != None and context.object.type == 'ARMATURE':
                    s = bpy.context.object.xkdh
                    
                    split = layout.row().split(factor=0.25)
                    split.column().label(text='映射目标:')
                    split.column().label(text=context.object.name, icon='ARMATURE_DATA')
                    layout.prop(s, 'selected_source', text='动作来源', icon='ARMATURE_DATA')
                    layout.separator()
                    
                    if s.source == None:
                        layout.label(text='选择另一骨架对象作为动作来源以继续操作', icon='INFO')
                    else:
                        
                        row = layout.row()
                        row.prop(s, 'preview', text='预览约束', icon= 'HIDE_OFF' if s.preview else 'HIDE_ON')
                        
                        row = layout.row()
                        row.operator('xkdh.bake', text='烘培动画', icon='NLA')
                        row.operator('xkdh.bake_collection', text='批量烘培动画', icon='NLA', )

                else:
                    layout.label(text='未选则需要更改表情的对象', icon='ERROR')

        # 开发模式
        elif scene.mode_table == 'DEVELOPER':
            # 选中的是角色框
            if scene.role_table == 'ROLE':

                # bpy.types.Scene.useraction_table = bpy.props.EnumProperty(
                # items = use_action.build_fbx_list('./data/user_action/'))
                # 选择预设
                row = layout.row()
                row.prop(scene, "char_table", text='映射类型')

                # 一键生成角色
                row = layout.row()
                row.prop(scene, "mblab_character_name", text='角色类型')

                # 用户DIY的FBX
                row = layout.row()
                row.prop(scene, "useraction_table", text='映射类型')

            elif scene.role_table == 'ACTION':
                s = bpy.context.object.xkdh
                    
                split = layout.row().split(factor=0.25)
                split.column().label(text='映射目标:')
                split.column().label(text=context.object.name, icon='ARMATURE_DATA')
                # layout.prop(s, 'mybone_source', text='我的骨骼', icon='ARMATURE_DATA')
                layout.prop(s, 'selected_source', text='动作来源', icon='ARMATURE_DATA')
                layout.separator()
                
                if s.source == None:
                    layout.label(text='选择另一骨架对象作为动作来源以继续操作', icon='INFO')
                else:
                    row = layout.row()
                    row.prop(scene, "map_table", text='映射类型')


                # 一键解除绑定
                row = layout.row(heading="绑定运动方向", align=True)
                row.prop(scene, "copy_loc_x", text="X", toggle=True)
                row.prop(scene, "copy_loc_y", text="Y", toggle=True)
                row.prop(scene, "copy_loc_z", text="Z", toggle=True)
                row = layout.row()
                row.operator('xkdh.bind', text='一键绑定', icon='ADD')
                row.operator('xkdh.clear', text='一键解绑', icon='REMOVE')

                # 插帧
                row = layout.row(heading="插帧范围", align=True)
                row.prop(scene, "copy_starttime", text='起始帧')
                row.prop(scene, "copy_endtime", text='结束帧')
                row = layout.row()
                row.operator('xkdh.insert_keyframe', text='插帧', icon='CONSTRAINT_BONE')
                row.operator('xkdh.clear_keyframe', text='清空', icon='CONSTRAINT_BONE')
                
                # 一键眨眼
                row = layout.row()
                row.operator('xkdh.blink', text='一键眨眼', icon='MONKEY')

                row = layout.row()
                row.operator('xkdh.bake', text='烘培动画', icon='NLA')
                row.operator('xkdh.bake_collection', text='批量烘培动画', icon='NLA', )

                # 导出fbx
                row = layout.row()
                row.prop(scene, "export_name", text="动作名")
                row.operator('xkdh.export_fbx', text='导出', icon='CONSTRAINT_BONE')
                row = layout.row()
                row.operator('xkdh.user_fbx_folder', text='文件夹位置', icon='CONSTRAINT_BONE')
                # row = layout.row()
                # row.label(text='使用预设:')
                # row.menu(mapping.BAC_MT_presets.__name__, text=mapping.BAC_MT_presets.bl_label)
                # row.operator(mapping.AddPresetBACMapping.bl_idname, text="", icon='ADD')
                # row.operator(mapping.AddPresetBACMapping.bl_idname, text="", icon='REMOVE').remove_active=True
                # use_action.draw_panel(layout.box())

            
            elif scene.role_table == 'EXPRESSION':
                pass

preview_collections = {}

class XKDH_PT_Panel2(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "小柯动画"
    bl_label = "技巧教程 + 插件更新"

    def draw(self, context):
        layout = self.layout
        layout.label(text='----------------   插件使用教程   详见公众号    ------------------')
        layout.label(text='该插件永久免费, 只为帮助大家做动画更轻松', icon='BLENDER')
        layout.label(text='关注公众号, 可以观看最新的插件教程哦', icon='BLENDER')
        layout.operator('xkdh.gongzhonghao', text='公众号: 小柯讲动画', icon='URL')

        layout.label(text='----------------   动画教学直播   来抖音直播间   ------------------')
        layout.label(text='想做好的动画, 需要对内容细节有很好的把握', icon='BLENDER')
        layout.label(text='关注我的抖音直播, 小白也能轻易上手哦~', icon='BLENDER')
        layout.operator('xkdh.douyin', text='抖音号: 小柯讲动画', icon='URL')
     
        row = layout.row()
        row.operator('xkdh.update', text='插件更新', icon='URL')


classes = (
	BAC_PT_Panel, 
    XKDH_PT_Panel2,

)

