# ##### 声明 #####
# 该插件完全免费, 不得以售卖, 修改插件后售卖等形式进行牟利
# 请勿对插件进行修改后进行二次发布, 若因此产生不良影响及严重后果, 追究二次发布者的责任
# 
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>



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
    "name" : "小柯动画插件",
    "author" : "xiao ke",
    "description" : "小柯动画插件,帮你快速制作动画",
    "blender" : (2, 83, 0),
    "version" : (0, 0, 3),
    "location" : "View 3D > Toolshelf",
    "category" : "Animation",

}

from re import T
import bpy
from . import data
from . import global_var
from . import panel
from . import mapping
from . import newchar
from . import use_action
from . import develop_action
from . import update
# from . import importer
from .utilfuncs import *
import os

def get_user_preferences(context):
    if hasattr(context, "user_preferences"):
        return context.user_preferences

    if hasattr(context, "preferences"):
        return context.preferences

    return None


def add_facemap_for_groups(groups):
    """Creates a face_map called group.name.lower if none exists
    in the active object
    """
    obj = bpy.context.object
    groups = groups if isinstance(groups, (list, tuple)) else [groups]

    for group in groups:
        if not obj.face_maps.get(group.name.lower()):
            obj.face_maps.new(name=group.name.lower())
            obj.facemap_materials.add()

class BODY_UL_structure(bpy.types.UIList):
    def draw_item(self, _context, layout, _data, item, icon, skip, _skip, _skip_):
        fmap = item
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            layout.prop(fmap, "name", text="", emboss=False, icon="FACE_MAPS")
        elif self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text="", icon_value=icon)



class BAC_State(bpy.types.PropertyGroup):
    # 来源骨架
    selected_source: bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, 
        obj: obj.type == 'ARMATURE' and obj != bpy.context.object,
        update=lambda self, 
        ctx: get_state().update_source()
    )

    mybone_source: bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, 
        obj: obj.type == 'ARMATURE',
        update=lambda self, 
        ctx: get_state().update_source()
        # ctx: bpy.data.ksdh.update_source()
    )

    source: bpy.props.PointerProperty(type=bpy.types.Object)
    target: bpy.props.PointerProperty(type=bpy.types.Object)
    
    # 这个mappings 很重要
    mappings: bpy.props.CollectionProperty(type=data.BAC_BoneMapping)
    active_mapping: bpy.props.IntProperty(default=-1)
    
    editing_mappings: bpy.props.BoolProperty(default=False, description="展开详细编辑面板")
    editing_type: bpy.props.IntProperty(description="用于记录面板类型")

    preview: bpy.props.BoolProperty(
        default=True, 
        description="开关所有约束以便预览烘培出的动画之类的",
        update=lambda self, ctx: get_state().update_preview()
    )
    source_collection: bpy.props.PointerProperty(type=bpy.types.Collection)
    
    def update_source(self):
        self.target = bpy.context.object  # 选中骨架
        # self.target = self.mybone_source  # 选中骨架
        self.source = self.selected_source  # 来源骨架

        for m in self.mappings:
            m.apply()
    
    def update_preview(self):
        for m in self.mappings:
            m.mute(not self.preview)
    
    def get_source_armature(self):
        return self.source.data

    def get_target_armature(self):
        return self.target.data
    
    def get_source_pose(self):
        return self.source.pose

    def get_target_pose(self):
        return self.target.pose

    def get_active_mapping(self):
        return self.mappings[self.active_mapping]
    
    def get_mapping_by_source(self, name):
        if name != "":
            for i, m in enumerate(self.mappings):
                if m.source == name:
                    return m, i
        return None, -1

    def get_mapping_by_target(self, name):
        if name != "":
            for i, m in enumerate(self.mappings):
                if m.target == name:
                    return m, i
        return None, -1
    
    def add_mapping(self, target, source):
        # 这里需要检测一下目标骨骼是否已存在映射
        m, i = self.get_mapping_by_target(target)
        # 若已存在，则覆盖原本的源骨骼，并返回映射和索引值
        if m:
            print("目标骨骼已存在映射关系，已覆盖修改源骨骼")
            m.source = source
            return m, i
        # 若不存在，则新建映射，同样返回映射和索引值
        m = self.mappings.add()
        m.selected_target = target
        m.source = source
        return m, len(self.mappings) - 1
    
    def add_mapping_below(self, target, source):
        # i 是索引 len(self.mappings) - 1
        i = self.add_mapping(target, source)[1]
        self.mappings.move(i, self.active_mapping + 1)
        self.active_mapping += 1
    
    def remove_mapping(self, index):
        self.mappings[index].clear()
        self.mappings.remove(index)

    def add_fbx(self, target, source):
        # i 是索引 len(self.mappings) - 1
        i = self.add_mapping(target, source)[1]
        self.mappings.move(i, self.active_mapping + 1)
        self.active_mapping += 1
                

classes = (
    BODY_UL_structure,
	*panel.classes,
	*data.classes,
	*mapping.classes,
    *newchar.classes,
    *use_action.classes,
    *develop_action.classes,
    *update.classes,
    # *importer.classes,
    # *expression.classes,
	BAC_State,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.xkdh = bpy.props.PointerProperty(type=BAC_State)

    
    print("hello ksdh!")

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.xkdh
    print("goodbye ksdh!")
