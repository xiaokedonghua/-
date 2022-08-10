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

