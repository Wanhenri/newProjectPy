"""
PyNGL is a Python language module designed for publication-quality
visualization of data. PyNGL stands for "Python Interface to the
NCL Graphics Libraries," and it is pronounced "pingle."
      http://www.pyngl.ucar.edu/
"""

__all__ = ['add_annotation', 'add_cyclic', 'add_new_coord_limits', \
           'add_lat_90','add_polygon', 'add_polyline', 'add_polymarker', \
           'add_text', 'asciiread', 'betainc', 'blank_plot', \
           'change_workstation', 'chiinv', 'clear_workstation', 'contour', \
           'contour_map', 'datatondc', 'define_colormap', 'delete_wks', \
           'destroy', 'dim_gbits', 'draw', 'draw_colormap', 'draw_ndc_grid', \
           'end', 'frame', 'free_color', 'fspan', 'ftcurv', 'ftcurvp', \
           'ftcurvpi', 'gaus', 'gc_convert', 'gc_dist', 'gc_inout', \
           'gc_interp', 'gc_qarea', 'gc_tarea', 'generate_2d_array', \
           'get_MDfloat_array', 'get_MDinteger_array', \
           'get_bounding_box', 'get_float', 'get_float_array', \
           'get_integer', 'get_integer_array', 'get_named_color_index', \
           'get_string', 'get_string_array', 'get_workspace_id', \
           'hlsrgb', 'hsvrgb', 'ind', 'int2p', 'labelbar_ndc', 'legend_ndc', \
           'linmsg', 'map', 'maximize_plot', 'merge_colormaps', \
           'natgrid', 'ndctodata', 'new_color', 'new_dash_pattern', \
           'new_marker', 'nice_cntr_levels','nngetp', 'nnsetp', \
           'normalize_angle', 'open_wks', 'overlay', 'panel', 'polygon', \
           'polygon_ndc', 'polyline', 'polyline_ndc', 'polymarker', \
           'polymarker_ndc', 'pynglpath', \
           'read_colormap_file', 'regline', 'remove_annotation', \
           'remove_overlay', 'retrieve_colormap', 'rgbhls', 'rgbhsv', \
           'rgbyiq', 'set_color', 'set_values', 'skewt_bkg', \
           'skewt_plt', 'streamline', 'streamline_map', \
           'streamline_scalar', 'streamline_scalar_map', 'text', \
           'text_ndc', 'update_workstation', 'vector', 'vector_map', \
           'vector_scalar', 'vector_scalar_map', 'vinth2p', 'wmbarb', \
           'wmbarbmap', 'wmgetp', 'wmsetp', 'wmstnm', 'wrf_avo', \
           'wrf_dbz', 'wrf_ij_to_ll', 'wrf_ll_to_ij', \
           'wrf_map_resources', 'wrf_pvo', 'wrf_rh', 'wrf_slp', \
           'wrf_td', 'wrf_tk', 'xy', 'y', 'yiqrgb']

# So we can get path to PyNGL ancillary files
from distutils.sysconfig import get_python_lib

# PyNGL analysis functions
import fplib

import sys
#
# The "netcdftime" module was contributed by Jeffrey Whitaker of NOAA.
# The latest version can be downloaded from:
#
# http://code.google.com/p/netcdf4-python/
#
# from netcdftime import __doc__, __version__
# from netcdftime import *

#
#  Get version number and flag for numpy compatibility.
#
#  Also, get the __array_module__  and __array_module_version__
#  attributes. Note that PyNGL no longer supports Numeric, so 
#  __array_module__ should always be "numpy".
#
import pyngl_version
__version__              = pyngl_version.version
__array_module__         = pyngl_version.array_module
__array_module_version__ = pyngl_version.array_module_version

#
# Test to make sure we can actually load numpy and that we 
# have a reasonable version.
#
try:
  import numpy
#
# If we are dealing with a numpy version that is less than 1.0.0, then
# check the version that PyNGL was built with against this version.
#
  if numpy.__version__[0] == '0' and \
     numpy.__version__ < __array_module_version__:
    print ('Warning: your version of numpy may be older than what PyNGL')
    print ('was built with. You could have compatibility problems.')
    print ('PyNGL was built with numpy version',__array_module_version__,'and you are')
    print ('importing version',numpy.__version__)
except ImportError:
  print ('Cannot find numpy, cannot proceed.')
  sys.exit()

#
# Test to see if we can load masked arrays.
#

try:
  from numpy import ma
  HAS_MA = True
except:
  HAS_MA = False

#
# This function calculates where two lines cross each other.
#
def _find_cross_xy(x1,x2,y11,y12,y21,y22):
  if((x2-x1) == 0 or (y12-y11+y21-y22) == 0):
    x0 = -9999
    y0 = -9999
  else:
    x0 = (x2*y21 - x2*y11 + x1*y12 - x1*y22)/(y12-y11+y21-y22)
    y0 = (y11*y22 - y12*y21) / (y11-y12+y22-y21)
  return [x0,y0]


#
# This function takes "n" Y or X curves, defined on the same set of X
# or Y points, and fills the area between each adjacent curves with
# some given color. Depending on options set by the user, the areas
# between curves can be filled differently if one is greater than
# another.
#
def _fill_bw_xy(wks,plot,xx,yy,res):
#
# Determine whether we're filling between Y curves or X curves.
#
  ndimsx = xx.shape
  ndimsy = yy.shape
  rankx  = len(ndimsx)
  ranky  = len(ndimsy)

  if(rankx == 1 and ranky == 2):
    fill_x = False
    xi = xx
    yi = yy
  else:
    if(rankx == 2 and ranky == 1):
      fill_x = True
      xi = yy
      yi = xx
    else:
      print("_fill_bw_xy: Error: If filling between two curves, one set must be 2D, and the other 1D.")
      return plot

# Check length of arrays.
  dsizes_y = yi.shape
  npts     = xi.shape[0]
  ncurves  = dsizes_y[0]

  if(dsizes_y[1] != npts):
    print("_fill_bw_xy: Error: The rightmost dimension of both arrays must be the same.")
    return plot

  if(ncurves <= 1):
    print("_fill_bw_xy: Error: The leftmost dimension of input array must be at least 2.")
    return plot

  if( not res.has_key("nglXYFillColors") and  \
      not res.has_key("nglXYAboveFillColors") and  \
      not res.has_key("nglXYBelowFillColors") and  \
      not res.has_key("nglXYRightFillColors") and  \
      not res.has_key("nglXYLeftFillColors")):
    return plot     # No resources set, so just return.
  
#
# Check resources. There are five possible resources:
#    nglXYFillColors
#    nglXYAboveFillColors
#    nglXYBelowFillColors
#    nglXYRightFillColors
#    nglXYLeftFillColors
#
# If the first one is set, it overwrites the others. If
# none of them are set, then no fill color will be used.
#
# To make things a little easier, above==right and below==left
#
  if(res.has_key("nglXYFillColors")):
    above_fill_colors = _get_key_value_keep(res,"nglXYFillColors",[-1])
    below_fill_colors = above_fill_colors
  else:
    if(fill_x):
      above_fill_colors = _get_key_value_keep(res,"nglXYRightFillColors",[-1])
      below_fill_colors = _get_key_value_keep(res,"nglXYLeftFillColors",[-1])
    else:
      above_fill_colors = _get_key_value_keep(res,"nglXYAboveFillColors",[-1])
      below_fill_colors = _get_key_value_keep(res,"nglXYBelowFillColors",[-1])
      
  nacol = len(above_fill_colors)
  nbcol = len(below_fill_colors)

#
# Make a copy of the input arrays. Not sure if I need this.
#
  x  = xi
  y  = yi

#
# Create arrays for storing polygon points.
#
  first     = numpy.zeros(2,'f')
  last      = numpy.zeros(2,'f')
  polygon_x = numpy.zeros(2*npts+3,'f')
  polygon_y = numpy.zeros(2*npts+3,'f')

#
# Loop through each set of two curves, filling them as we go.
#
  gsres = Resources()
  plot.polygon = []

  xmsg = _get_fill_value(xi)
  ymsg = _get_fill_value(yi)

  for n in range(0,ncurves-1):
    y1 = yi[n,:]    # Grab the current curve
    y2 = yi[n+1,:]  # and the next curve.
  
    iacol = n % nacol
    ibcol = n % nbcol
#
# Compute a delta that will be used to determine if two points are
# actually the same point. 
#
    range_y1 = max(y1) - min(y1)
    range_y2 = max(y2) - min(y2)

    delta_y1 = 0.01 * range_y1
    delta_y2 = 0.01 * range_y2
    if(delta_y1 == 0):
      delta = delta_y2
    elif(delta_y2 == 0):
      delta = delta_y1
    else:
      delta = min([delta_y1,delta_y2])
      
    npoly = 0     # Number of polygons
#
# First fill in polygons where y1 is above y2, and then fill in
# polygons where y2 is above y1.
#
    for ab in range(0,2):
      gsres.gsFillColor = above_fill_colors[iacol]
      if(ab == 1):
        y1 = yi[n+1,:]
        y2 = yi[n,:]
# Color for when first curve is > second curve
        gsres.gsFillColor = below_fill_colors[ibcol]
#
# Get areas where y1 > y2.
#
      y1_gt_y2 = numpy.ma.where(y1 > y2, True, False)
      msg      = _get_fill_value(y1_gt_y2)

      bpt = -1    # Index of first point of polygon.
      ept = -1    # Index of last point of polygon.
#
# Loop through points.
#
      for i in range(0,npts):
        if(bpt < 0):
          if y1_gt_y2[i]:
            bpt = i
            ept = i
        else:
          if y1_gt_y2[i]:
            ept = i
          
          if(not y1_gt_y2[i] or ept == (npts-1)):
#
# Draw polygon. If bpt is the very first point or ept is the
# very last point, then these are special cases we have to
# handle separately.
#
            if(bpt == 0 or (bpt > 0 and (_ismissing(y1[bpt-1],ymsg) or \
                                         _ismissing(y2[bpt-1],ymsg) or \
                                         _ismissing(x[bpt-1],xmsg)))):
              first[0] =  x[bpt]
              first[1] =  y2[bpt]
            else:
              if(numpy.fabs(y1[bpt-1]-y2[bpt-1]) <= delta):
#
# If the two points are within delta of each other, then we'll
# consider them to be the same point.
#
                first[0] =   x[bpt-1]
                first[1] =  y1[bpt-1]
              else:
#
# Otherwise, find the intersection where the two curves cross.
#
                first = _find_cross_xy(x[bpt-1],x[bpt],y1[bpt-1], \
                                       y1[bpt],y2[bpt-1],y2[bpt])
            
            if(ept == (npts-1) or (ept < (npts-1) and \
               (_ismissing(y1[ept+1],ymsg) or \
                _ismissing(y2[ept+1],ymsg) or \
                _ismissing(x[ept+1],xmsg)))):
              last[0] =   x[ept]
              last[1] =  y2[ept]
            else:
              if(numpy.fabs(y1[ept+1]-y2[ept+1]) <= delta):
#
# If the two points are within delta of each other, then we'll
# consider them to be the same point.
#
                last[0] =   x[ept+1]
                last[1] =  y1[ept+1]
              else:
#
# Otherwise, find the intersection where the two curves cross.
#
                last = _find_cross_xy(x[ept],x[ept+1],y1[ept],y1[ept+1], \
                                     y2[ept],y2[ept+1])
#
# Initialize polygon indexes.
#
            ppts  = ept - bpt + 1
            ppts2 = ppts * 2
# The start of the "forward" points.
            polygon_x[0]              = first[0]
            polygon_y[0]              = first[1]
# The "forward" points.
            polygon_x[1:ppts+1]       = x[bpt:ept+1]
            polygon_y[1:ppts+1]       = y1[bpt:ept+1]
# The start of the "backwards" points.
            polygon_x[ppts+1]         = last[0]
            polygon_y[ppts+1]         = last[1]
# The "backwards" points.
            if bpt == 0:
              polygon_y[ppts+2:ppts2+2] = y2[ept::-1]
              polygon_x[ppts+2:ppts2+2] = x[ept::-1]
            else:
              polygon_y[ppts+2:ppts2+2] = y2[ept:bpt-1:-1]
              polygon_x[ppts+2:ppts2+2] = x[ept:bpt-1:-1]
# Close the polygon.
            polygon_x[ppts2+2]        = first[0]
            polygon_y[ppts2+2]        = first[1]
#
# Make sure polygons get drawn *after* the plot gets drawn.
#
            if(npoly == 0):
              tmpres = Resources()
              tmpres.tfPolyDrawOrder = "Predraw"
              set_values(plot,tmpres)
#
# Add polygon to XY plot. It won't get drawn until plot is drawn.
#
            if(fill_x):
              plot.polygon.append(add_polygon(wks,plot, \
                                              polygon_y[0:ppts2+3], \
                                              polygon_x[0:ppts2+3],gsres))
            else:
              plot.polygon.append(add_polygon(wks,plot, \
                                              polygon_x[0:ppts2+3], \
                                              polygon_y[0:ppts2+3],gsres))
#
# Advance polygon counter.
#
            npoly = npoly + 1
            bpt = -1            # Reinitialize
            ept = -1
          
  return plot

#
# I copied this from Nio.py
#
def _get_integer_version(strversion):
    d = strversion.split('.')
    if len(d) > 2:
       v = int(d[0]) * 10000 + int(d[1]) * 100 + int(d[2][0])
    elif len(d) is 2:
       v = int(d[0]) * 10000 + int(d[1]) * 100
    else:
       v = int(d[0]) * 10000
    return v

IS_NEW_MA = _get_integer_version(numpy.__version__) > 10004

#
# Import other stuff we need.
#
from hlu import *
import hlu, site, types, string, commands, sys, os, math, re

#
# Try to guess the package path for PyNGL. If it can't
# be found, then you can "help" it by setting the 
# environment variable PYNGL_NCARG to the "ncarg"
# directory that's under the package directory.
#

pkgs_pth = get_python_lib(1)

# Try a different one.
if not (os.path.exists(pkgs_pth)):
  pkgs_pth = os.path.join(sys.prefix, 'lib64', 'python'+sys.version[:3],
                        'site-packages')

if (not (os.path.exists(pkgs_pth)) and os.environ.get("PYNGL_NCARG") is None):
  print ('Cannot find the Python packages directory and PYNGL_NCARG is not set.')
  print ('There may be some difficulty finding needed PyNGL system files')
  print ('unless you set the PYNGL_NCARG environment variable.')

first_call_to_open_wks = 0

class Resources:
  pass

class PlotIds:
  pass

def _inputt(a,b):
#
# Promote a and b to numpy arrays that have at least a dimension of 1.
#
  a2 = _promote_scalar(a)
  b2 = _promote_scalar(b)
#
# Determine what kind of array to return.
#
  if _is_numpy(a) or _is_numpy(b):
    import numpy
    return numpy.array(fplib._inputt(a2,b2))
  else:
    return fplib._inputt(a2,b2)

def _int_id(plot_id):
#
#  Convert PlotIds objects to integer plot ids.
#
  if (type(plot_id) == type(1)):
#  Is an integer.
    return plot_id
  elif (type(plot_id) == type([1])):
#  Is a list.
    return plot_id[0]
  elif (isinstance(plot_id,PlotIds)):
#  Is a PlotIds class instance.
    if (type(plot_id.base[0]) != type(1)):
      print ("plot id is not valid")
      return None
    return plot_id.base[0]
  else:
    print ("plot id is not valid")
    return None

def _is_list_or_tuple(arg):
  if ( ((type(arg) == types.ListType) or (type(arg) == types.TupleType)) ):
    return True
  else:
    return False
  
def _is_numpy_array(arg):
  if isinstance(arg,numpy.ndarray):
    return True
  else:
    return False

def _is_numpy_ma(arg):
  if HAS_MA and ma.isMaskedArray(arg):
    return True
  else:
    return False

#
# This function returns True if it encounters a Python scalar.
#
def _is_python_scalar(arg):
  import types
  if (type(arg)==types.IntType or type(arg)==types.LongType or \
      type(arg)==types.FloatType):
    return True
  else:
    return False

# 
# This function returns True if we have a numpy scalar or array.
#
def _is_numpy(arg):
  try:
    import numpy
    if isinstance(arg,numpy.ndarray) or isinstance(arg,numpy.generic):
      return True
    else:
      return False
  except:
    return False

#
# This function returns True if it encounters a numpy scalar.
# A numpy scalar can either be a numpy array with 0 dimensions,
# or a numpy scalar, which is a new thing that didn't exist in
# numeric.
#
def _is_numpy_scalar(arg):
  try:
    import numpy
    if (isinstance(arg,numpy.ndarray)) and (len(arg.shape) == 0):
      return True
#
# Test for numpy scalar.
#
    elif isinstance(arg,numpy.generic):
      return True
    else:
      return False
  except:
    return False

#
# This function returns True if it's a Python scalar or a 
# numpy scalar.
#
def _is_scalar(arg):
  return _is_numpy_scalar(arg) or _is_python_scalar(arg)

def _arg_with_scalar(arg):
#
#  This function is to accommodate scalar arguments for 
#  some functions that take lists, tuples, or NumPy arrays.
#  The input argument is checked to see if it is a number and,
#  if so, it is converted to a single-element list.  Otherwise
#  the original argument is returned.
#
    if (_is_scalar(arg)):
      return [arg]
    else:
      return arg

#
# This function returns a NumPy array and the fill value 
# if arr is a masked array; otherwise it just returns arr and 
# 'None' for the fill value.
#
# Later, I'd like to add recognition of NioVariables, and then
# I can look for the "_FillValue" attribute and use this.
#
def _get_arr_and_fv(arr):
  if _is_numpy_ma(arr):
    if IS_NEW_MA:
      return arr.filled(),arr.fill_value
    else:
      return arr.filled(),arr.fill_value()
  else:
    return arr,None

#
# This function returns a NumPy array and the fill value 
# if arr is a masked array; otherwise it just returns arr and 
# a default missing value.
#
# This is similar to _get_arr_and_fv, except a fill
# value is always returned.
#
def _get_arr_and_force_fv(arr,default_msg=1.e20):
  if _is_numpy_ma(arr):
    if IS_NEW_MA:
      return arr.filled(),arr.fill_value
    else:
      return arr.filled(),arr.fill_value()
  else:
    return arr,default_msg

#
# Determine if a variable has an attribute. If so,
# return that attribute's value. Otherwise, return
# the default value given.
#
def _get_res_value_keep(res, attrname,default):
  if hasattr(res,attrname):
    return(getattr(res,attrname))
  else:
    return(default)

#
# Determine if a variable has a key. If so,
# return that key's value. Otherwise, return
# the default value given.
#
def _get_key_value_keep(res, keyname,default):
  if res.has_key(keyname):
    return(res[keyname])
  else:
    return(default)

#
# If a masked array, then convert to a numpy array. 
# Otherwise just return the value.
#
# This is similar to "_get_arr_and_fv" except
# it doesn't return the fill value.
#
# Hopefully after the release of numpy 1.0.5, we can move
# this code into the C interface.
#
def _convert_from_ma(value):
  if _is_numpy_ma(value):
    return value.filled()
  else:
    return value

def _convert_to_ma(arr,fv):
  if HAS_MA:
    return ma.masked_values(arr,value=fv)
  else:
    return arr

#
# This function checks if a fill value exists, and if it does,
# sets the appropriate missing value PyNGL resource.
#
def _set_msg_val_res(rlist,fv,plot_type):
  type_res_pairs = { "xy_x"     : "caXMissingV", 
                     "xy_y"     : "caYMissingV", 
                     "scalar"   : "sfMissingValueV", 
                     "vector_u" : "vfMissingUValueV",
                     "vector_v" : "vfMissingVValueV"}

  if not plot_type in type_res_pairs.keys():
    return None

  res_to_set = type_res_pairs[plot_type]
  if not fv is None:
    if not rlist.has_key(res_to_set):
      rlist[res_to_set] = fv
    else:
      if rlist[res_to_set] != fv:
        print ("Warning:",res_to_set,"is not equal to actual missing value of data,",fv)

def _ck_for_rangs(dir):
#
#  This function checks that the appropriate data files for
#  the high-res database exist.
#
  file_names = (                                    \
                "gshhs(0).rim", "gshhs(1).rim",     \
                "gshhs(2).rim", "gshhs(3).rim",     \
                "gshhs(4).rim",                     \
                "rangs(0).cat", "rangs(0).cel",     \
                "rangs(1).cat", "rangs(1).cel",     \
                "rangs(2).cat", "rangs(2).cel",     \
                "rangs(3).cat", "rangs(3).cel",     \
                "rangs(4).cat", "rangs(4).cel"      \
               )
  for file in file_names:
    fp_file = dir + "/" + file
    if (not (os.path.exists(fp_file))):
      print ('\nInfo message: The environment variable PYNGL_RANGS has ')
      print ('   been set, but the required high-res database file')
      print ('   "' + fp_file + '"')
      print ('   is not in that directory.\n')
      return None

def _ismissing(arg,mval):
#
#  Returns an array of the same shape as "arg" that
#  has True values in all places where "arg" has 
#  missing values.
#
    arg2 = _convert_from_ma(arg)
    if _is_numpy(arg2):
      pass
    else:
      print ("_ismissing: first argument must be a numpy array or scalar.")
      return None
    return(numpy.equal(arg2,mval))


#
#  _get_fill_value(arr)
#     input: 
#       arr - any Python object
#     output:
#       if arr is a numpy masked array:
#          fill_value is the fill value
#         if arr is not a masked array
#          fill_value returned as None.
#
def _get_fill_value(arr):
#
#  If arr is a numpy masked array, return its fill value.
#
  if _is_numpy_ma(arr):
    if IS_NEW_MA:
      return arr.fill_value
    else:
      return arr.fill_value()
#
#  Not a NumPy masked array.
#
  return None

def _get_values(obj,rlistc):
  rlist = _crt_dict(rlistc)
  values = NhlGetValues(_int_id(obj),rlist)
  del rlist
  return (values)

# 
# Test procedure to see if we're masking a lambert conformal map.
#
def _test_for_mask_lc(rlist,rlist1):
  masklc      = False
  maskoutline = 1

  if rlist.has_key("nglMaskLambertConformal"):
    if rlist["nglMaskLambertConformal"]:
      masklc = True
  if rlist.has_key("nglMaskLambertConformalOutlineOn"):
    maskoutline = rlist["nglMaskLambertConformalOutlineOn"]

  if masklc:
    if rlist1.has_key("mpMinLatF") and rlist1.has_key("mpMaxLatF") and \
       rlist1.has_key("mpMinLonF") and rlist1.has_key("mpMaxLonF"):
      if (rlist1["mpMinLatF"] < 0):
        rlist1["mpLambertParallel1F"] = -0.001
        rlist1["mpLambertParallel2F"] = -89.999
    else:
      print ("map: Warning: one or more of the resources mpMinLatF, mpMaxLatF, mpMinLonF, and mpMaxLonF have not been set.")
      print("No masking of the Lambert Conformal map will take place.")
      masklc = False

#
# Don't draw or advance frame if we're masking a
# lambert conformal map. We'll do that later.
#
  drawit  = True
  frameit = True
  maxit   = True
  if masklc:
    if rlist.has_key("nglDraw"):
      drawit = rlist["nglDraw"]
    if rlist.has_key("nglFrame"):
      frameit = rlist["nglFrame"]
    if rlist.has_key("nglMaximize"):
      maxit = rlist["nglMaximize"]

    _set_spc_res("Draw",False)
    _set_spc_res("Frame",False)
    _set_spc_res("Maximize",False)

  mask_list = {}
  mask_list["MaskLC"]         = masklc
  mask_list["MaskLCDraw"]     = drawit
  mask_list["MaskLCFrame"]    = frameit
  mask_list["MaskLCMaximize"] = maxit
  mask_list["MaskLCOutline"]  = maskoutline
  return mask_list

#***********************************************************************#
# Function : mask_lambert_conformal                                     #
#                 wks: graphic                                          #
#               maplc: graphic                                          #
#           mask_list: dictionary                                       #
#                 res: logical                                          #
#                                                                       #
#   Given a lambert conformal projection, and min/max lat/lon coords,   #
#   this function will mask the map outside the boundaries defined by   #
#   the coords. mask_list has a set of resources that determines the    #
#   behavior of the masked plot.                                        #
#   "res" is an optional list of resources.                             #
#                                                                       #
#   Note, due to the nature of Lambert Conformal plots, lon labels      #
#   cannot be automatically drawn on this type of plot.                 #
#                                                                       #
#   Programming Note: The function expects longitude input data to      #
#   range from -360:180E. If this is not the case, the function         #
#   will alter the min/max to be in that range.                         #
#                                                                       #
#***********************************************************************;
def _mask_lambert_conformal(wks, maplc, mask_list, mlcres):
#
# the mpMin/MaxLat/LonF resources should be set at this point,
# otherwise we're in trouble.
#
  minlat = mlcres["mpMinLatF"]
  maxlat = mlcres["mpMaxLatF"]
  minlon = mlcres["mpMinLonF"]
  maxlon = mlcres["mpMaxLonF"]

#
# Some error checking.
#
  if (maxlat > 0 and minlat < 0):
    print ("mask_lambert_conformal: warning: you are not authorized to specify.")
    print ("  a maxlat that is above the equator and a minlat that is below")
    print ("  the equator. No masking will take place.")
    return maplc

  if (minlon > maxlon):
     print ("mask_lambert_conformal: warning: Minimum longitude is greated than")
     print ("  maximum, subtracting 360 from minumum.")
     minlon = minlon - 360
     print ("minlon = "+minlon+", maxlon = "+maxlon)

  if (minlat > maxlat):
     print ("mask_lambert_conformal: warning: Minimum latitude is greater than")
     print ("  maximum, swapping the two.")
     tmplat = minlat
     minlat = maxlat
     maxlat = tmplat
     print (("minlat = "+minlat+", maxlat = "+maxlat))

  if (minlon >= 180 and maxlon > 180):
     minlon = minlon - 360
     maxlon = maxlon - 360  

  if (minlon < 180 and maxlon >= 180):
     minlon = minlon - 360
     maxlon = maxlon - 360  

#
# Set up list of map resources. The user should have already created a 
# lambert conformal map, but just in case  he/she didn't, it will be done
# here. Some of these resources may have already been set by the user, so
# be sure to use these values.
#
  meridian = minlon + (maxlon - minlon)/2.
  mpres = Resources()
  mpres.mpProjection = "LambertConformal"

  if hasattr(mlcres,"mpLimitMode"):
    need_to_set_limits = False
  else:
    need_to_set_limits = True
    mpres.mpLimitMode  = "LatLon"

  mpres.mpLambertMeridianF = _get_res_value_keep(mlcres,"mpLambertMeridianF",meridian)

  if (minlat < 0):
     mpres.mpLambertParallel2F = _get_res_value_keep(mlcres, \
                                 "mpLambertParallel2F",-89.999  )
  else:
     mpres.mpLambertParallel1F = _get_res_value_keep(mlcres, \
                                 "mpLambertParallel1F", 0.001)
     mpres.mpLambertParallel2F = _get_res_value_keep(mlcres, \
                                 "mpLambertParallel2F",89.999  )

#
# Determine whether we are in the southern or northern hemisphere.
#
  if(minlat >= 0):
    is_nh = True
  else:
    is_nh = False

#
# If the user hasn't already set the limits of the map, then set them
# here. Make sure there's some space around the area we want to mask.
#
  if need_to_set_limits:
    if is_nh:
      mpres.mpMinLatF = max(minlat-0.5,  0)
      mpres.mpMaxLatF = min(maxlat+0.5, 90)
    else:
      mpres.mpMinLatF = max(minlat-0.5,-90)
      mpres.mpMaxLatF = min(maxlat+0.5,  0)
    mpres.mpMinLonF = minlon-0.5
    mpres.mpMaxLonF = maxlon+0.5

#
# These draw order resources are necessary to make sure the map
# outlines, lat/lon lines, and perimeter gets drawn *after* the
# masking polygons are drawn.
#
  mpres.mpOutlineDrawOrder     = _get_res_value_keep(mlcres, \
                                 "mpOutlineDrawOrder","PostDraw")
  mpres.mpGridAndLimbDrawOrder = _get_res_value_keep(mlcres, \
                                 "mpGridAndLimbDrawOrder","PostDraw")
  mpres.mpPerimDrawOrder       = _get_res_value_keep(mlcres, \
                                 "mpPerimDrawOrder","PostDraw")

#
# This section is to get rid of some of the remnants that appear around the
# edges of the plot, even after the masking is done. To accomplish this,
# tickmarks are being turned on, but only the border is being drawn in the
# background color.  Since things like streamlines can *still* leave 
# remnants, even with this extra code, we have put in a hook to allow the
# user to specify the thickness of the border line.
# 
  mpres.pmTickMarkDisplayMode = "Always"
  mpres.tmXBLabelsOn          = False
  mpres.tmXTLabelsOn          = False
  mpres.tmYLLabelsOn          = False
  mpres.tmYRLabelsOn          = False
  mpres.tmYLOn                = False
  mpres.tmYROn                = False
  mpres.tmXBOn                = False
  mpres.tmXTOn                = False
  mpres.tmBorderLineColor     = "background"
  mpres.tmBorderThicknessF    = _get_res_value_keep(mlcres, \
                                "tmBorderThicknessF",2.0)
#
# Now that we've set all these resources, apply them to the map.
#
  set_values(maplc,mpres)

#
# Thus begins the section for creating the two masking polygons.
# The polygons must be drawn in NDC, because trying to draw them in
# lat/lon space is not a good use of time and produces unpredictable
# results.
#
# Get viewport coordinates and calculate NDC positionsd of the
# four corners of the plot.
#
  vpx = get_float(maplc,"vpXF")
  vpy = get_float(maplc,"vpYF")
  vpw = get_float(maplc,"vpWidthF")
  vph = get_float(maplc,"vpHeightF")

  xlft = vpx
  xrgt = vpx + vpw
  ytop = vpy
  ybot = vpy - vph

#
# Calculate NDC coordinates of four corners of area defined by min/max
# lat/lon coordinates.
#
  xmnlnmnlt, ymnlnmnlt = datatondc(maplc, minlon, minlat) 
  xmxlnmnlt, ymxlnmnlt = datatondc(maplc, maxlon, minlat) 
  xmnlnmxlt, ymnlnmxlt = datatondc(maplc, minlon, maxlat) 
  xmxlnmxlt, ymxlnmxlt = datatondc(maplc, maxlon, maxlat) 

#
# Calculate NDC coordinates of southern hemisphere semi-circle.
#
  nscirc     = 100
  scirc_lon  = fspan(maxlon,minlon,nscirc)
  scirc_lat  = numpy.zeros([nscirc],'f')
  scirc_lat[:] = minlat
  scirc_xndc, scirc_yndc = datatondc(maplc,scirc_lon,scirc_lat)

#
# Calculate NDC coordinates of northern hemisphere semi-circle.
#
  nncirc     = 100
  ncirc_lon  = numpy.array(fspan(maxlon,minlon,nncirc))
  ncirc_lat  = numpy.zeros([nncirc],'f')
  ncirc_lat[:]  = maxlat
  ncirc_xndc,ncirc_yndc = datatondc(maplc,ncirc_lon,ncirc_lat)
  
#
# Create two polygons in NDC space (northern and southern hemisphere),
# using all the coordinates we gathered above. The two polygons will be
# set differently depending on whether we're in the northern or 
# southern hemisphere.  Yes, we could do this with one polygon, but it's
# a little cleaner this way, trust me.
#
  if is_nh:
    nxpoly = numpy.zeros(nncirc+7,'f')
    nypoly = numpy.zeros(nncirc+7,'f')
    sxpoly = numpy.zeros(nscirc+5,'f')
    sypoly = numpy.zeros(nscirc+5,'f')
  else:
    nxpoly = numpy.zeros(nncirc+5,'f')
    nypoly = numpy.zeros(nncirc+5,'f')
    sxpoly = numpy.zeros(nscirc+7,'f')
    sypoly = numpy.zeros(nscirc+7,'f')

#
# Define masking polygons for map that is in the northern hemisphere.
#
  if is_nh:
    nxpoly[0]          = xrgt
    nypoly[0]          = ymxlnmnlt
    nxpoly[1]          = xmxlnmnlt
    nypoly[1]          = ymxlnmnlt
    nxpoly[2:nncirc+2] = ncirc_xndc
    nypoly[2:nncirc+2] = ncirc_yndc
    nxpoly[nncirc+2]   = xmnlnmnlt
    nypoly[nncirc+2]   = ymnlnmnlt
    nxpoly[nncirc+3]   = xlft
    nypoly[nncirc+3]   = ymnlnmnlt
    nxpoly[nncirc+4]   = xlft
    nypoly[nncirc+4]   = ytop
    nxpoly[nncirc+5]   = xrgt
    nypoly[nncirc+5]   = ytop
    nxpoly[nncirc+6]   = xrgt
    nypoly[nncirc+6]   = ymxlnmnlt

    sxpoly[0]        = xrgt
    sypoly[0]        = ymxlnmnlt
    sxpoly[1:nscirc+1] = scirc_xndc
    sypoly[1:nscirc+1] = scirc_yndc
    sxpoly[nscirc+1] = xlft
    sypoly[nscirc+1] = ymnlnmnlt
    sxpoly[nscirc+2] = xlft
    sypoly[nscirc+2] = ybot
    sxpoly[nscirc+3] = xrgt
    sypoly[nscirc+3] = ybot
    sxpoly[nscirc+4] = xrgt
    sypoly[nscirc+4] = ymxlnmnlt
  else:
#
# Define masking polygons for plot that is in the southern hemisphere.
#
    nxpoly[0]        = xrgt
    nypoly[0]        = ymxlnmxlt
    nxpoly[1:nncirc+1] = ncirc_xndc
    nypoly[1:nncirc+1] = ncirc_yndc
    nxpoly[nncirc+1] = xlft
    nypoly[nncirc+1] = ymnlnmxlt
    nxpoly[nncirc+2] = xlft
    nypoly[nncirc+2] = ytop
    nxpoly[nncirc+3] = xrgt
    nypoly[nncirc+3] = ytop
    nxpoly[nncirc+4] = xrgt
    nypoly[nncirc+4] = ymxlnmxlt

    sxpoly[0]          = xrgt
    sypoly[0]          = ymxlnmxlt
    sxpoly[1]          = xmxlnmxlt
    sypoly[1]          = ymxlnmxlt
    sxpoly[2:nscirc+2] = scirc_xndc
    sypoly[2:nscirc+2] = scirc_yndc
    sxpoly[nscirc+2]   = xmnlnmxlt
    sypoly[nscirc+2]   = ymnlnmxlt
    sxpoly[nscirc+3]   = xlft
    sypoly[nscirc+3]   = ymnlnmxlt
    sxpoly[nscirc+4]   = xlft
    sypoly[nscirc+4]   = ybot
    sxpoly[nscirc+5]   = xrgt
    sypoly[nscirc+5]   = ybot
    sxpoly[nscirc+6]   = xrgt
    sypoly[nscirc+6]   = ymxlnmxlt

#
# Attach the two polygons (and optionally, the outline polyline) 
# to the map.  Fill the polygons in the background color.
#
  pres             = Resources()
  pres.gsFillColor = "background"

#
# Northern hemisphere polygon
#
  maplc.prim1 = add_polygon(wks,maplc,nxpoly,nypoly,pres,isndc=1)

#
# Southern hemisphere polygon
#
  maplc.prim2 = add_polygon(wks,maplc,sxpoly,sypoly,pres,isndc=1)

#
# Outline the area we are looking at (optional).
#
  if mask_list["MaskLCOutline"]:
    pres.gsLineColor      = "foreground"
    pres.gsLineThicknessF = 3.0
    outline_lon        = [ minlon, maxlon, maxlon, minlon, minlon ]
    outline_lat        = [ minlat, minlat, maxlat, maxlat, minlat ]
    maplc.prim3 = add_polyline(wks,maplc,outline_lon,outline_lat,pres)

  if mask_list["MaskLCMaximize"]:
    maximize_plot(wks,maplc)
  if mask_list["MaskLCDraw"]:
    draw(maplc)
  if mask_list["MaskLCFrame"]:
    frame(wks)

  return(maplc)

#
# Special function to deal with values that may come in as
# a scalar (as defined by the "_is_scalar" function above)
# that need to be converted to something that won't
# register as having 0 dimensions.  We do this by 
# promoting it to a numpy array.
#
# Note: this function promotes the value to a double.
# There's a promote_scalar_int32 if you need an integer.
#
def _promote_scalar(x):
  if _is_scalar(x):
    import numpy
    return numpy.array([x])
  else:
    return x

#
# Similar to _promote_scalar, except it promotes
# value to a numpy integer if it comes in as a Python
# scalar.
#
def _promote_scalar_int32(x):
  if _is_python_scalar(x):
    import numpy
    return numpy.array([x],'int32')
  else:
    return x

def _pynglpath_ncarg():
#
#  Find the root directory that contains the supplemental PyNGL files,
#  like fontcaps, colormaps, and map databases. First see if
#  PYNGL_NCARG is set. If not, then look in the PYTHONPATH
#  directories.
#
  pyngl_dir = os.environ.get("PYNGL_NCARG") 
  if (not pyngl_dir is None) and os.path.exists(pyngl_dir):
    if not os.path.exists(os.path.join(pyngl_dir,"colormaps")):
      print ("pynglpath: supplemental 'colormaps' directory cannot be found. PYNGL_NCARG")
      print ("           may be set incorrectly. You may not need to set it at all.")
    return pyngl_dir

  import sys 
  for path in sys.path: 
    trypath = os.path.join(path,"PyNGL","ncarg") 
    if os.path.exists(trypath): 
      return trypath
    else: 
      trypath = os.path.join(path,"ncarg") 
      if os.path.exists(os.path.join(trypath,"colormaps")): 
        return trypath

  print ("pynglpath: supplemental 'ncarg' directory cannot be found.")
  print ("You may need to set the PYNGL_NCARG environment variable.")
  sys.exit()

def _lst2pobj(lst):
#
#  Converts a list of object ids returned from a plotting function
#  to a PlotIds object with attributes.
#
#  A Python list of PlotIds is in the order:
#
#    base
#    contour
#    vector
#    streamline
#    map
#    xy
#    xydspec
#    text
#    primitive
#    labelbar
#    legend
#    cafield
#    sffield
#    vffield
#
  rval = PlotIds()

  if (lst[0] is None):
    rval.nbase = 0
  else:
    rval.nbase = len(lst[0])
  rval.base    = lst[0]

  if (lst[1] is None):
    rval.ncontour = 0
  else:
    rval.ncontour = len(lst[1])
  rval.contour    = lst[1]

  if (lst[2] is None):
    rval.nvector = 0
  else:
    rval.nvector = len(lst[2])
  rval.vector    = lst[2]

  if (lst[3] is None):
    rval.nstreamline = 0
  else:
    rval.nstreamline = len(lst[3])
  rval.streamline    = lst[3]

  if (lst[4] is None):
    rval.nmap = 0
  else:
    rval.nmap = len(lst[4])
  rval.map    = lst[4]

  if (lst[5] is None):
    rval.nxy = 0
  else:
    rval.nxy = len(lst[5])
  rval.xy     = lst[5]

  if (lst[6] is None):
    rval.nxydspec = 0
  else:
    rval.nxydspec = len(lst[6])
  rval.xydspec    = lst[6]

  if (lst[7] is None):
    rval.ntext = 0
  else:
    rval.ntext = len(lst[7])
  rval.text    = lst[7]

  if (lst[8] is None):
    rval.nprimitive = 0
  else:
    rval.nprimitive = len(lst[8])
  rval.primitive    = lst[8]

  if (lst[9] is None):
    rval.nlabelbar = 0
  else:
    rval.nlabelbar = len(lst[9])
  rval.labelbar    = lst[9]

  if (lst[10] is None):
    rval.nlegend = 0
  else:
    rval.nlegend = len(lst[10])
  rval.legend    = lst[10]

  if (lst[11] is None):
    rval.ncafield = 0
  else:
    rval.ncafield = len(lst[11])
  rval.cafield    = lst[11]

  if (lst[12] is None):
    rval.nsffield = 0
  else:
    rval.nsffield = len(lst[12])
  rval.sffield    = lst[12]

  if (lst[13] is None):
    rval.nvffield = 0
  else:
    rval.nvffield = len(lst[13])
  rval.vffield    = lst[13]

  return rval

def _pobj2lst(pobj):
#  
#  A Python list of PlotIds is in the order:
#
#    base
#    contour
#    vector
#    streamline
#    map
#    xy
#    xydspec
#    text
#    primitive
#    labelbar
#    legend
#    cafield
#    sffield
#    vffield
#
#  Converts the attributes of a PlotId object to a Python list.
#
  if (pobj == 0):
    return [None,None,None,None,None,None,None,None,None,None,None,None,None,None]
  else:
    return [pobj.base,pobj.contour,pobj.vector,pobj.streamline,pobj.map, \
           pobj.xy,pobj.xydspec,pobj.text,pobj.primitive,pobj.labelbar, \
           pobj.legend,pobj.cafield,pobj.sffield,pobj.vffield]

def _pseq2lst(pseq):
#
#  Takes a list of Python plot objects and converts it to
#  a list of lists that will be converted to a list of PlotId
#  structures in the panel argument.
#
  lst = []
  for i in range(len(pseq)):
    lst.append(_pobj2lst(pseq[i]))
  return lst

#
# Set a default missing value and a flag indicating 
# whether a fill value was already present.
#
def _set_default_msg(fv,default_msg=1.e20):
  if fv is None:
    return default_msg,0
  else:
    return fv,1

def _set_spc_res(resource_name,value):
#
#  Change True and False values to 1 and 0 and leave all other
#  values unchaged.
#
  lval = value
  if (value == True):
    lval = 1
  elif (value == False):
    lval = 0

#
#  Set the special resource values.
#
#  These resources must stay in this order!
#  If you add new resources, add them at the
#  end of the list. See also _set_spc_defaults.
#
  if (resource_name   == "Maximize"):
    set_nglRes_i(0, lval) 
  elif (resource_name == "Draw"):
    set_nglRes_i(1, lval) 
  elif (resource_name == "Frame"):
    set_nglRes_i(2, lval) 
  elif (resource_name == "Scale"):
    set_nglRes_i(3, lval) 
  elif (resource_name == "Debug"):
    set_nglRes_i(4, lval) 
  elif (resource_name == "PaperOrientation"):
    if(type(lval) == types.StringType):
      if(string.lower(lval) == "portrait"):
        set_nglRes_i(5, 0) 
      elif(string.lower(lval) == "landscape"):
        set_nglRes_i(5, 6) 
      elif(string.lower(lval) == "auto"):
        set_nglRes_i(5, 3) 
      else:
        print ("_set_spc_res: Unknown value for " + resource_name)
    else:
      set_nglRes_i(5, lval) 
  elif (resource_name == "PaperWidth"):
    set_nglRes_f(6, lval) 
  elif (resource_name == "PaperHeight"):
    set_nglRes_f(7, lval) 
  elif (resource_name == "PaperMargin"):
    set_nglRes_f(8, lval) 
  elif (resource_name == "PanelCenter"):
    set_nglRes_i(9, lval) 
  elif (resource_name == "PanelRowSpec"):
    set_nglRes_i(10, lval) 
  elif (resource_name == "PanelXWhiteSpacePercent"):
    set_nglRes_f(11, lval) 
  elif (resource_name == "PanelYWhiteSpacePercent"):
    set_nglRes_f(12, lval) 
  elif (resource_name == "PanelBoxes"):
    set_nglRes_i(13, lval) 
  elif (resource_name == "PanelLeft"):
    set_nglRes_f(14, lval) 
  elif (resource_name == "PanelRight"):
    set_nglRes_f(15, lval) 
  elif (resource_name == "PanelBottom"):
    set_nglRes_f(16, lval) 
  elif (resource_name == "PanelTop"):
    set_nglRes_f(17, lval) 
  elif (resource_name == "PanelInvsblTop"):
    set_nglRes_f(18, lval) 
  elif (resource_name == "PanelInvsblLeft"):
    set_nglRes_f(19, lval) 
  elif (resource_name == "PanelInvsblRight"):
    set_nglRes_f(20, lval) 
  elif (resource_name == "PanelInvsblBottom"):
    set_nglRes_f(21, lval) 
  elif (resource_name == "PanelSave"):
    set_nglRes_i(22, lval) 
  elif (resource_name == "SpreadColors"):
    set_nglRes_i(23, lval) 
  elif (resource_name == "SpreadColorStart"):
    set_nglRes_i(24, lval) 
  elif (resource_name == "SpreadColorEnd"):
    set_nglRes_i(25, lval) 
  elif (resource_name == "PanelLabelBarOrientation"):
    set_nglRes_i(26, lval) 
  elif (resource_name == "PanelLabelBar" and len(resource_name) == 13):
    set_nglRes_i(27, lval) 
  elif (resource_name == "PanelLabelBarXF"):
    set_nglRes_f(28, lval) 
  elif (resource_name == "PanelLabelBarYF"):
    set_nglRes_f(29, lval) 
  elif (resource_name == "PanelLabelBarLabelFontHeightF"):
    set_nglRes_f(30, lval) 
  elif (resource_name == "PanelLabelBarWidthF"):
    set_nglRes_f(31, lval) 
  elif (resource_name == "PanelLabelBarHeightF"):
    set_nglRes_f(32, lval) 
  elif (resource_name == "PanelLabelBarOrthogonalPosF"):
    set_nglRes_f(33, lval) 
  elif (resource_name == "PanelLabelBarParallelPosF"):
    set_nglRes_f(34, lval) 
  elif (resource_name == "PanelLabelBarPerimOn"):
    set_nglRes_i(35, lval) 
  elif (resource_name == "PanelLabelBarAlignment"):
    set_nglRes_i(36, lval) 
  elif (resource_name == "PanelLabelBarLabelAutoStride"):
    set_nglRes_i(37, lval) 
  elif (resource_name == "PanelFigureStrings" and len(resource_name) == 18):
    set_nglRes_c(38, lval) 
  elif (resource_name == "PanelFigureStringsCount"):
    set_nglRes_i(39, lval) 
  elif (resource_name == "PanelFigureStringsJust"):
    set_nglRes_i(40, lval) 
  elif (resource_name == "PanelFigureStringsOrthogonalPosF"):
    set_nglRes_f(41, lval) 
  elif (resource_name == "PanelFigureStringsParallelPosF"):
    set_nglRes_f(42, lval) 
  elif (resource_name == "PanelFigureStringsPerimOn"):
    set_nglRes_i(43, lval) 
  elif (resource_name == "PanelFigureStringsBackgroundFillColor"):
    set_nglRes_i(44, lval) 
  elif (resource_name == "PanelFigureStringsFontHeightF"):
    set_nglRes_f(45, lval) 
  elif (resource_name == "AppResFileName"):
    set_nglRes_s(46, lval) 
  elif (resource_name == "XAxisType"):
    if(type(lval) == types.StringType):
      if(string.lower(lval) == "irregularaxis"):
        set_nglRes_i(47, 0) 
      elif(string.lower(lval) == "linearaxis"):
        set_nglRes_i(47, 1) 
      elif(string.lower(lval) == "logaxis"):
        set_nglRes_i(47, 2) 
      else:
        print ("_set_spc_res: Unknown value for " + resource_name)
    else:
      set_nglRes_i(47, lval) 
  elif (resource_name == "YAxisType"):
    if(type(lval) == types.StringType):
      if(string.lower(lval) == "irregularaxis"):
        set_nglRes_i(48, 0) 
      elif(string.lower(lval) == "linearaxis"):
        set_nglRes_i(48, 1) 
      elif(string.lower(lval) == "logaxis"):
        set_nglRes_i(48, 2) 
      else:
        print ("_set_spc_res: Unknown value for " + resource_name)
    else:
      set_nglRes_i(48, lval) 
  elif (resource_name == "PointTickmarksOutward"):
    set_nglRes_i(49, lval) 
  elif (resource_name == "XRefLine"):
    set_nglRes_f(50, lval) 
  elif (resource_name == "YRefLine"):
    set_nglRes_f(51, lval) 
  elif (resource_name == "XRefLineThicknessF"):
    set_nglRes_f(52, lval) 
  elif (resource_name == "YRefLineThicknessF"):
    set_nglRes_f(53, lval) 
  elif (resource_name == "XRefLineColor"):
    set_nglRes_i(54, lval) 
  elif (resource_name == "YRefLineColor"):
    set_nglRes_i(55, lval) 
  elif (resource_name == "MaskLambertConformal"):
    set_nglRes_i(56, lval) 
  elif (resource_name == "MaskLambertConformalOutlineOn"):
    set_nglRes_i(57, lval) 

  else:
    print ("_set_spc_res: Unknown special resource ngl" + resource_name)

def _check_res_value(resvalue,strvalue,intvalue):
#
#  Function for checking a resource value that can either be of
#  type string or integer (like color resource values).
#
  if( (type(resvalue) == types.StringType and \
     string.lower(resvalue) == string.lower(strvalue)) or \
     (type(resvalue) == types.IntType and resvalue == intvalue)):
    return(True)
  else:
    return(False)

def _set_tickmark_res(reslist,reslist1):
#
# Set tmEqualizeXYSizes to True so that tickmark lengths and font
# heights are the same size on both axes.
#
  if((reslist.has_key("nglScale") and reslist["nglScale"] > 0) or
     (not (reslist.has_key("nglScale")))):
    reslist1["tmEqualizeXYSizes"] = True

def _set_contour_res(reslist,reslist1):
#
#  Set some contour resources of which we either don't like the NCL
#  defaults, or we want to set something on behalf of the user.
#
  if(reslist.has_key("cnFillOn") and reslist["cnFillOn"] > 0):
    if ( not (reslist.has_key("cnInfoLabelOn"))):
      reslist1["cnInfoLabelOn"] = False
    if ( not (reslist.has_key("pmLabelBarDisplayMode")) and 
         (not (reslist.has_key("lbLabelBarOn")) or 
               reslist.has_key("lbLabelBarOn") and 
                        reslist["lbLabelBarOn"] > 0)):
      reslist1["pmLabelBarDisplayMode"] = "Always"
#
# The ContourPlot object does not recognize the lbLabelBarOn resource
# so we have to remove it after we've used it.
#
  if (reslist1.has_key("lbLabelBarOn")):
    del reslist1["lbLabelBarOn"]
#
# It used to be that nglSpreadColors was set to True by default.
#
# With PyNGL 1.5.0, however, this resource is somewhat obsolete,
# as cnFillPalette should now be used. nglSpreadColors will only
# be set back to True if nglSpreadColorStart set explicitly to
# something other than 2 and/or nglSpreadColorEnd is set explicitly
# to something other than -1.
#
  if((reslist.has_key("nglSpreadColorStart") and
      reslist["nglSpreadColorStart"] != 2) or 
     (reslist.has_key("nglSpreadColorEnd") and
      reslist["nglSpreadColorEnd"] != -1)):
      lval = 1
      set_nglRes_i(23, lval) 
#
#  Check for "plural" resources that only take effect if their
#  corresponding "Mono" resource is set to False, and set the
#  Mono resource on behalf of the user.
#
  if(reslist.has_key("cnLineDashPatterns")):
    if ( not (reslist.has_key("cnMonoLineDashPattern"))):
      reslist1["cnMonoLineDashPattern"] = False
  if(reslist.has_key("cnLineColors")):
    if (not (reslist.has_key("cnMonoLineColor"))):
      reslist1["cnMonoLineColor"] = False
  if(reslist.has_key("cnLineThicknesss")):
    if (not (reslist.has_key("cnMonoLineThickness"))):
      reslist1["cnMonoLineThickness"] = False
  if(reslist.has_key("cnLevelFlags")):
    if (not (reslist.has_key("cnMonoLevelFlag"))):
      reslist1["cnMonoLevelFlag"] = False
  if(reslist.has_key("cnFillPatterns")):
    if (not (reslist.has_key("cnMonoFillPattern"))):
      reslist1["cnMonoFillPattern"] = False
  if(reslist.has_key("cnFillScales")):
    if (not (reslist.has_key("cnMonoFillScale"))):
      reslist1["cnMonoFillScale"] = False
  if(reslist.has_key("cnLineLabelFontColors")):
    if (not (reslist.has_key("cnMonoLineLabelFontColor"))):
      reslist1["cnMonoLineLabelFontColor"] = False
#
# Set some tickmark resources.
#
  _set_tickmark_res(reslist,reslist1)

def _set_vector_res(reslist,reslist1):
#
#  Set some vector resources of which we either don't like the NCL
#  defaults, or we want to set something on behalf of the user.
#
# Vectors can be colored one of two ways, either with colored line
# vectors or filled colored vectors, or wind barbs.  Any one of these
# would warrant a labelbar.
#
# Don't bother setting the the vcMonoLineArrowColor,
# vcMonoFillArrowEdgeColor, vcMonoFillArrowFillColor, or 
# vcMonoWindBarbColor resources to False if vcLevelColors is
# set, because it all depends on if vcGlyphStyle is set a certain way.
# Put the responsibility on the user
#
  if( (reslist.has_key("vcMonoLineArrowColor") and
       (_check_res_value(reslist["vcMonoLineArrowColor"],"False",0) or
       not reslist["vcMonoLineArrowColor"])) or
      (reslist.has_key("vcMonoFillArrowFillColor") and
       (_check_res_value(reslist["vcMonoFillArrowFillColor"],"False",0) or
       not reslist["vcMonoFillArrowFillColor"])) or
      (reslist.has_key("vcMonoFillArrowEdgeColor") and
       (_check_res_value(reslist["vcMonoFillArrowEdgeColor"],"False",0) or
       not reslist["vcMonoFillArrowEdgeColor"])) or
      (reslist.has_key("vcMonoWindBarbColor") and
       (_check_res_value(reslist["vcMonoWindBarbColor"],"False",0) or
        not reslist["vcMonoWindBarbColor"]))):
    if ( not (reslist.has_key("pmLabelBarDisplayMode")) and 
         (not (reslist.has_key("lbLabelBarOn")) or 
               reslist.has_key("lbLabelbarOn") and 
                        reslist["lbLabelBarOn"] > 0)):
      reslist1["pmLabelBarDisplayMode"] = "Always"
#
# The VectorPlot object does not recognize the lbLabelBarOn resource
# so we have to remove it after we've used it.
#
  if (reslist1.has_key("lbLabelBarOn")):
    del reslist1["lbLabelBarOn"]
#
# It used to be that nglSpreadColors was set to True by default.
#
# With PyNGL 1.5.0, however, this resource is somewhat obsolete,
# as vcLevelPalette should now be used. nglSpreadColors will only
# be set back to True if nglSpreadColorStart set explicitly to
# something other than 2 and/or nglSpreadColorEnd is set explicitly
# to something other than -1.
#
  if((reslist.has_key("nglSpreadColorStart") and
      reslist["nglSpreadColorStart"] != 2) or 
     (reslist.has_key("nglSpreadColorEnd") and
      reslist["nglSpreadColorEnd"] != -1)):
      lval = 1
      set_nglRes_i(23, lval) 
#
# Set some tickmark resources.
#
  _set_tickmark_res(reslist,reslist1)

def _set_streamline_res(reslist,reslist1):
#
#  Set some streamline resources of which we either don't like the NCL
#  defaults, or we want to set something on behalf of the user.
#
# stMonoLineColor is different, because there is no stLineColors resource.
# Instead, there's an stLevelColors resource, and this is the one we
# need to set here.
#
  if(reslist.has_key("stLevelColors")):
    if (not (reslist.has_key("stMonoLineColor"))):
      reslist1["stMonoLineColor"] = False

  if( reslist.has_key("stMonoLineColor") and
      (reslist["stMonoLineColor"]  or reslist["stMonoLineColor"] == 0)):
    if ( not (reslist.has_key("pmLabelBarDisplayMode")) and 
         (not (reslist.has_key("lbLabelBarOn")) or 
               reslist.has_key("lbLabelbarOn") and 
                        reslist["lbLabelBarOn"] > 0)):
      reslist1["pmLabelBarDisplayMode"] = "Always"

#
# Set some tickmark resources.
#
  _set_tickmark_res(reslist,reslist1)

def _set_map_res(reslist,reslist1):
#
# Turn on map tickmarks.
#
  if ( not (reslist.has_key("pmTickMarkDisplayMode"))):
    reslist1["pmTickMarkDisplayMode"] = "Always"
  if ( not (reslist.has_key("pmTitleDisplayMode"))):
    reslist1["pmTitleDisplayMode"] = "Conditional"
  if(reslist.has_key("mpFillPatterns")):
    if (not (reslist.has_key("mpMonoFillPattern"))):
      reslist1["mpMonoFillPattern"] = False
  if(reslist.has_key("mpFillScales")):
    if (not (reslist.has_key("mpMonoFillScale"))):
      reslist1["mpMonoFillScale"] = False
  
def _set_labelbar_res(reslist,reslist1,part_of_plot):
#
# Set some labelbar resources of which we don't like the NCL
# defaults.
# 
  if ( not (reslist.has_key("lbPerimOn"))):
    reslist1["lbPerimOn"] = False
  if ( not (reslist.has_key("lbLabelAutoStride"))):
    reslist1["lbLabelAutoStride"] = True
  if(reslist.has_key("lbLabelFontHeightF")):
    if ( not (reslist.has_key("lbAutoManage"))):
      reslist1["lbAutoManage"] = False
  if(reslist.has_key("lbFillScales")):
    if (not (reslist.has_key("lbMonoFillScale"))):
      reslist1["lbMonoFillScale"] = False
  if(part_of_plot):
      if(reslist.has_key("lbOrientation")):
        if ( not (reslist.has_key("pmLabelBarSide"))):
          if(_check_res_value(reslist["lbOrientation"],"Horizontal",0)):
            reslist1["pmLabelBarSide"] = "Bottom"
          if(_check_res_value(reslist["lbOrientation"],"Vertical",1)):
            reslist1["pmLabelBarSide"] = "Right"

def _set_legend_res(reslist,reslist1):
#
# Set some legend resources of which we don't like the NCL
# defaults.  These are mostly the Mono resources which we default to
# False if the corresponding parallel version of this resource is set.
#
# We may not be doing anything with these yet, since
# we don't have a legend function yet.
# 
  if ( not (reslist.has_key("lgPerimOn"))):
    reslist1["lgPerimOn"] = False
  if ( not (reslist.has_key("lgLabelAutoStride"))):
    reslist1["lgLabelAutoStride"] = True
  if(reslist.has_key("lgLabelFontHeightF")):
    if ( not (reslist.has_key("lgAutoManage"))):
      reslist1["lgAutoManage"] = False
  if(reslist.has_key("lgItemTypes")):
    if (not (reslist.has_key("lgMonoItemType"))):
      reslist1["lgMonoItemType"] = False
  if(reslist.has_key("lgLineDashSegLens")):
    if (not (reslist.has_key("lgMonoLineDashSegLen"))):
      reslist1["lgMonoLineDashSegLen"] = False
  if(reslist.has_key("lgLineThicknesses")):
    if (not (reslist.has_key("lgMonoLineThickness"))):
      reslist1["lgMonoLineThickness"] = False
  if(reslist.has_key("lgMarkerThicknesses")):
    if (not (reslist.has_key("lgMonoMarkerThickness"))):
      reslist1["lgMonoMarkerThickness"] = False
  if(reslist.has_key("lgLineLabelFontHeights")):
    if (not (reslist.has_key("lgMonoLineLabelFontHeight"))):
      reslist1["lgMonoLineLabelFontHeight"] = False
  if(reslist.has_key("lgMarkerSizes")):
    if (not (reslist.has_key("lgMonoMarkerSize"))):
      reslist1["lgMonoMarkerSize"] = False

# Converts resource class to a dictionary.
def _crt_dict(resource_i):
  dic = {}
  if (resource_i is None):
    return(dic)
  for t in dir(resource_i):
    if (t[0:2] != '__'):        # skip any Python-supplied attributes.
      dic[t] = getattr(resource_i,t)
  return(dic)

def _set_spc_defaults(type):
#
#  Type = 1 sets the ngl special resources for plotting functions.
#  Type = 0 sets the ngl special resources for text/poly resources
#
#  These resources must stay in this order. 
#   See also _set_spc_res.
#
  if (type == 1):
    set_nglRes_i(0, 1)      # nglMaximize
    set_nglRes_i(1, 1)      # nglDraw
    set_nglRes_i(2, 1)      # nglFrame
  elif (type == 0):
    set_nglRes_i(0, 0)      # nglMaximize
    set_nglRes_i(1, 1)      # nglDraw
    set_nglRes_i(2, 0)      # nglFrame
#
  set_nglRes_i( 3, 1)       # nglScale
  set_nglRes_i( 4, 0)       # nglDebug
  set_nglRes_i( 5, -1)      # nglPaperOrientation
  set_nglRes_f( 6, 8.5)     # nglPaperWidth
  set_nglRes_f( 7, 11.)     # nglPaperHeight
  set_nglRes_f( 8, 0.5)     # nglPaperMargin
  set_nglRes_i( 9, 1)       # nglPanelCenter
  set_nglRes_i(10, 0)       # nglPanelRowSpec
  set_nglRes_f(11, 1.)      # nglPanelXWhiteSpacePercent
  set_nglRes_f(12, 1.)      # nglPanelYWhiteSpacePercent
  set_nglRes_i(13, 0)       # nglPanelBoxes
  set_nglRes_f(14, 0.)      # nglPanelLeft
  set_nglRes_f(15, 1.)      # nglPanelRight
  set_nglRes_f(16, 0.)      # nglPanelBottom
  set_nglRes_f(17, 1.)      # nglPanelTop
  set_nglRes_f(18, -999.)   # nglPanelInvsblTop
  set_nglRes_f(19, -999.)   # nglPanelInvsblLeft
  set_nglRes_f(20, -999.)   # nglPanelInvsblRight
  set_nglRes_f(21, -999.)   # nglPanelInvsblBottom
  set_nglRes_i(22, 0)       # nglPanelSave
  set_nglRes_i(23, 0)       # nglSpreadColors
  set_nglRes_i(24, 2)       # nglSpreadColorStart
  set_nglRes_i(25, -1)      # nglSpreadColorEnd
  set_nglRes_i(26, 0)       # nglPanelLabelBarOrientation
  set_nglRes_i(27, 0)       # nglPanelLabelBar
  set_nglRes_f(28, -999.)   # nglPanelLabelBarXF
  set_nglRes_f(29, -999.)   # nglPanelLabelBarYF
  set_nglRes_f(30, -999.)   # nglPanelLabelBarLabelFontHeightF
  set_nglRes_f(31, -999.)   # nglPanelLabelBarWidthF
  set_nglRes_f(32, -999.)   # nglPanelLabelBarHeightF
  set_nglRes_f(33, -999.)   # nglPanelLabelBarOrthogonalPosF
  set_nglRes_f(34, -999.)   # nglPanelLabelBarParallelPosF
  set_nglRes_i(35, 0)       # nglPanelLabelBarPerimOn
  set_nglRes_i(36, 1)       # nglPanelLabelBarAlignment
  set_nglRes_i(37, 1)       # nglPanelLabelBarLabelAutoStride
  set_nglRes_c(38, [])      # nglPanelFigureStrings
  set_nglRes_i(39, 0)       # nglPanelFigureStringsCount
  set_nglRes_i(40, 8)       # nglPanelFigureStringsJust
  set_nglRes_f(41, -999.)   # nglPanelFigureStringsOrthogonalPosF
  set_nglRes_f(42, -999.)   # nglPanelFigureStringsParallelPosF
  set_nglRes_i(43, 1)       # nglPanelFigureStringsPerimOn
  set_nglRes_i(44, 0)       # nglPanelFigureStringsBackgroundFillColor
  set_nglRes_f(45, -999.)   # nglPanelFigureStringsFontHeightF
  set_nglRes_s(46, "")      # nglAppResFileName
  set_nglRes_i(47, 0)       # nglXAxisType - default to irregular
  set_nglRes_i(48, 0)       # nglYAxisType - default to irregular
  set_nglRes_i(49, 0)       # nglPointTickmarksOutward
  set_nglRes_f(50, -999.)   # nglXRefLine
  set_nglRes_f(51, -999.)   # nglYRefLine
  set_nglRes_f(52, 1.)      # nglXRefLineThicknessF
  set_nglRes_f(53, 1.)      # nglYRefLineThicknessF
  set_nglRes_i(54, 1)       # nglXRefLineColor
  set_nglRes_i(55, 1)       # nglYRefLineColor
  set_nglRes_i(56, 0)       # nglMaskLambertConformal
  set_nglRes_i(57, 1)       # nglMaskLambertConformalOutlineOn

################################################################
#
#  Skewt support functions.
#
################################################################

def _skewty(pres):    # y-coord given pressure (mb)
  return(132.182-44.061*numpy.lib.scimath.log10(pres))

def _skewtx(temp,y):  # x-coord given temperature (c)
  return (0.54*temp+0.90692*y)

def _dptlclskewt(p, tc, tdc):
  return c_dptlclskewt(p, tc, tdc)

def _dtmrskewt(w, p):
  return c_dtmrskewt(w, p)

def _dtdaskewt(o,p):
  return c_dtdaskewt(o, p)

def _dsatlftskewt(thw,p):
  return c_dsatlftskewt(thw, p)

def _dshowalskewt(p,t,td,nlvls):
  return c_dshowalskewt(p,t,td,nlvls)

def _dpwskewt(td,p,n):
  return c_dpwskewt(td,p,n)

def _get_skewt_msg(varname,res_intrnl,res_public,opt,ma_fv):
#
# Check if user has explicitly set a skewt missing value resource,
# or whether there's one from a masked array. The masked array one
# takes precedence, because this is the value that is used to fill
# in all the missing value locations.
#
  if hasattr(opt,res_intrnl):
    if (not ma_fv is None) and ma_fv != getattr(opt,res_intrnl):
      print ("_get_skewt_msg:",res_public,"is being set to a different value")
      print ("           than the fill_value in the",varname,"masked array.")
      print ("           The masked array fill_value will take precedence.")
      msg = ma_fv
    else:
      msg = getattr(opt,res_intrnl)
  elif not ma_fv is None:
    msg = ma_fv
  else:
    msg = -999.
  return msg

#
#  A dictionary for converting from new skew-T resource names
#  to the originals.
#
RscConv = {  \
           "sktColoredBandsOn":"sktDrawColAreaFill",                 \
           "sktDewPointLineColor":"sktcolDewPt",                     \
           "sktDewPointMissingV":"sktTDCmissingV",                   \
           "sktDryAdiabaticLinesOn":"sktDrawDryAdiabat",             \
           "sktGeopotentialLabelColor":"sktcolZLabel",               \
           "sktGeopotentialLabelsOn":"sktPrintZ",                    \
           "sktGeopotentialMissingV":"sktZmissingV",                 \
           "sktGeopotentialWindBarbColor":"sktcolWindZ",             \
           "sktHeightScaleOn":"sktDrawHeightScale",                  \
           "sktHeightWindBarbColor":"sktcolWindH",                   \
           "sktHeightWindBarbPositionMissingV":"sktHmissingV",       \
           "sktHeightWindBarbPositions":"sktHeight",                 \
           "sktHeightWindBarbDirections":"sktHdir",                  \
           "sktHeightWindBarbSpeeds":"sktHspd",                      \
           "sktHeightWindBarbsOn":"sktPlotWindH",                    \
           "sktIsobarLinesOn":"sktDrawIsobar",                       \
           "sktIsothermalLinesOn":"sktDrawIsotherm",                 \
           "sktMixingRatioLinesOn":"sktDrawMixRatio",                \
           "sktMoistAdiabaticLinesOn":"sktDrawMoistAdiabat",         \
           "sktParcelPathLineColor":"sktcolPpath",                   \
           "sktParcelPathLineOn":"sktCape",                          \
           "sktParcelPathStartCoordinate":"sktParcel",               \
           "sktPressureMissingV":"sktPmissingV",                     \
           "sktPressureWindBarbColor":"sktcolWindP",                 \
           "sktPressureWindBarbStride":"sktWthin",                   \
           "sktPressureWindBarbsOn":"sktPlotWindP",                  \
           "sktStdAtmosphereLineOn":"sktDrawStandardAtm",            \
           "sktStdAtmosphereLineThicknessF":"sktDrawStandardAtmThk", \
           "sktTemperatureMissingV":"sktTCmissingV",                 \
           "sktTemperatureSoundingLineColor":"sktcolTemperature",    \
           "sktThermoInfoLabelColor":"sktcolThermoInfo",             \
           "sktThermoInfoLabelOn":"sktThermoInfo",                   \
           "sktUseMultipleLineColors":"sktDrawColLine",              \
           "sktWindBarbLineOn":"sktDrawWind",                        \
           "sktWindDirectionMissingV":"sktWDIRmissingV",             \
           "sktWindSpeedMissingV":"sktWSPDmissingV",                 \
          }

def _poly(wks,plot,x,y,ptype,is_ndc,rlistc=None):
# Get NumPy array from masked arrays, if necessary.
  x2,fill_value_x = _get_arr_and_fv(x)
  y2,fill_value_y = _get_arr_and_fv(y)

  _set_spc_defaults(0)
  rlist1 = {}
  if (not rlistc is None) and rlistc != False:
    rlist = _crt_dict(rlistc)  
    for key in rlist.keys():
      rlist[key] = _convert_from_ma(rlist[key])
      if (key[0:3] == "ngl"):
        _set_spc_res(key[3:],rlist[key])      
      else:
        rlist1[key] = rlist[key]

# Set flags indicating whether missing values present.
  fill_value_x,ismx = _set_default_msg(fill_value_x)
  fill_value_y,ismy = _set_default_msg(fill_value_y)

  ply = poly_wrap(wks,_pobj2lst(plot),_arg_with_scalar(x2),_arg_with_scalar(y2),
                  "double","double",len(_arg_with_scalar(x2)),ismx,ismy, \
                  fill_value_x,fill_value_y,ptype,rlist1,pvoid())
  del rlist1
  if (not rlistc is None) and rlistc != False:
    del rlist
  return None

def _add_poly(wks,plot,x,y,ptype,rlistc=None,isndc=0):
# Get NumPy array from masked arrays, if necessary.
  x2,fill_value_x = _get_arr_and_fv(x)
  y2,fill_value_y = _get_arr_and_fv(y)

  rlist = _crt_dict(rlistc)  
  rlist1 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist1[key] = rlist[key]

# Set flags indicating whether missing values present.
  fill_value_x,ismx = _set_default_msg(fill_value_x)
  fill_value_y,ismy = _set_default_msg(fill_value_y)

  ply = add_poly_wrap(wks,_pobj2lst(plot), _arg_with_scalar(x2),  \
            _arg_with_scalar(y2), "double","double", len(_arg_with_scalar(x2)),
            ismx,ismy,isndc,fill_value_x,fill_value_y,ptype,rlist1,pvoid())

  del rlist
  del rlist1
  return(_lst2pobj(ply))

def get_workspace_id():
  """
Returns a reference to the current Workspace object.
wid = Ngl.get_workspace_id()
  """
  return NhlGetWorkspaceObjectId()

#
#  Globals for random number generator for generat_2d_array
#
dfran_iseq = 0
dfran_rseq = [.749, .973, .666, .804, .081, .483, .919, .903,   \
              .951, .960, .039, .269, .270, .756, .222, .478,   \
              .621, .063, .550, .798, .027, .569, .149, .697,   \
              .451, .738, .508, .041, .266, .249, .019, .191,   \
              .266, .625, .492, .940, .508, .406, .972, .311,   \
              .757, .378, .299, .536, .619, .844, .342, .295,   \
              .447, .499, .688, .193, .225, .520, .954, .749,   \
              .997, .693, .217, .273, .961, .948, .902, .104,   \
              .495, .257, .524, .100, .492, .347, .981, .019,   \
              .225, .806, .678, .710, .235, .600, .994, .758,   \
              .682, .373, .009, .469, .203, .730, .588, .603,   \
              .213, .495, .884, .032, .185, .127, .010, .180,   \
              .689, .354, .372, .429                            \
             ]

#
#  Random number generator for generate_2d_array.
#
def _dfran():
  global dfran_iseq
  global dfran_rseq
  dfran_iseq = dfran_iseq % 100
  r = dfran_rseq[dfran_iseq]
  dfran_iseq = dfran_iseq + 1
  return r

################################################################
#  
#  Public functions in alphabetical order.
#  
################################################################


################################################################

def add_annotation(plot_id1,plot_id2,rlistc=None):
  """
Adds an annotation to a given plot and returns an integer that
represents the annotation added.
anno = Ngl.add_annotation(base_id, annotation_id, res=None)
base_id -- The PlotId of the plot of which you want to add the annotation.
annotation_id -- The PlotId of the annotation you want to attach to
                 the plot.
res -- An optional instance of the Resources class having annotation
      resources as attributes.
  """

  rlist = _crt_dict(rlistc)
  anno = NhlAddAnnotation(_int_id(plot_id1),_int_id(plot_id2))
  values = NhlSetValues(_int_id(anno),rlist)
  del rlist
  return anno

################################################################

#
# Add a cyclic point in the x dimension (longitude dimension) to
# a 2D array. If there is also a 1D lon coordinate array, add 360 to 
# create the cyclic point.
#
def add_cyclic(data,lon_coord=None):
  """
Adds cyclic points to an array and returns a NumPy array of the
same type as data with one more element in the rightmost dimension.
datap = Ngl.add_cyclic(data, longitude=None)
data -- A two-dimensional array to which you want to add a cyclic
        point in the rightmost dimension.
longitude -- An optional one-dimensional array, representing
             longitude values, that you want to add a cyclic
             point to.
  """
#
# Check input data to make sure it is 2D.
#
  dims = data.shape
  if (len(dims) != 2):
    print ("add_cyclic: input must be a 2-dimensional array.")
    sys.exit()

  ny  = dims[0]
  nx  = dims[1]
  nx1 = nx + 1

#
# Test longitude array, if it exists.
#
# In numpy 1.4.1 and later, you can't test a numpy masked
# array for being equal to None.
#
  if(_is_numpy_ma(lon_coord) or \
     (not _is_numpy_ma(lon_coord) and (not lon_coord is None))):
    lon_coord_dims = lon_coord.shape
    lon_coord_rank = len(lon_coord_dims)
#
# Longitude coordindate array must be 1D.
#
    if (lon_coord_rank != 1):
      print ("add_cyclic: longitude coordinate array must be a 1-dimensional.")
      sys.exit()
#
# Check dimension size against data array.
#
    nlon = lon_coord_dims[0]
    if (nlon != nx):
      print ("add_cyclic: longitude coordinate array must be the same length as the rightmost dimension of the data array.")
      sys.exit()

#
# Create the new data array with one extra value in the X direction.
#
  if _is_numpy_ma(data):
    newdata         = ma.zeros((ny,nx1),data.dtype.char)
    if IS_NEW_MA:
      newdata.set_fill_value(data.fill_value)
    else:
      newdata.set_fill_value(data.fill_value())
  else:
    newdata         = numpy.zeros((ny,nx1),data.dtype.char)
  newdata[:,0:nx] = data
  newdata[:,nx]   = data[:,0]

#
# Add 360 to the longitude value in order to make it cyclic.
#
# In numpy 1.4.1 and later, you can't test a numpy masked
# array for being equal to None.
#
  if(_is_numpy_ma(lon_coord) or \
     (not _is_numpy_ma(lon_coord) and (not lon_coord is None))):
    newloncoord       = numpy.zeros(nx1,lon_coord.dtype.char)
    newloncoord[0:nx] = lon_coord
    newloncoord[nx]   = lon_coord[0] + 360

    return newdata,newloncoord
  else:
    return newdata

################################################################

#
# In order to add new axes limits for the case where sfXArray and/or
# sfYArray are being set to arrays, you need to create a new data array
# that has one extra element on the axis side you want to add the new
# limit value(s) for.
#
# This function checks which axes limits are to be changed, and creates
# new data and coord arrays with the extra element(s) added. The data
# array must have a missing value associated with it.

def add_new_coord_limits(data,fillvalue=None,xcoord=None,ycoord=None, \
                         xmin=None,xmax=None,ymin=None,ymax=None):
  """
Changes the minimum and/or maximum limits of X and/or Y coordinate arrays
and creates a new data array and new coordinate array(s).
new_data,new_xcoord,new_ycoord = Ngl.add_new_coord_limits(data,fillvalue,
                                      xcoord=None,ycoord=None, 
                                      xmin=None,xmax=None,ymin=None,ymax=None)
data -- A two-dimensional array that will be used to create a new
        data array to which you want to add new minimum and/or maximum
        values to the X and/or Y coordinate arrays.
fillvalue = The value to use for missing values in data.
xcoord,ycoord -- Optional coordinate arrays for the X or Y axes. At
                 least one of these must be set.
xmin,xmax -- Optional new minimum or maximum values for the X coordinate
             array. At least one of these must be set if xcoord is set.
ymin,ymax -- Optional new minimum or maximum values for the Y coordinate
             array. At least one of these must be set if ycoord is set.
  """

  if (len(data.shape) != 2):
    print ("add_new_coord_limits - array must be 2D")
    sys.exit()

  data_is_masked = False
  if fillvalue is None:
    if _is_numpy_ma(data):
      data2,fillvalue = _get_arr_and_fv(data)
      data_is_masked = True
    else:
      print ("add_new_coord_limits - fillvalue must be set if you don't have a masked array")
      sys.exit()
  else:
    data2 = data

#
# Check for whether one or both elements of X and/or Y arrays are to
# be added.
#
  if xcoord is None and ycoord is None:
    print ("add_new_coord_limits: At least one of xcoord and/or ycoord must be set to an array")
    sys.exit()

  nx       = data2.shape[1]
  ny       = data2.shape[0]
  ix_start = 0
  iy_start = 0
  ix_end   = nx
  iy_end   = ny

  new_nx = nx
  new_ny = ny

  if not xcoord is None:
    if (len(xcoord.shape) != 1):
      print ("add_new_coord_limits - X coord array must be 1D")
      sys.exit()

    if xmin is None and xmax is None:
      print ("add_new_coord_limits: If xcoord is specified, then one of xmin, xmax must be specified")
      sys.exit()
    if xcoord.shape[0] != nx:
      print ("add_new_coord_limits: xcoord must be the same length as the second dimension of data")
      sys.exit()
#
# Test if one or two elements are to be added.
#
    if not xmin is None:
      ix_start = 1
      new_nx   = new_nx + 1
    ix_end = nx + ix_start

    if not xmax is None:
      new_nx   = new_nx + 1

  if not ycoord is None:
    if (len(ycoord.shape) != 1):
      print ("add_new_coord_limits - Y coord array must be 1D")
      sys.exit()

    if ymin is None and ymax is None:
      print ("add_new_coord_limits: If ycoord is specified, then one of ymin, ymax must be specified")
      sys.exit()

    if ycoord.shape[0] != ny:
      print ("add_new_coord_limits: ycoord must be the same length as the first dimension of data")
      sys.exit()
#
# Test if one or two elements are to be added.
#
    if not ymin is None:
      iy_start = 1
      new_ny   = new_ny + 1

    iy_end = ny + iy_start

    if not ymax is None:
      new_ny = new_ny + 1

#
# Create new arrays.
#
  if data_is_masked:
    if HAS_MA:
      new_data     = ma.zeros((new_ny,new_nx),data2.dtype.char)
    if IS_NEW_MA:
      new_data.set_fill_value(data.fill_value)
    else:
      new_data.set_fill_value(data.fill_value())
  else:
    new_data     = numpy.zeros((new_ny,new_nx),data2.dtype.char)
  if not xcoord is None:
    new_xcoord = numpy.zeros(new_nx,xcoord.dtype.char)
  if not ycoord is None:
    new_ycoord = numpy.zeros(new_ny,ycoord.dtype.char)
# 
# Fill the new data array with the original values, and missing
# values everywhere else.
#
  new_data[:,:] = fillvalue
  new_data[iy_start:iy_end,ix_start:ix_end] = data2[:,:]

#
# Fill in the new coordinate arrays.
#
  if not xcoord is None:
    new_xcoord[ix_start:ix_end] = xcoord
    if not xmin is None:
       new_xcoord[0] = xmin
    if not xmax is None:
      new_xcoord[ix_end] = xmax

  if not ycoord is None:
    new_ycoord[iy_start:iy_end] = ycoord
    if not ymin is None:
       new_ycoord[0] = ymin
    if not ymax is None:
      new_ycoord[iy_end] = ymax

  if (not xcoord is None) and (not ycoord is None):
    return new_data, new_xcoord, new_ycoord
  elif not xcoord is None:
    return new_data, new_xcoord
  else:
    return new_data, new_ycoord

#
# Add -90 and 90 to the latitude dimension to give it "nice"
# values, and then make sure the data is missing in these new 
# locations.  By default, it is assumed the latitude dimemsion
# is the leftmost dimension. If this is not the case, then
# axis must be set to "x".
#
def add_lat_90(data,lat_coord=None,axis="y"):
  """
Adds -90 and 90 points to a latitude coordinate dimension of a 2D
array and returns a NumPy array of the same type as data with two more
elements in the given dimension (leftmost by default). These new 
locations will contain all missing values. A fill_value will be 
added, if none exists, and set to 1e20.
datap = Ngl.add_lat_90(data, latitude=None, axis="y")
data -- A two-dimensional array to which you want to add -90/90
        latitude points to the given dimension (Y axis by default,
        or axis="x")
latitude -- An optional one-dimensional array, representing
            latitude values, that you want to add the points
            to.
  """
#
# Check input data to make sure it is 2D.
#
  dims = data.shape
  if (len(dims) != 2):
    print ("add_lat_90: input must be a 2-dimensional array.")
    sys.exit()

  if(axis is None):
    axis = "y"
  else:
    saxis = string.lower(axis)
    if (saxis != "x" and saxis != "y"):
      print ("add_lat_90: 'axis' must be set to 'x' or 'y'")
      sys.exit()

  ny  = dims[0]
  nx  = dims[1]

  if(saxis == "y"):
    ny1  = ny + 1
    ny2  = ny + 2
  else:
    nx1  = nx + 1
    nx2  = nx + 2
#
# Test latitude array, if it exists.
#
# In numpy 1.4.1 and later, you can't test a numpy masked
# array for being equal to None.
#
  if(_is_numpy_ma(lat_coord) or \
     (not _is_numpy_ma(lat_coord) and (not lat_coord is None))):
    lat_coord_dims = lat_coord.shape
    lat_coord_rank = len(lat_coord_dims)
#
# Latitude coordindate array must be 1D.
#
    if (lat_coord_rank != 1):
      print ("add_lat_90: latitude coordinate array must be a 1-dimensional.")
      sys.exit()
#
# Check dimension size against data array.
#
    nlat = lat_coord_dims[0]
    if ((saxis == "y" and nlat != ny) or \
        (saxis == "x" and nlat != nx)):
      print ("add_lat_90: latitude coordinate array must be the same length as the",axis,"dimension of the data array.")
      sys.exit()

    nlat1 = nlat+1
    nlat2 = nlat+2

#
# Create the new data array with two extra values in the Y direction.
#
  if(saxis == "y"):
    newdata = ma.zeros((ny2,nx),data.dtype.char)
  else:
    newdata = ma.zeros((ny,nx2),data.dtype.char)

  fill_value = _get_fill_value(data)
  if(fill_value is None):
    newdata.set_fill_value(1.e20)
  else:
    newdata.set_fill_value(fill_value)

  if(saxis == "y"):
    newdata[1:ny1,:] = data
    newdata[0,:]     = newdata.fill_value
    newdata[ny1,:]   = newdata.fill_value
  else:
    newdata[:,1:nx1] = data
    newdata[:,0]     = newdata.fill_value
    newdata[:,nx1]   = newdata.fill_value

#
# Update the latitude coordinate array too, if requested.
#
# In numpy 1.4.1 and later, you can't test a numpy masked
# array for being equal to None.
#
  if(_is_numpy_ma(lat_coord) or \
     (not _is_numpy_ma(lat_coord) and (not lat_coord is None))):
    newlatcoord          = numpy.zeros(nlat2,lat_coord.dtype.char)
    newlatcoord[1:nlat1] = lat_coord

# Is this south-north, or north-south?
    if(lat_coord[1] > lat_coord[0]):
      newlatcoord[0]   = -90
      newlatcoord[nlat1] =  90
      newlatcoord[nlat1] =  90
    else:
      newlatcoord[0]     =  90
      newlatcoord[nlat1] = -90

    return newdata,newlatcoord
  else:
    return newdata

################################################################

def add_polygon(wks,plot,x,y,rlistc=None,isndc=0):
  """
Adds a polygon to an existing plot and returns a PlotId representing
the polygon added.
pgon = Ngl.add_polygon(wks, plot, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
plot -- The id of the plot which you want to add the polygon to.
x, y -- One-dimensional (masked) NumPy arrays or Python lists containing
        the x, y coordinates of the polygon.
res -- An optional instance of the Resources class having GraphicStyle
       resources as attributes.
  """
  return(_add_poly(wks,plot,x,y,NhlPOLYGON,rlistc,isndc))

################################################################

def add_polyline(wks,plot,x,y,rlistc=None,isndc=0):
  """
Adds polylines to an existing plot and returns a PlotId representing
polylines added.
pline = Ngl.add_polyline(wks, plot, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
plot -- The id of the plot which you want to add the polylines to.
x, y -- One-dimensional (masked) NumPy arrays containing the x, y
        coordinates of the polylines.
res -- An optional instance of the Resources class having GraphicStyle
       resources as attributes.
  """
  return(_add_poly(wks,plot,x,y,NhlPOLYLINE,rlistc,isndc))

################################################################

def add_polymarker(wks,plot,x,y,rlistc=None,isndc=0):
  """
Adds polymarkers to an existing plot and returns a PlotId representing
polymarkers added.
pmarker = Ngl.add_polymarker(wks, plot, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
plot -- The id of the plot which you want to add the polymarkers to.
x, y -- One-dimensional (masked) NumPy arrays containing the x, y
        coordinates of the polymarkers.
res -- An optional instance of the Resources class having GraphicStyle
       resources as attributes.
  """
  return(_add_poly(wks,plot,x,y,NhlPOLYMARKER,rlistc,isndc))

################################################################

def add_text(wks,plot,text,x,y,rlistc=None):
  """
Adds text strings to an existing plot and returns a PlotId representing
the text strings added.
txt = Ngl.add_text(wks, plot, text, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
plot -- The id of the plot which you want to add the text strings to.
text -- An array of text strings to add.
x, y -- One-dimensional arrays containing the x, y coordinates of the
        text strings.
res -- An optional instance of the Resources class having TextItem
       resources as attributes.
  """
  rlist = _crt_dict(rlistc)  
 
#
#  Separate the resource dictionary into those resources
#  that apply to am or tx.
#
  am_rlist  = {}
  tx_rlist  = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:2] == "tx"):
      tx_rlist[key] = rlist[key]
    if (key[0:2] == "am"):
      am_rlist[key] = rlist[key]

#
#  Call the wrapped function and return.
#
  atx = add_text_wrap(wks,_pobj2lst(plot),text,x,y,"double","double",  \
                          tx_rlist,am_rlist, pvoid())
  del rlist
  del tx_rlist
  del am_rlist
  return(_lst2pobj(atx))

################################################################

def asciiread(filename,dims,type="float",sep=","):
  """
Reads data from an ASCII file and returns a NumPy array.
array = Ngl.asciiread(filename, dims, type='float')
filename -- The name of the ASCII file to read.
dims -- A list or tuple specifying the dimension sizes (or -1 to read
        all values into a 1-dimensional array).
type -- An optional argument specifying the type of the data you are
        reading. The legal values are: 'integer', 'float', or
        'double'.
  """
#
#  Regular expression special characters that must be escaped if
#  "sep" is set to one of them.
#
  schar = [".", "^", "$", "*", "+", "?"]
  if (schar.count(sep) > 0):
    sep = "\\" + sep

  file = open(filename)
#
#  If dims = -1, determine the number of valid tokens in
#  the input file, otherwise calculate the number from
#  the dims value.  If dims = -1 the return value will be
#  a NumPy array containing of all the legal values,
#  all other values are ignored.
#
  if (dims == -1):
    nnum = 0
    while(1):
      rline = file.readline()
      if len(rline) == 0:
        break
      
      line = re.sub(sep," ",rline)  # replace separator with blanks
      toks = string.split(line)
      for str in toks:
        if (type == "integer"):
          try:
            int(str)
            nnum = nnum+1
          except:
            pass
        elif ((type == "float") or (type == "double")):
          try:
            float(str)
            nnum = nnum+1
          except:
            pass
  else:
    nnum = 1
    if (not (isinstance(dims,types.ListType)) and \
        not (isinstance(dims,types.TupleType))):
      print ('asciiread: dims must be a list or a tuple')
      return None
    for m in xrange(len(dims)):
      nnum = nnum*dims[m]
 
  if (type == "integer"):
    ar = numpy.zeros(nnum,'i')
  elif (type == "float"):
    ar = numpy.zeros(nnum,'float32')
  elif (type == "double"):
    ar = numpy.zeros(nnum,'float64')
  else:
    print ('asciiread: type must be one of: "integer", "float", or "double".')
    sys.exit()

  count = 0
  file.seek(0,0)
  while (1):
    rline = file.readline()
    if len(rline) == 0:
      break
    line = re.sub(sep," ",rline)  # replace separator with blanks
    toks = string.split(line)
    for tstr in toks:
      str = re.sub(",","",tstr)
      if (type == "integer"):
        try:
          ar[count] = int(str)
          count = count+1
        except:
          pass
      elif ((type == "float") or (type == "double")):
        try:
          ar[count] = float(str)
          count = count+1
        except:
          pass

  if (count < nnum and dims != -1):
    print ("asciiread: Warning, fewer data items than specified array size.")

  file.close()
  if (dims == -1):
    return ar
  else:
    return numpy.reshape(ar,dims)

################################################################

def betainc(x, a, b):
  """
Evaluates the incomplete beta function.
alpha = Ngl.betainc (x,a,b)
x -- upper limit of integration x must must be in (0,1) inclusive and
can only be float or double. Can contain missing values.
a -- first beta distribution parameter; must be > 0.0. Must be same
dimensionality as x.
b -- second beta distribution parameter; must be > 0.0.  Must be same
dimensionality as x.
  """

# Deal with masked array.
  fill_value_x = _get_fill_value(x)

  if not fill_value_x is None:
    x2 = x.filled(fill_value_x)
  else:
    fill_value_x = 1.e20
    x2 = _promote_scalar(x)
  
#
# Promote a and b to numpy arrays that have at least a dimension of 1.
#
  a2 = _promote_scalar(a)
  b2 = _promote_scalar(b)

  result = fplib.betainc(x2, a2, b2, fill_value_x)

  del x2
  del a2
  del b2
# 
#  Return a masked array only if x was a masked array.
# 
  if _is_numpy_ma(x):
    return ma.masked_array(result,fill_value=fill_value_x)
  else:
    return result


################################################################

def blank_plot(wks,rlistc=None):
  """
Creates and draws a blank plot, and returns a PlotId representing the 
plot created.
blankplot = Ngl.blank_plot(wks, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
res -- An (optional) instance of the Resources class having PyNGL
       resources as attributes.
  """
  _set_spc_defaults(1)

  rlist = _crt_dict(rlistc)  
 
#
#  Separate the resource dictionary into those resources
#  that apply to various lists.
#
  bp_rlist  = {}

# For a blank plot, we usually don't want to draw it or advance the frame.
  if not rlist.has_key("nglDraw"):
    rlist["nglDraw"] = False

  if not rlist.has_key("nglFame"):
    rlist["nglFrame"] = False

  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      bp_rlist[key] = rlist[key]

  _set_tickmark_res(rlist,bp_rlist)      # Set some addtl tickmark resources

  if not rlist.has_key("pmTickMarkDisplayMode"):
    bp_rlist["pmTickMarkDisplayMode"] = "Always"

  if not rlist.has_key("pmTitleDisplayMode"):
    bp_rlist["pmTitleDisplayMode"] = "Always"

#
#  Call the wrapped function and return.
#
  ibp = blank_plot_wrap(wks,bp_rlist,pvoid())

  del rlist
  del bp_rlist

# ret.xy and ret.base will be None if XY plot is invalid.
  return(_lst2pobj(ibp))

################################################################

def change_workstation(obj,wks):
  """
Changes the workstation that plots will be drawn to.
Ngl.change_workstation(plot, wks)
plot -- The identifier returned from calling a plotting function
        (Ngl.xy, Ngl.contour_map etc).
wks -- The identifier returned from calling Ngl.open_wks.
  """
  NhlChangeWorkstation(_int_id(obj),wks)

################################################################

def chiinv(x,y):
  """
Evaluates the inverse chi-squared distribution function.
x = Ngl.chiinv(p,df)
p -- Integral of the chi-square distribution ([0 < p <1)
df -- degrees of freedom of the chi-square distribution (0, +infinity).
  """
#
# Promote x and y to numpy arrays that have at least a dimension of 1.
#
  x2 = _promote_scalar(x)
  y2 = _promote_scalar(y)
#
# Determine what kind of array to return. This is dependent on the
# types of the arguments passed to chiinv, and not which fplib
# module was loaded.
#
  if _is_numpy(x) or _is_numpy(y):
    import numpy
    return numpy.array(fplib.chiinv(x2,y2))
  else:
    return fplib.chiinv(x2,y2)

################################################################

def clear_workstation(obj):
  """
Clears a specified workstation.
Ngl.clear_workstation(wks)
wks -- The identifier returned from calling Ngl.open_wks.
  """
  NhlClearWorkstation(_int_id(obj))

################################################################

def contour(wks,array,rlistc=None):
  """
Creates and draws a contour plot, and returns a PlotId of the plot
created.
plot = Ngl.contour(wks, data, res=None)
wks -- The identifier returned from calling Ngl.open_wks
data -- The data to contour. Masked arrays allowed.
res -- An optional instance of the Resources class having PyNGL
       resources as attributes.
  """

#
#  Make sure the array is 1D or 2D.
#
  if (len(array.shape) != 1 and len(array.shape) != 2):
    print ("contour - array must be 1D or 2D")
    return None

# Get NumPy array from masked array, if necessary.
  arr2,fill_value = _get_arr_and_fv(array)
  
  _set_spc_defaults(1)
  rlist = _crt_dict(rlistc)  
 
#  Separate the resource dictionary into those resources
#  that apply to ScalarField and those that apply to
#  ContourPlot.
#
  rlist1 = {}
  rlist2 = {}
  rlist3 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:2] == "sf"):
      rlist1[key] = rlist[key]
    elif(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist2[key] = rlist[key]
#
# In addition, if this plot is potentially going to be overlaid
# on an Irregular Plot Class (in order to lineariize or logize it)
# then we need to keep track of all the tickmark resources, because
# we'll have to reapply them to the IrregularPlot class.
#
      if(key[0:2] == "vp" or key[0:2] == "tm" or key[0:6] == "pmTick"):
        rlist3[key] = rlist[key]

# Set missing value resource, if necessary
  _set_msg_val_res(rlist1,fill_value,"scalar")

  _set_contour_res(rlist,rlist2)       # Set some addtl contour resources
  _set_labelbar_res(rlist,rlist2,True) # Set some addtl labelbar resources
  _set_tickmark_res(rlist,rlist3)      # Set some addtl tickmark resources
#
#  Call the wrapped function and return.
#
  if (len(arr2.shape) == 2):
    icn = contour_wrap(wks,arr2,"double",arr2.shape[0],arr2.shape[1], \
                           0, pvoid(),"",0,pvoid(),"", 0, pvoid(), rlist1, \
                          rlist2,rlist3,pvoid())
  else:
    icn = contour_wrap(wks,arr2,"double",arr2.shape[0],-1, \
                           0, pvoid(),"",0,pvoid(),"", 0, pvoid(), rlist1, \
                          rlist2,rlist3,pvoid())

  del rlist
  del rlist1
  del rlist2
  del rlist3
  return(_lst2pobj(icn))

################################################################

def contour_map(wks,array,rlistc=None):
  """
Creates and draws contours over a map, and returns a PlotId of the plot
created.
plot = Ngl.contour_map(wks, data, res=None)
wks -- The identifier returned from calling Ngl.open_wks
data -- The data to contour. Masked arrays allowed.
res -- An optional instance of the Resources class having PyNGL
       resources as attributes.
  """
#
#  Make sure the array is 2D.
#
  if (len(array.shape) != 1 and len(array.shape) != 2):
    print ("contour_map - array must be 1D or 2D")
    return None

# Get NumPy array from masked array, if necessary.
  arr2,fill_value = _get_arr_and_fv(array)
    
  _set_spc_defaults(1)
  rlist = _crt_dict(rlistc)  
 
#  Separate the resource dictionary into those resources
#  that apply to ScalarField, MapPlot, and ContourPlot.
#
  rlist1 = {}
  rlist2 = {}
  rlist3 = {}

  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
# Now sort resources into correct individual resource lists.
    if (key[0:2] == "sf"):
      rlist1[key] = rlist[key]
    elif( (key[0:2] == "mp") or (key[0:2] == "vp") or (key[0:3] == "pmA") or \
          (key[0:3] == "pmO") or (key[0:3] == "pmT") or (key[0:2] == "tm") or \
          (key[0:2] == "ti") ):
      rlist2[key] = rlist[key]
    elif(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist3[key] = rlist[key]

# Set missing value resource, if necessary
  _set_msg_val_res(rlist1,fill_value,"scalar")

  _set_map_res(rlist,rlist2)           # Set some addtl map resources
  _set_contour_res(rlist,rlist3)       # Set some addtl contour resources
  _set_labelbar_res(rlist,rlist3,True) # Set some addtl labelbar resources

# 
# Test for masking a lambert conformal plot.
#
  mask_list = _test_for_mask_lc(rlist,rlist2)

#
#  Call the wrapped function and return.
#
  if (len(arr2.shape) == 2):
        icm = contour_map_wrap(wks,arr2,"double", \
                                arr2.shape[0],arr2.shape[1],0, \
                                pvoid(),"",0,pvoid(),"", 0, pvoid(), \
                                rlist1,rlist3,rlist2,pvoid())
  else:
        icm = contour_map_wrap(wks,arr2,"double", \
                                arr2.shape[0],-1,0, \
                                pvoid(),"",0,pvoid(),"", 0, pvoid(), \
                                rlist1,rlist3,rlist2,pvoid())

  licm = _lst2pobj(icm)

  if mask_list["MaskLC"]:
    licm = _mask_lambert_conformal(wks, licm, mask_list, rlist2)

  del rlist
  del rlist1
  del rlist2
  del rlist3
  return(licm)

################################################################

def datatondc(obj,x,y):
  """
Converts coordinates in data space to coordinates in NDC
space. Missing values are ignored.
xndc,yndc = Ngl.datatondc(plot,xdata,ydata)
plot -- The identifier returned from calling any plot object creation
        function, like Ngl.xy, Ngl.contour, Ngl.vector_map, etc.
xdata,ydata -- One dimensional (masked) arrays containing values to be
               converted.
  """

  x2,fvx = _get_arr_and_fv(x)
  y2,fvy = _get_arr_and_fv(y)

# Set flags indicating whether missing values present.
  fvx,ismx = _set_default_msg(fvx)
  fvy,ismy = _set_default_msg(fvy)

  error,xout,yout,status,range = \
     NhlPDataToNDC(_int_id(obj),x2,y2,len(_promote_scalar(x2)),
                   fvx,fvy,ismx,ismy)

# Convert to masked array if input was masked array, or any of the
# values are outside the plot data space.
  if ismx or status == 1:
    xout = _convert_to_ma(xout,range)
  if ismy or status == 1:
    yout = _convert_to_ma(yout,range)

  del error,status,range
  return xout,yout

################################################################

def define_colormap(wks,cmap):
  """
Defines a new color map for the given workstation.
Ngl.define_colormap(wks,cmap)
wks -- The identifier returned from calling Ngl.open_wks.
cmap -- An n x 3 array of RGB triplets, or a predefined colormap name.
  """
  cres = Resources()
  cres.wkColorMap = cmap
  set_values(wks,cres)
  return None

################################################################

def delete_wks(wks):
  """
Deletes a workstation object that was created using open_wks.
Calling this function after you are finished drawing to a workstation
provides for the sequential opening and deleting of an indefinite number of
workstations, thus avoiding any restrictions on the maximum number of
simultaneously open workstations of a given type.
Ngl.delete_wks(wks))
wks -- The identifier returned from calling Ngl.open_wks.
  """
  NhlDestroy(wks)
  return None

################################################################

def destroy(obj):
  """
Destroys an Ngl object.
Ngl.destroy(object)
object -- The identifier returned from calling any object creation
          function, like Ngl.xy, Ngl.contour, Ngl.open_wks, etc.
  """
  NhlDestroy(_int_id(obj))
  return None

################################################################

def dim_gbits(npack,ibit,nbits,nskip,iter):
  """
Unpacks bit chunks from the rightmost dimension of the input array.
xchunk = Ngl.dim_gbits(npack,ibit,nbits,nskip,iter)
ibit -- a bit-count offset to be used before the first bit chunk is unpacked.
nbits -- the number of bits in each bit chunk to be unpacked.
nskip -- the number of bits to skip between each bit chunk to be unpacked
(after the first bit chunk has been unpacked)
iter -- the number of bit chunks to be unpacked.
  """
#
# Make sure main value is not a python scalar
#
  npack2 = _promote_scalar_int32(npack)

  npack_dtype = npack2.dtype

  if( npack_dtype != numpy.int8  and npack_dtype != numpy.uint8 and \
      npack_dtype != numpy.int16 and npack_dtype != numpy.uint16 and \
      npack_dtype != numpy.int32 and npack_dtype != numpy.uint32):
    print("dim_gbits: Error: wrong type for npack")
    return None

  ibit2  = _promote_scalar_int32(ibit)
  nbits2 = _promote_scalar_int32(nbits)
  nskip2 = _promote_scalar_int32(nskip)
  iter2  = _promote_scalar_int32(iter)

  return(fplib.dim_gbits(npack2,ibit2,nbits2,nskip2,iter2))

################################################################

def draw(obj):
  """
Draws an Ngl plot object.
Ngl.draw(plot)
plot -- The identifier returned from calling any plot object creation
        function, like Ngl.xy, Ngl.contour, Ngl.vector_map, etc.
  """
  NhlDraw(_int_id(obj))
  return None

################################################################

def draw_colormap(wks):
  """
Draws the current color map and advances the frame.
Ngl.draw_colormap(wks)
wks -- The identifier returned from calling Ngl.open_wks.
  """
  draw_colormap_wrap(wks)
  return None

################################################################

def draw_color_palette(wks,colormap_name=None,opt=None):
  """
Draws the given color map and advances the frame.
If no color map is given, then the current colormap 
associated with the given workstation is drawn.
Ngl.draw_color_palette(wks,colormap_name,opt)
wks -- The identifier returned from calling Ngl.open_wks.
colormap_name -- The name of the predefined colormap to draw, 
  i.e. "rainbow"
opt -- The identifier returned from Ngl.Resources(). An optional
       list of resources you can set (not yet defined).
  """

#---Retrieve values for attributes
  if wks is None:
    wks = open_wks("x11","color_map")

  call_frame    = _get_res_value_keep(opt,"Frame",True)
  labels_on     = _get_res_value_keep(opt,"LabelsOn",True)

  if(not opt is None and hasattr(opt,"LabelStrings")):
    set_label_strings = True
    label_strings     = opt.LabelStrings
  else:
    set_label_strings = False

  font_height   = _get_res_value_keep(opt,"LabelFontHeight",0.015)
  across        = _get_res_value_keep(opt,"Across",True)

  if colormap_name is None:
    rgb = retrieve_colormap(wks)
  else:
    rgb = read_colormap_file(colormap_name)
  ncolors  = rgb.shape[0]
  nrows    = int(numpy.sqrt(ncolors))

#---Figure out ncols such that the columns will span across the page.
  ncols = int(ncolors/nrows)
  if((ncols*nrows) < ncolors):
    ncols = ncols+1

  ntotal = nrows * ncols        # # of colors per page.

#---If drawing labels, test that we have valid number of labels
  if(labels_on):
    if( not set_label_strings):
      label_strings = ['%d' % i for i in range(ncolors)]
    else:
      if(len(label_strings) != ncolors):
        print("Error: draw_color_palette: invalid number of labels for boxes")
        return

#---Calculate X and Y positions of text and box in the view port.
  width  = 1./ncols
  height = 1./nrows

  if(ncols > 1):
    xpos_2d    = numpy.empty([nrows,ncols])
    xpos_2d[:] = fspan(0,1-width,ncols)
    if(across):
      xpos = numpy.ravel(xpos_2d)
    else:
      xpos = numpy.ravel(xpos_2d.T)
  else:
    xpos = numpy.empty(ntotal)
    xpos.fill(0.)

  if(nrows > 1):
    ypos_2d = numpy.empty([ncols,nrows])
    ypos_2d[:] = fspan(1-height,0,nrows)
    if(across):
      ypos = numpy.ravel(ypos_2d.T)
    else:
      ypos = numpy.ravel(ypos_2d)
  else:
    ypos = numpy.empty(ntotal)
    ypos.fill(1.-height)

#---Calculate box coordinates.
  xbox = [0,width, width,     0,0]
  ybox = [0,    0,height,height,0]

  gnres = Resources()   # variables to hold list of resources
  lnres = Resources()

  if(labels_on):
    font_space                  = font_height/2.
    txres                       = Resources()
    txres.txFontHeightF         = font_height
    txres.txFont                = "helvetica-bold"
    txres.txJust                = "BottomLeft"
    txres.txPerimOn             = True
    txres.txPerimColor          = "black"
    txres.txFontColor           = "black"
    txres.txBackgroundFillColor = "white"

  lnres.gsLineColor  = "black"

#---ntotal colors per page.
  for i in range(ncolors):
#---Draw box and fill in the appropriate color.
    gnres.gsFillColor = rgb[i,:]
    polygon_ndc(wks,xbox+xpos[i],ybox+ypos[i],gnres) # Draw box.

#---Outline box in black.
    polyline_ndc(wks,xbox+xpos[i],ybox+ypos[i],lnres)

#---Draw color label.
    if(labels_on):
      text_ndc(wks,label_strings[i],font_space+xpos[i],ypos[i]+font_space,txres)

  if(call_frame):
    frame(wks)   # Advance the frame.
  return

################################################################

def draw_ndc_grid(wks):
  """
Draws grid lines at 0.1 NDC intervals and labels them.
Ngl.draw_ndc_grid(wks)
wks -- The identifier returned from calling Ngl.open_wks.
  """
  igray = new_color(wks,0.72,0.72,0.72)        # Add gray.

  gridres = Resources()                        # polyline mods desired
  gridres.gsLineColor            = igray       # color of lines
  gridres.gsLineThicknessF       = 1.5         # thickness of lines
  gridres.gsLineDashPattern      = 1	       # dash the lines
  gridres.gsLineLabelFontColor   = igray       # color of labels
  gridres.gsLineLabelFontHeightF = 0.0105      # size of labels

#
# Draw and label vertical and horizontal lines at 0.1 intervals.
#
  for gh in range(1,10):
    gridres.gsLineLabelString = gh*10/100.     # adds a line label string

    polyline_ndc(wks,[0.,1.],[gh*10/100.,gh*10/100.],gridres)
    polyline_ndc(wks,[gh*10/100.,gh*10/100.],[0.,1.],gridres)

#
# Draw and label vertical and horizontal lines at the very
# edges at 0.01 and 0.99 NDC.
#
  gridres.gsLineLabelString = 0.01
  polyline_ndc(wks,[0.,1.],[0.01,0.01],gridres)

  gridres.gsLineLabelString = 0.99
  polyline_ndc(wks,[0.,1.],[0.99,0.99],gridres)

  gridres.gsLineLabelString = 0.01
  polyline_ndc(wks,[0.01,0.01],[0.,1.],gridres)

  gridres.gsLineLabelString = 0.99
  polyline_ndc(wks,[0.99,0.99],[0.,1.],gridres)

  return None

################################################################

def end():
  """
Terminates a PyNGL script, flushes all buffers, and closes all
internal files.
Ngl.end()
  """
  NhlClose()
  return None

################################################################

def frame(wks):
  """
Terminates a picture on a specified workstation.
Ngl.frame(wks)
wks -- The identifier returned from calling Ngl.open_wks.
  """
  NhlFrame(wks)
  return None

################################################################

def fspan(min,max,num):
  """
Returns an array of evenly-spaced floating point numbers.
sarray = Ngl.fspan(start, end, num)
start -- Value at which to start.
end -- Value at which to end.
num -- Number of equally-spaced points desired between start and end.
  """
  delta = (float(max-min)/float(num-1))
  a = []
  for i in range(num-1):
    a.append(min + float(i)*delta)
  a.append(max)
  return numpy.array(a,'f')

################################################################

def ftcurv(x,y,xo):
  """
Calculates an interpolatory spline through a sequence of functional
values.
iarray = Ngl.ftcurv(xi, yi, xo)
xi -- An array containing the abscissae for the input function, with
      rightmost dimension npts. If xi is multi-dimensional, it must
      have the same dimension sizes as yi.
yi -- An array of any dimensionality, whose rightmost dimension is
      npts, containing the functional values of the input
      function. That is, yi(...,k) is the functional value at
      xi(...,k) for k=0,npts-1.
xo -- A 1D array of length nxo containing the abscissae for the
      interpolated values.
  """
  if _is_list_or_tuple(x):
    dsizes_x = len(x)
  elif _is_numpy_array(x):
    dsizes_x = x.shape[0]
  else:
    print (\
     "ftcurv: type of argument 1 must be one of: list, tuple, or NumPy array")
    return None
  if _is_list_or_tuple(y):
    dsizes_y = len(y)
  elif _is_numpy_array(y):
    dsizes_y = y.shape[0]
  else:
    print (\
     "ftcurv: type of argument 2 must be one of: list, tuple, or NumPy array")
    return None
  if (dsizes_x != dsizes_y):
    print ("ftcurv: first and second arguments must be the same length.")
    return None

  if _is_list_or_tuple(xo):
    dsizes_xo = len(xo)
  elif _is_numpy_array(xo):
    dsizes_xo = xo.shape[0]

  status,yo = ftcurvc(dsizes_x,x,y,dsizes_xo,xo)
  if (status == 1):
    print ("ftcurv: input array must have at least three elements.")
    return None
  elif (status == 2): 
    print ("ftcurv: input array values must be strictly increasing.")
    return None
  else:
    del status
    return yo

################################################################

def ftcurvp(x,y,p,xo):
  """
Calculates an interpolatory spline under tension through a sequence of
functional values for a periodic function.
iarray = Ngl.ftcurvp(xi, yi, p, xo)
xi -- An array containing the abscissae for the input function, with
      rightmost dimension npts. If xi is multi-dimensional, it must
      have the same dimension sizes as yi.
yi -- An array of any dimensionality, whose rightmost dimension is
      npts, containing the functional values of the input
      function. That is, yi(...,k) is the functional value at
      xi(...,k) for k=0,npts-1.
p -- A scalar value specifying the period of the input function; the
     value must not be less than xi(npts-1) - xi(0).
xo -- A 1D array of length nxo containing the abscissae for the
      interpolated values.
  """
  if _is_list_or_tuple(x):
    dsizes_x = len(x)
  elif _is_numpy_array(x):
    dsizes_x = x.shape[0]
  else:
    print (\
     "ftcurvp: type of argument 1 must be one of: list, tuple, or NumPy array")
    return None
  if _is_list_or_tuple(y):
    dsizes_y = len(y)
  elif _is_numpy_array(y):
    dsizes_y = y.shape[0]
  else:
    print (\
     "ftcurvp: type of argument 2 must be one of: list, tuple, or NumPy array")
    return None
  if (dsizes_x != dsizes_y):
    print ("ftcurvp: first and second arguments must be the same length.")
    return None

  if _is_list_or_tuple(xo):
    dsizes_xo = len(xo)
  elif _is_numpy_array(xo):
    dsizes_xo = xo.shape[0]

  status,yo = ftcurvpc(dsizes_x,x,y,p,dsizes_xo,xo)
  if (status == 1):
    print ("ftcurvp: input array must have at least three elements.")
    return None
  elif (status == 2):
    print ("ftcurvp: the period is strictly less than the span of the abscissae.")
    return None
  else:
    del status
    return yo

################################################################

def ftcurvpi(xl, xr, p, x, y):
  """
Calculates an integral of an interpolatory spline between two
specified points.
iarray = Ngl.ftcurvpi(xl, xr, p, xi, yi)
xl -- A scalar value containing the lower limit of the integration.
xr -- A scalar value containing the upper limit of the integration.
p -- A scalar value specifying the period of the input function; the
     value must not be less than xi(npts-1) - xi(0).
xi -- An array containing the abscissae for the input function, with
      rightmost dimension npts. If xi is multi-dimensional, it must
      have the same dimension sizes as yi.
yi -- An array of any dimensionality, whose rightmost dimension is
      npts, containing the functional values of the input
      function. That is, yi(...,k) is the functional value at
      xi(...,k) for k=0,npts-1.
  """
  if _is_list_or_tuple(x):
    dsizes_x = len(x)
  elif _is_numpy_array(x):
    dsizes_x = x.shape[0]
  else:
    print (\
     "ftcurvpi: type of argument 4 must be one of: list, tuple, or NumPy array")
    return None
  if _is_list_or_tuple(y):
    dsizes_y = len(y)
  elif _is_numpy_array(y):
    dsizes_y = y.shape[0]
  else:
    print (\
     "ftcurvpi: type of argument 5 must be one of: list, tuple, or NumPy array")
    return None
  if (dsizes_x != dsizes_y):
    print ("ftcurvpi: fourth and fifth arguments must be the same length.")
    return None

  return (ftcurvpic(xl,xr,p,dsizes_x,x,y)[1])

################################################################

def gaus(n):
  """
Computes gaussian latitudes and weights and returns a NumPy array
dimensioned 2*nlat-by-2.
ginfo = Ngl.gaus(nlat)
nlat -- A scalar integer equal to the number of latitude points per
        hemisphere.
  """
  return NglGaus_p(n,2*n,2)[1]

################################################################

def gc_convert(angle,ctype):
  """
Converts degrees along a great circle to radians, meters, feet, or
kilometers and returns a NumPy array of the same shape as angle.
conv_vals = Ngl.gc_convert(angle, type)
angle -- A one-dimensional NumPy array (or scalar value) of angles
         (in degrees).
type -- A string (or integer) indicating the units you want to convert
        to. Legal values are:
        "radians"    (or 0)
        "meters"     (or 1)
        "kilometers" (or 2)
        "feet"       (or 3)
        "miles"      (or 4)
  """

#
#  Convert an angle in degrees along a great circle to
#  radians, meters, kilometers, or feet.
#
  d2r =  0.0174532952   # degrees to radians
  r2m = 6371220.        # radians to meters
  m2f = 3.2808          # meters to feet

  dtype = ctype
  if (ctype == 0):
    dtype = "ra"
  elif (ctype == 1):
    dtype = "me"
  elif (ctype == 2):
    dtype = "ki"
  elif (ctype == 3):
    dtype = "fe"
  elif (ctype == 4):
    dtype = "mi"

  if (dtype[0:2] == "ra"):
    return d2r*angle
  elif (dtype[0:2] == "me"):
    return d2r*angle*r2m
  elif (dtype[0:2] == "ki"):
    return d2r*angle*r2m/1000.
  elif (dtype[0:2] == "fe"):
    return d2r*angle*r2m*m2f
  elif (dtype[0:2] == "mi"):
    return d2r*angle*r2m*m2f/5280.
  else:
    print ("gc_convert: unrecognized conversion type " + str(ctype))

################################################################

def gc_dist(rlat1,rlon1,rlat2,rlon2):
  """
Calculates the distance in degrees along a great circle between two
points.
dist = Ngl.gc_dist(lat1, lon1, lat2, lon2)
lat1, lon1 -- Latitude and longitude of first point on the globe.
lat2, lon2 -- Latitude and longitude of second point on the globe.
  """
  return c_dgcdist(rlat1,rlon1,rlat2,rlon2,2)

################################################################

def gc_interp(rlat1,rlon1,rlat2,rlon2,numi):
  """
Interpolates points along a great circle between two specified points
on the globe. The returned latitudes and longitudes are returned as
NumPy arrays in degrees in the interval [0.,360) if npts is positive
and in the interval [-180.,180.) if npts is negative.
lat,lon = Ngl.gc_interp(lat1, lon1, lat2, lon2, npts)
lat1, lon1 -- Latitude and longitude, in degrees, of the first point
              on the globe.
lat2, lon2 -- Latitude and longitude, in degrees, of second point on
              the globe.
npts -- The number of equally-spaced points you want to interpolate to.
  """
  num = abs(numi)
  if (abs(num) < 2):
    print ("gc_interp: the number of points must be at least two.")
  elif (num == 2):
    lat = numpy.array([rlat1,rlat2],'f')
    lon = numpy.array([rlon1,rlon2],'f')
    return [lat,lon]
  else:
    lat_tmp = numpy.zeros(num,'f')
    lon_tmp = numpy.zeros(num,'f')
    lat,lon = mapgci(rlat1,rlon1,rlat2,rlon2,num-2)
    lon0_tmp = rlon1
    lon1_tmp = rlon2
#
#  Adjust points to be in the desired range.
#
    for i in range(0,num-2):
      if (numi > 0):
        lon[i] = normalize_angle(lon[i],0)
      else:
        lon[i] = normalize_angle(lon[i],1)
    if (numi > 0):
      lon0_tmp = normalize_angle(lon0_tmp,0) 
      lon1_tmp = normalize_angle(lon1_tmp,0)
    else:
      lon0_tmp = normalize_angle(lon0_tmp,1) 
      lon1_tmp = normalize_angle(lon1_tmp,1)

#
#  Set up return arrays.
#
    lat_tmp[1:num-1] = lat[0:num-2]
    lon_tmp[1:num-1] = lon[0:num-2]
    lat_tmp[0]     = rlat1
    lat_tmp[num-1] = rlat2
    lon_tmp[0]     = lon0_tmp
    lon_tmp[num-1] = lon1_tmp
    del lat,lon

    return lat_tmp,lon_tmp

################################################################

def gc_inout(plat,plon,lat,lon):
  """
Determines if a set of lat/lon points are inside or outside of a spherical polygon.
inout = Ngl.gc_inout(plat, plon, lat, lon)
plat, plon -- Latitude and longitude, in degrees, of a set 
              of points on the globe.
lat, lon -- Latitude and longitude, in degrees, of the vertices
            of a spherical polygon.
  """
#
# Promote plat and plon to numpy arrays that have at least a dimension of 1.
#
  plat2 = _promote_scalar(plat)
  plon2 = _promote_scalar(plon)
  return(fplib.gc_inout(plat2,plon2,lat,lon))

################################################################

def gc_tarea(lat1, lon1, lat2, lon2, lat3, lon3, radius=1.):
  """
Finds the area of a triangular patch on a sphere whose vertices
are given in degrees as lat/lon pairs.
area = Ngl.gc_tarea(lat1, lon1, lat2, lon2, lat3, lon3, radius=1.)
lat1, lon1 -- Latitude and longitude, in degrees, of the first vertex.
              These can be scalars, lists, or NumPy arrays.
lat2, lon2 -- Latitude and longitude, in degrees, of the second vertex.
              These can be scalars, lists, or NumPy arrays.
lat3, lon3 -- Latitude and longitude, in degrees, of the third vertex.
              These can be scalars, lists, or NumPy arrays.
radius     -- An optional argument specifying the radius of the sphere.
The returned object is a scalar if the arguments are scalars,
or a NumPy array of the same size as the input arrays otherwise.
Any area returned is that bounded by the arcs of great circles
connecting the vertices.
  """
  lat1t = numpy.atleast_1d(numpy.array(lat1)).astype(float)
  lon1t = numpy.atleast_1d(numpy.array(lon1)).astype(float)
  lat2t = numpy.atleast_1d(numpy.array(lat2)).astype(float)
  lon2t = numpy.atleast_1d(numpy.array(lon2)).astype(float)
  lat3t = numpy.atleast_1d(numpy.array(lat3)).astype(float)
  lon3t = numpy.atleast_1d(numpy.array(lon3)).astype(float)
  
  rtn = numpy.zeros(len(lat1t),'f')
  pi  = 4.*math.atan(1.)
  d2r = pi/180.
  tol = 1.e-7
  for i in xrange(len(lat1t)):
    a = d2r*gc_dist(lat1t[i], lon1t[i], lat2t[i], lon2t[i])
    b = d2r*gc_dist(lat2t[i], lon2t[i], lat3t[i], lon3t[i])
    c = d2r*gc_dist(lat3t[i], lon3t[i], lat1t[i], lon1t[i])
    sa, sb, sc = math.sin(a), math.sin(b), math.sin(c)
    if (abs(sa) < tol or abs(sb) < tol or abs(sc) < tol):
      print ("gc_tarea: input vertices must be distinct and not be polar opposites.")
      sys.exit()
    ca, cb, cc = math.cos(a), math.cos(b), math.cos(c)
    sang1 = math.acos( (ca-cb*cc)/(sb*sc) )
    sang2 = math.acos( (cb-ca*cc)/(sa*sc) )
    sang3 = math.acos( (cc-ca*cb)/(sa*sb) )
    rtn[i] = radius*radius*(sang1 + sang2 + sang3 - pi)
  del lat1t,lon1t,lat2t,lon2t,lat3t,lon3t,a,b,c,sa,sb,sc,ca,cb,cc, \
      sang1,sang2,sang3,tol
  if (_is_scalar(lat1)):
    return rtn[0]
  else:
    return rtn

################################################################

def gc_qarea(lat1, lon1, lat2, lon2, lat3, lon3, lat4, lon4, radius=1.):
  """
Finds the area of a convex quadrilateral patch on a sphere whose vertices
are given in degrees as lat/lon pairs.
area = Ngl.gc_qarea(lat1, lon1, lat2, lon2, lat3, lon3, radius=1.)
lat1, lon1 -- Latitude and longitude, in degrees, of the first vertex.
              These can be scalars, lists, or NumPy arrays.
lat2, lon2 -- Latitude and longitude, in degrees, of the second vertex.
              These can be scalars, lists, or NumPy arrays.
lat3, lon3 -- Latitude and longitude, in degrees, of the third vertex.
              These can be scalars, lists, or NumPy arrays.
lat4, lon4 -- Latitude and longitude, in degrees, of the fourth vertex.
              These can be scalars, lists, or NumPy arrays.
radius     -- An optional argument specifying the radius of the sphere.
The returned spherical area is a scalar if the arguments are scalars
or a NumPy array of the same size as the input arrays otherwise.
The vertices must be entered in either clockwise or counter-clockwise order.
A returned area is that bounded by arcs of great circles connecting
the vertices.
  """
  return gc_tarea(lat1, lon1, lat2, lon2, lat3, lon3, radius=radius) +  \
         gc_tarea(lat1, lon1, lat3, lon3, lat4, lon4, radius=radius)

################################################################

def generate_2d_array(dims, num_low, num_high, minv, maxv, seed=0, \
                      highs_at=None, lows_at=None):
  """
Generates smooth 2D arrays primarily for use in examples.
array = generate_2d_array(dims, num_low, num_high, minv, maxv, seed=0,
                          highs_at=None, lows_at=None)
dims -- a list (or array) containing the dimensions of the
        two-dimensional array to be returned.
num_low, num_high -- Integers representing the approximate minimum 
                     and maximum number of highs and lows that the 
                     output array will have. They must be in the 
                     range 1 to 25. If not, then they will be set to 
                     either 1 or 25.
minv, maxv -- The exact minimum and maximum values that the output array 
              will have.
iseed -- an optional argument specifying a seed for the random number
         generator.  If iseed is outside the range 0 to 99, it will
         be set to 0.
lows_at -- an optional argument that is a list of coordinate  
           pairs specifying where the lows will occur.  If this
           argument appears, then its length must equal num_low and
           the coordinates must be in the ranges specified in dims.
highs_at -- an optional argument that is a list of coordinate  
            pairs specifying where the highs will occur.  If this
            argument appears, then its length must equal num_high and
            the coordinates must be in the ranges specified in dims.
  """  
#
#  Globals for random numbers.
#
  global dfran_iseq
  dfran_iseq = seed
#
#  Check arguments.
#
  try:
    alen = len(dims)
  except:
    print ("generate_2d_array: first argument must be a list, tuple, or array having two elements specifying the dimensions of the output array.")
    return None
  if (alen != 2):   
    print ("generate_2d_array: first argument must have two elements specifying the dimensions of the output array.")
    return None
  if (int(dims[0]) <=1 and int(dims[1]) <=1):
    print ("generate_2d_array: array must have at least two elements.")
    return None
  if (num_low < 1):
    print ("generate_2d_array: number of lows must be at least 1 - defaulting to 1.")
    num_low = 1
  if (num_low > 25):
    print ("generate_2d_array: number of lows must be at most 25 - defaulting to 25.")
    num_high =25
  if (num_high < 1):
    print ("generate_2d_array: number of highs must be at least 1 - defaulting to 1.")
    num_high = 1
  if (num_high > 25):
    print ("generate_2d_array: number of highs must be at most 25 - defaulting to 25.")
    num_high =25
  if (seed > 100 or seed < 0):
    print ("generate_2d_array: seed must be in the interval [0,100] - seed set to 0.")
    seed = 0
  if not lows_at is None:
    if (len(lows_at) != num_low):
      print ("generate_2d_array: the list of positions for the lows must be the same size as num_low.")
  if not highs_at is None:
    if (len(highs_at) != num_high):
      print ("generate_2d_array: the list of positions for the highs must be the same size as num_high.")

#
#  Dims are reversed in order to get the same results as the NCL function.
#
  nx = int(dims[1])
  ny = int(dims[0])
  out_array = numpy.zeros([nx,ny],'f')
  tmp_array = numpy.zeros([3,51],'f')
  fovm = 9./float(nx)
  fovn = 9./float(ny)
  nlow = max(1,min(25,num_low))
  nhgh = max(1,min(25,num_high))
  ncnt = nlow + nhgh

#
  for k in xrange(num_low):
    if not lows_at is None:
      tmp_array[0,k] =  float(lows_at[k][1])   # lows at specified locations.
      tmp_array[1,k] =  float(lows_at[k][0])
      tmp_array[2,k] = -1.
    else:
      tmp_array[0,k] =  1.+(float(nx)-1.)*_dfran() # lows at random locations.
      tmp_array[1,k] =  1.+(float(ny)-1.)*_dfran() # lows at random locations.
      tmp_array[2,k] = -1.
  for k in xrange(num_low,num_low+num_high):
    if not highs_at is None:
      tmp_array[0,k] =  float(highs_at[k-num_low][1])  # highs locations
      tmp_array[1,k] =  float(highs_at[k-num_low][0])  # highs locations
      tmp_array[2,k] =  1.
    else:
      tmp_array[0,k] =  1.+(float(nx)-1.)*_dfran() # highs at random locations.
      tmp_array[1,k] =  1.+(float(ny)-1.)*_dfran() # highs at random locations.
      tmp_array[2,k] =  1.
  
  dmin =  1.e+36
  dmax = -1.e+36
  midpt = 0.5*(minv + maxv)
  for j in xrange(ny):
    for i in xrange(nx):
      out_array[i,j] = midpt
      for k in xrange(ncnt):
        tempi = fovm*(float(i+1)-tmp_array[0,k])
        tempj = fovn*(float(j+1)-tmp_array[1,k])
        temp  = -(tempi*tempi + tempj*tempj)
        if (temp >= -20.):
          out_array[i,j] = out_array[i,j] +    \
             midpt*tmp_array[2,k]*math.exp(temp)
      dmin = min(dmin,out_array[i,j])
      dmax = max(dmax,out_array[i,j])
                   
  out_array = (((out_array-dmin)/(dmax-dmin))*(maxv-minv))+minv

  del tmp_array

  return numpy.transpose(out_array,[1,0])


def _get_double(obj,name):
  return(NhlGetDouble(_int_id(obj),name))

def _get_double_array(obj,name):
  return(NhlGetDoubleArray(_int_id(obj),name))

################################################################

def get_float(obj,name):
  """
Retrieves the value of a resource that uses a float scalar.
fval = Ngl.get_float(plotid, resource_name)
plotid -- The identifier returned from Ngl.open_wks, or any PyNGL
          function that returns a PlotId.
resource_name -- The name of the resource whose value you want to
                 retrieve.
  """  
  return(NhlGetFloat(_int_id(obj),name))

################################################################

def get_bounding_box(obj):
  """
Retrieves the NDC bounding box values for the given object.
plotid -- The identifier returned from Ngl.open_wks, or any PyNGL
          function that returns a PlotId.
  """  
  t = numpy.zeros(1,'f')
  b = numpy.zeros(1,'f')
  l = numpy.zeros(1,'f')
  r = numpy.zeros(1,'f')
  t,b,l,r = getbb(_int_id(obj))
  return t,b,l,r

################################################################

def get_float_array(obj,name):
  """
Retrieves the value of a resource that uses a one-dimensional float array.
farr = Ngl.get_float_array(plotid, resource_name)
plotid -- The identifier returned from Ngl.open_wks, or any PyNGL
          function that returns a PlotId.
resource_name -- The name of the resource whose value you want to
                 retrieve.
  """
  return(NhlGetFloatArray(_int_id(obj),name))

################################################################

def get_integer(obj,name):
  """
Retrieves the value of a resource that uses an integer scalar.
ival = Ngl.get_integer(plotid, resource_name)
plotid -- The identifier returned from Ngl.open_wks, or any PyNGL
          function that returns a PlotId.
resource_name -- The name of the resource whose value you want to
                 retrieve.
  """  
  return(NhlGetInteger(_int_id(obj),name))

################################################################

def get_integer_array(obj,name):
  """
Retrieves the value of a resource that uses a one-dimensional integer array.
iarr = Ngl.get_integer_array(plotid, resource_name)
plotid -- The identifier returned from Ngl.open_wks, or any PyNGL
          function that returns a PlotId.
resource_name -- The name of the resource whose value you want to
                 retrieve.
  """
  return(NhlGetIntegerArray(_int_id(obj),name))

def _get_MDdouble_array(obj,name):
  rval = NhlGetMDDoubleArray(_int_id(obj),name)
  if (rval[0] != -1):
    print ("get_MDdouble_array: error number %d" % (rval[0]))
    return None
  return(rval[1])

################################################################

def get_MDfloat_array(obj,name):
  """
Retrieves the value of a resource that uses a multi-dimensional float
array.
farr = Ngl.get_MDfloat_array(plotid, resource_name)
plotid -- The identifier returned from Ngl.open_wks, or any PyNGL
          function that returns a PlotId.
resource_name - The name of the resource whose value you want to
                retrieve.
  """
  rval = NhlGetMDFloatArray(_int_id(obj),name)
  if (rval[0] != -1):
    print ("get_MDfloat_array: error number %d" % (rval[0]))
    return None
  return(rval[1])

################################################################

def get_MDinteger_array(obj,name):
  """
Retrieves the value of a resource that uses a multi-dimensional
integer array.
iarr = Ngl.get_MDinteger_array(plotid, resource_name)
plotid -- The identifier returned from Ngl.open_wks, or any PyNGL
          function that returns a PlotId.
resource_name - The name of the resource whose value you want to
                retrieve.
  """
  rval = NhlGetMDIntegerArray(_int_id(obj),name)
  if (rval[0] != -1):
    print ("get_MDinteger_array: error number %d" % (rval[0]))
    return None
  return(rval[1])

################################################################

#
#  Returns the color index whose associated color on the given
#  workstation is closest to the color name supplied.
#
def get_named_color_index(wkid,name):
  """
Returns the color index whose associated color on the given
workstation is closest to the color name supplied.
cindex = Ngl.get_named_color_index(wks, color_name)
wks -- The identifier returned from calling Ngl.open_wks.
color_name -- A color name from the rgb.txt file.
  """
  return(NhlGetNamedColorIndex(wkid,name))

def _get_parent_workstation(plot_id):
  NhlGetParentWorkstation(_int_id(plot_id))

################################################################

def get_string(obj,name):
  """
Retrieves the value of a resource that uses a string.
str = Ngl.get_string(plotid, resource_name)
plotid -- The identifier returned from Ngl.open_wks, or any PyNGL
          function that returns a PlotId.
resource_name -- The name of the resource whose value you want to retrieve.
  """
  return(NhlGetString(_int_id(obj),name))

################################################################

def get_string_array(obj,name):
  """
Retrieves the value of a resource that uses a one-dimensional string
array.
sarr = Ngl.get_string_array(plotid, resource_name)
plotid -- The identifier returned from Ngl.open_wks, or any PyNGL
          function that returns a PlotId.
resource_name -- The name of the resource whose value you want to
                 retrieve.
  """
  return(NhlGetStringArray(_int_id(obj),name))

################################################################

def hlsrgb(h,l,s):
  """
Converts from the HLS color space to RGB.
r, g, b = Ngl.hlsrgb(h, l, s)
h -- Hue values in the range [0.,360.). A hue of "0." corresponds to
     blue.
l -- Lightness values in the range [0.,100.]. Lightness is a measure
     of the quantity of light - a lightness of 0. is black, and a
     lightness of 100. gives white. The pure hues occur at lightness
     value 50.
s -- Saturation values in the range [0.,100.]. Saturation is a measure
     of how much white light is mixed with the color. Colors having a
     saturation value of 0. represent grays with a gray intensity
     value equal to the lightness L. Colors with a saturation value of
     100. are fully saturated colors. The hue is undefined when
     S=0. The fully saturated pure hues occur when S=100. and L=50.
  """
  if (_is_scalar(h) and _is_scalar(l) and _is_scalar(s)):
    return(c_hlsrgb(h,l,s))
  elif (_is_numpy_array(h) and _is_numpy_array(l) and _is_numpy_array(s)):
    ishape = h.shape
    dimc = len(h.ravel())
    rr = numpy.zeros(dimc,'f')
    gr = numpy.zeros(dimc,'f')
    br = numpy.zeros(dimc,'f')
    for i in xrange(dimc):
      rr[i],gr[i],br[i] = c_hlsrgb(h.ravel()[i],l.ravel()[i],s.ravel()[i])
    rr.shape = gr.shape = br.shape = ishape
    del ishape,dimc
    return rr,gr,br
  elif ( _is_list_or_tuple(h) and _is_list_or_tuple(l) and \
         _is_list_or_tuple(s) ):
    hi = numpy.array(h,'f')
    li = numpy.array(l,'f')
    si = numpy.array(s,'f')
    ishape = hi.shape
    dimc = len(hi.ravel())
    rr = numpy.zeros(dimc,'f')
    gr = numpy.zeros(dimc,'f')
    br = numpy.zeros(dimc,'f')
    for i in xrange(dimc):
      rr[i], gr[i], br[i] = c_hlsrgb(hi.ravel()[i],li.ravel()[i],si.ravel()[i])
    rr.shape = gr.shape = br.shape = ishape
    del hi,li,si,ishape,dimc
    return rr,gr,br
  else:
    print ("hlsrgb: arguments must be scalars, arrays, lists or tuples.")

################################################################

def hsvrgb(h,s,v):
  """
Converts from the HSV color space to RGB.
r, g, b = Ngl.hsvrgb(h, s, v)
h -- Hue values in the range [0.,360.). A hue of 0. corresponds to
     red.
s -- Saturation values in the range [0.,1.]. Saturation is a measure
     of how much white light is mixed with the color. Saturation
     values of 0. represent grays (with a gray value equal to the
     value V). Saturation values of 1. are fully saturated colors. The
     hue is undefined when S=0. The fully saturated pure hues occur
     when S=1. and V=1.
v -- Values for the value component in the range [0.,1.].
  """
  if (_is_scalar(h) and _is_scalar(s) and _is_scalar(v)):
    return(c_hsvrgb(h,s,v))
  elif (_is_numpy_array(h) and _is_numpy_array(s) and _is_numpy_array(v)):
    ishape = h.shape
    dimc = len(h.ravel())
    rr = numpy.zeros(dimc,'f')
    gr = numpy.zeros(dimc,'f')
    br = numpy.zeros(dimc,'f')
    for i in xrange(dimc):
      rr[i],gr[i],br[i] = c_hsvrgb(h.ravel()[i],s.ravel()[i],v.ravel()[i])
    rr.shape = gr.shape = br.shape = ishape
    return rr,gr,br
  elif ( _is_list_or_tuple(h) and _is_list_or_tuple(s) and \
         _is_list_or_tuple(v) ):
    hi = numpy.array(h,'f')
    si = numpy.array(s,'f')
    vi = numpy.array(v,'f')
    ishape = hi.shape
    dimc = len(hi.ravel())
    rr = numpy.zeros(dimc,'f')
    gr = numpy.zeros(dimc,'f')
    br = numpy.zeros(dimc,'f')
    for j in xrange(dimc):
      rr[j],gr[j],br[j] = c_hsvrgb(hi.ravel()[j],si.ravel()[j],vi.ravel()[j])
    rr.shape = gr.shape = br.shape = ishape
    del hi,si,vi,dimc,ishape
    return rr,gr,br
  else:
    print ("hsvrgb: arguments must be scalars, arrays, lists or tuples.")

################################################################

#
#  Get indices of a list where the list values are true.
#
def ind(seq):
  """
Returns the integer indices of a Python list where the list values are true.
tindex = Ngl.ind(plist)
plist -- A Python list, tuple, or one-dimensional NumPy array.
  """
  inds = []
  for i in xrange(len(seq)):
    if (seq[i] != 0):
      inds.append(i)
  return(inds)

################################################################

def int2p(pin, xin, pout, linlog):
  """
Interpolates data on one set of pressure levels to a different set of
pressure levels.  The return array will be a multi-dimensional NumPy
array of the same shape as xin, but the rightmost dimension will have
the same size as the rightmost dimension of pout.  The return type
will be double if xinis double, float otherwise.
xout = Ngl.int2p(pin, xin, pout, linlog)
pin -- A NumPy array of any dimensionality containing input pressure
levels. If multi-dimensional, the level dimension must be in the
rightmost position and the values must be monotonically increasing or
decreasing.  
xin -- A NumPy array of any dimensionality containing the data to be
interpolated. If pin is multi-dimensional, then these two arrays have
the same dimension sizes.  
pout -- A Numpy array of any dimensionality containing output pressure
levels with values monotonically increasing or decreasing. If
multi-dimensional, the level dimension must be in the rightmost
dimension and all other dimensions must be the same as xin. If
one-dimensional, then all of xin will be interpolated to the same
levels. Must have the same units as pin. 
linlog -- A scalar integer indicating the type of interpolation:
abs(linlog) == 1 --> linear interpolation
abs(linlog) != 1 --> log interpolation
If linlog is negative, then extrapolation to levels outside the range
of pin will occur. Use extrapolation with caution.  
  """

# Convert arrays to numpy arrays with potential fill values
  xin2,fill_value_xin  = _get_arr_and_force_fv(xin)
  pin2,fill_value_pin  = _get_arr_and_force_fv(pin)
  pout2,fill_value_pin = _get_arr_and_fv(pout)

# Figure out what the output fill value should be
  if fill_value_xin is None:
    if fill_value_pin is None:
      fill_value = 1.e20
    else:
      fill_value = fill_value_pin
  else:
    fill_value = fill_value_xin
  
  aret = fplib.int2p(pin2, xin2, pout2, linlog, fill_value)
  return ma.masked_array(aret, fill_value=fill_value)


################################################################

def labelbar_ndc(wks,nbox,labels,x,y,rlistc=None):
  """
Creates and draws a labelbar anywhere in the viewport, and returns
a PlotId representing the labelbar created.
pid = Ngl.labelbar_ndc(wks, nboxes, labels, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
nboxes -- The number of labelbar boxes.
labels -- An array of label strings for the labelbar boxes.
x, y -- The NDC values (values from 0 to 1) defining the
        coordinates of the upper left corner of the labelbar.
res -- An optional instance of the Resources class having Labelbar
       resources as attributes.
  """
  _set_spc_defaults(0)
  rlist = _crt_dict(rlistc)
  rlist1 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist1[key] = rlist[key]

  _set_labelbar_res(rlist,rlist1,False) # Set some addtl labelbar resources

  ilb = labelbar_ndc_wrap(wks,nbox,labels,len(labels),x,y, 
                          "double","double",rlist1,pvoid())
  del rlist
  del rlist1

  return (_lst2pobj(ilb))

################################################################

def legend_ndc(wks,nitems,labels,x,y,rlistc=None):
  """
Draws a legend anywhere in the viewport, and returns a PlotId
representing the labelbar created.
pid = Ngl.legend_ndc(wks, nitems, labels, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
nitems -- The number of legend items.
labels -- An array of label strings for the legend.
x, y -- The NDC values (values from 0 to 1) defining the coordinates
         of the upper left corner of the legend.
res -- An optional instance of the Resources class having Labelbar
       resources as attributes.
  """
  _set_spc_defaults(0)
  rlist = _crt_dict(rlistc)
  rlist1 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist1[key] = rlist[key]

  _set_legend_res(rlist,rlist1)      # Set some addtl legend resources

  ilb = legend_ndc_wrap(wks,nitems,labels,len(labels),x,y, 
                        "double","double",rlist1,pvoid())
  del rlist
  del rlist1
  return (_lst2pobj(ilb))

################################################################

def linmsg(x, end_pts_msg=None, max_msg=None, fill_value=1.e20):
  """
Linearly interpolates to fill in missing values.
x = Ngl.linmsg(x,end_pts_msg=None,max_msg=None,fill_value=1.e20)
x -- A numpy or masked array of any dimensionality that contains missing values.
end_pts_msg -- how missing beginning and end points will be
               returned. If this value is greater than or equal to 0,
               then the beginning and end points will be returned as
               missing (default option). If this value is less
               than 0, then they will be set to the nearest
               non-missing value.
max_msg -- the maximum number of consecutive missing values to be
           interpolated. If not set, then this function will try 
           to interpolate as many values as it can.
fill_value -- The missing value for x. Defaults to 1.e20 if not set.
  """
#
#  Set defaults for input parameters not specified by user.
#
  if end_pts_msg is None:
    end_pts_msg = 0

#
# Setting max_msg to 0 will cause the C wrapper to set this to
# npts before going into the Fortran routine.
#
  if max_msg is None:
    max_msg = 0
#
#  If input array is a numpy masked array, return a numpy masked array.
#  Otherwise missing values are dealt with using the fill_value.
#
  fv = _get_fill_value(x)
  if (any(fv is None)):
    return fplib.linmsg(_promote_scalar(x),end_pts_msg,max_msg,fill_value)
  else:
    aret = fplib.linmsg(x.filled(fv), end_pts_msg, max_msg, fv)
    return ma.masked_array(aret, fill_value=fv)

################################################################

def map(wks,rlistc=None,res=None):
  """
Creates and draws a map, and returns a PlotId of the map plot created.
pid = Ngl.map(wks, res=None)
wks -- The identifier returned from calling Ngl.open_wks. 
res -- An optional instance of the Resources class having Map
       resources as attributes.
  """
  if not res is None:
    rlistc = res
  _set_spc_defaults(1)
  rlist = _crt_dict(rlistc)  
  rlist1 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist1[key] = rlist[key]

  _set_map_res(rlist,rlist1)           # Set some addtl map resources

# 
# Test for masking a lambert conformal plot.
#
  mask_list = _test_for_mask_lc(rlist,rlist1)

  imap  = map_wrap(wks,rlist1,pvoid())
  limap = _lst2pobj(imap)

  if mask_list["MaskLC"]:
    limap = _mask_lambert_conformal(wks, limap, mask_list, rlist1)

  del rlist
  del rlist1
  return(limap)

################################################################

def maximize_plot(wks,plot,rlistc=None):
  """
Maximizes the size of the given plot on the workstation.
Ngl.maximize_plot(wks, plotid, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
plotid -- The identifier returned from calling any graphics routine
          like Ngl.xy or Ngl.contour_map.
res -- An optional optional instance of the Resources class having
       PyNGL resources as attributes.
  """
  _set_spc_defaults(0)
  rlist = _crt_dict(rlistc)  
  rlist1 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist1[key] = rlist[key]
  maximize_plots(wks,_pobj2lst(plot),1,0,pvoid())

################################################################

def merge_colormaps(wks,cmap1,cmap2):
  """
Merges two color maps into one for the given workstation.
Ngl.merge_colormaps(wks,cmap1,cmap2)
wks -- The identifier returned from calling Ngl.open_wks.
cmap1 -- An n x 3 array of RGB triplets, or a predefined colormap name.
cmap2 -- A second n x 3 array of RGB triplets, or a predefined colormap name.
  """
#
# Retrieve original color map in case we need to reset it.
#
  orig_cmap = retrieve_colormap(wks)
# 
# Set and retrieve both color maps so we can then get the RGB triplets.
#
# For second color map, toss the first two colors (background/foreground).
#
  define_colormap(wks,cmap1)
  rgb_cmap1 = retrieve_colormap(wks)

  define_colormap(wks,cmap2)
  o_rgb_cmap2 = retrieve_colormap(wks)
  rgb_cmap2   = o_rgb_cmap2[2:,:]          # Drop colors 0 and 1.

  ncmap1 = rgb_cmap1.shape[0]              # Size of colormaps
  ncmap2 = rgb_cmap2.shape[0]

  if (ncmap1 + ncmap2) > 256:
    print ("merge_colormaps - Warning, the two color maps combined must have 256 or fewer colors.")
    print ("Keeping original color map.")
    define_colormap(wks,orig_cmap)
    return None

#
# Merge two colormaps into one.
#

  new_cmap = numpy.zeros((ncmap1+ncmap2,3),rgb_cmap1.dtype.char)
  new_cmap[:ncmap1,:] = rgb_cmap1
  new_cmap[ncmap1:,:] = rgb_cmap2
  
  define_colormap(wks,new_cmap)
  return None

################################################################

def natgrid(x,y,z,xo,yo):
  """
Uses a natural neighbor algorithm to interpolate 2-dimensional
randomly spaced data to a defined output grid.
xarray = Ngl.natgrid(x, y, z, xo, yo)
x, y -- One-dimensional arrays of the X and Y coordinate points of the
        input data.
z -- The one-dimensional input data to be interpolated, of the same
     length as x and y. Can be a NumPy float array or a Python list
     or tuple.
xo, yo -- One-dimensional NumPy float arrays or Python lists (of
          length numxout and numyout) containing the coordinate points
          of the output data grid.
  """
  if _is_list_or_tuple(x):
    dsizes_x = len(x)
  elif _is_numpy_array(x):
    dsizes_x = x.shape[0]
  else:
    print (\
     "natgrid: type of argument 1 must be one of: list, tuple, or NumPy array")
    return None

  if _is_list_or_tuple(xo):
    dsizes_xo = len(xo)
  elif _is_numpy_array(xo):
    dsizes_xo = xo.shape[0]
  else:
    print (\
     "natgrid: type of argument 4 must be one of: list, tuple, or NumPy array")
    return None

  if _is_list_or_tuple(yo):
    dsizes_yo = len(yo)
  elif _is_numpy_array(yo):
    dsizes_yo = yo.shape[0]
  else:
    print (\
     "natgrid: type of argument 5 must be one of: list, tuple, or NumPy array")
    return None

  ier,zo = \
     natgridc(dsizes_x,x,y,z,dsizes_xo,dsizes_yo,xo,yo,dsizes_xo,dsizes_yo)

  if (ier != 0):
    print ("natgrid: error number %d returned, see error table." % (ier))
    del ier
    return None
  else:
    return zo

def _ncargpath(type):
  return pynglpath(type)

################################################################

def new_color(wks_id,r,g,b):
  """
Adds the given color to the end of the color map of the given
workstation and returns the integer index of the 
the new color.
index = Ngl.new_color(wks, red, green, blue)
wks -- The identifier returned from calling Ngl.open_wks.
red, green, blue -- Floating point values between 0.0 and 1.0
                    inclusive.
  """
  return NhlNewColor(_int_id(wks_id),r,g,b)

################################################################

def ndctodata(obj,x,y):
  """
Converts coordinates in NDC space to coordinates in data space.
Missing values are ignored.
xdata,ydata = Ngl.ndctodata(plot,xndc,yndc)
plot -- The identifier returned from calling any plot object creation
        function, like Ngl.xy, Ngl.contour, Ngl.vector_map, etc.
xndc,yndc -- One dimensional (masked) arrays containing values to be
             converted.
  """

  x2,fvx = _get_arr_and_fv(x)
  y2,fvy = _get_arr_and_fv(y)

# Set flags indicating whether missing values present.
  fvx,ismx = _set_default_msg(fvx)
  fvy,ismy = _set_default_msg(fvy)


  error,xout,yout,status,range = \
     NhlPNDCToData(_int_id(obj),x2,y2,len(_promote_scalar(x2)),fvx,fvy,
                   ismx,ismy)

# Convert to masked array if input was masked array, or any of the
# values are outside the plot data space.
  if ismx or status == 1:
    xout = _convert_to_ma(xout,range)
  if ismy or status == 1:
    yout = _convert_to_ma(yout,range)

  del error,status,range
  return xout,yout

################################################################

def new_dash_pattern(wks_id,patterns):
  """
Adds a new dash pattern to the existing table of dash patterns, and
returns the integer index of the new pattern.
index = Ngl.new_dash_pattern(wks, dash_pattern)
wks -- The identifier returned from calling Ngl.open_wks.
dash_pattern -- A string indicating the dash pattern to create.  The
                dash pattern string can be any length, and should
                be generated using a combination of "$" and "_"
                characters. The "$" represents a pen-down, and the
                "_" represents a pen-up.
  """
  return NhlNewDashPattern(_int_id(wks_id),patterns)

################################################################

def new_marker(wks_id,marker_strings,font_nums,xoffset=0.,yoffset=0., \
               aspect_ratio=1., size=1., angle=0.):
  """
Adds a new marker to the existing table of markers and returns the
integer index of the new marker.
nmark = Ngl.new_marker(wks, marker_strings, font_nums, xoffset=0., yoffset=0., 
                       aspect_ratio=1., size=1., angle=0.)
wks -- The identifier returned from calling Ngl.open_wks.
marker_strings -- A single string (or list of strings) to indicate
                  what characters to pick from the font number (or
                  list of font numbers) in the font_nums argument
                  below. The strings will usually be a single
                  character, but that is not a requirement. For
                  example, you could create "Hello world" as a marker
                  (see Example 5).
                 
font_nums -- An integer scalar (or list of scalars, having the same
             length as the list of strings in the marker_strings
             argument) containing the font table numbers indicating
             which font table to use for the characters in the marker
             strings.
xoffset, yoffset -- Optional scalar arguments that are the X and Y
                    offsets of the marker. The units for these offsets
                    are character widths, that is, an x offset of
                    1. would move the marker a character width to the
                    right. In most cases these offsets are used for
                    only slight adjustments. The default value of 0.0
                    indicates no offset.
aspect_ratio -- An optional scalar that is the aspect ratio of the
                marker. A value greater than 1. stretches the marker
                in the vertical direction, and a value less than
                1. stretches it in the horizontal direction. The
                default of 1.0 produces a square aspect ratio. A value
                less than 0. will be set to the default.
size -- An optional scalar size multiplier for the default marker
        size. (a size less than 0. will default to 1.) A value of
        2. doubles the marker size, and value of 0.5 halves the marker
        size. The default is 1.0. A size less than 0. will be set to
        the default.
angle -- An optional scalar that is the angle at which to rotate the
         marker counter-clockwise; it must be greater than or equal to
         0. The default of 0.0 produces no rotation.
  """
  return NhlNewMarker(_int_id(wks_id),marker_strings, \
               font_nums,float(xoffset),float(yoffset), \
               float(aspect_ratio), float(size), float(angle))

################################################################

def set_color(wks_id,index,r,g,b):
  """
Sets a color in the color map of the given workstation.
Ngl.set_color(wks, index, red, green, blue)
wks -- The identifier returned from calling Ngl.open_wks.
index -- The index value in the color map of which to replace with the
         given color.
red, green, blue -- Floating point values between 0.0 and 1.0 inclusive.
  """
  NhlSetColor(_int_id(wks_id),index,r,g,b)
  return None

################################################################

def free_color(wks_id,index):
  """
Removes a color entry from a workstation.
Ngl.free_color(workstation, color_index)
workstation -- An identifier returned from calling Ngl.open_wks.
color_index -- An integer scalar specifying a color index.
  """
  NhlFreeColor(_int_id(wks_id),index)
  return None

################################################################

def nngetp(pname):
  """
Retrieves control parameter values for Ngl.natgrid.
pvalue = Ngl.nngetp(pname)
pname -- Name of the parameter whose value you want to retrieve.
  """
  iparms = [                                                         \
            "adf", "asc", "dup", "ext", "igr", "non", "rad",         \
            "sdi", "upd", "mdm",                                     \
            "ADF", "ASC", "DUP", "EXT", "IGR", "NON", "RAD",         \
            "SDI", "UPD", "MDM"                                      \
           ]
  rparms = [                                                         \
            "bI", "bJ", "hor", "magx", "magy", "magz", "nul", "ver", \
            "Bi", "Bj", "HOR", "MAGX", "MAGY", "MAGZ", "NUL", "VER", \
            "bi", "bj", "BI", "BJ"                                   \
           ]
  cparms = [                                                         \
            "alg", "ALG", "erf", "ERF"                                \
           ]
  if (not isinstance(pname,types.StringType)):
    print ("nngetp: Parameter '" + str(pname) + "' is not a string type." )
    return None
  if (iparms.count(pname) > 0):
    return c_nngeti(pname)
  elif (rparms.count(pname) > 0):
    return c_nngetrd(pname)
  elif (cparms.count(pname) > 0):
    return c_nngetcp(pname)
  else:
    print (\
      "nngetp: specified value for " + pname + " is not of a recognized type.")
  return None

################################################################

def nnsetp(pname,val):
  """
Sets control parameter values for Ngl.natgrid.
Ngl.nnsetp(pname, pvalue)
pname -- Name of the parameter whose value you want to retrieve.
pvalue -- Value of the parameter you want to set.
  """
  if (not isinstance(pname,types.StringType)):
    print ("nnsetp: Parameter '" + str(pname) + "' is not a string type." )
    return None
  if (isinstance(val,types.IntType)):
    c_nnseti(pname,val)
  elif (isinstance(val,types.FloatType)): 
    c_nnsetrd(pname,val)
  elif (isinstance(val,types.StringType)):
    c_nnsetc(pname,val)
  else:
    print (\
      "nnsetp: specified value for " + pname + " is not of a recognized type.")
  return None

################################################################

def normalize_angle(ang,type):
  """
Normalizes any angle in degrees to be in the interval [0.,360.) or
[-180.,180.).
nangle = Ngl.normalize_angle(angle, option)
angle -- An angle in degrees.
option -- An option flag that is either zero or non-zero.
  """
#
#  This function normalizes the angle (assumed to be in degrees) to
#  an equivalent angle in the range [0.,360.) if type equals 0, or
#  to an equivalent angle in the range [-180.,180.) if type is not zero.
#
  bang = ang
  if (type == 0):
    while(bang < 0.):
      bang = bang + 360.
    while(bang >= 360.):
      bang = bang - 360.
  else:
    while(bang < -180.):
      bang = bang + 360.
    while(bang >= 180.):
      bang = bang - 360.
  return bang

################################################################

def open_wks(wk_type,wk_name,wk_rlist=None):
  """
Opens a workstation on which to draw graphics, and returns a PlotID
representing the workstation created.
wks = Ngl.open_wks(type, name, res=None)
type -- The type of workstation to open. Some valids types include
        "ps", "eps", "pdf", "ncgm", and "X11".
name -- The name of the workstation.
res -- An optional instance of the Resources class having Workstation
       resources as attributes.
  """
#
  _set_spc_defaults(1)
  global first_call_to_open_wks
  rlist = _crt_dict(wk_rlist)

#
# Divide out "app" and other resources.
# 
  rlist1 = {}
  rlist2 = {}

  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:3] == "app"):
      rlist2[key] = rlist[key]
    elif(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist1[key] = rlist[key]

# 
#  Initialize the special resource values, and make sure 
#  NCARG_NCARG environment variable is set.
#
  if (first_call_to_open_wks == 0):

#
#  Set HLU environment variables.
#
    os.environ["NCARG_NCARG"] = _pynglpath_ncarg()

    tmp_dir = os.environ.get("TMPDIR")
    if (not tmp_dir is None) and os.path.exists(tmp_dir):
      os.environ["TMPDIR"] = tmp_dir
    else:
      os.environ["TMPDIR"] = "/tmp"

    color_dir_envn = os.environ.get("PYNGL_COLORMAPS")
    if (not color_dir_envn is None) and os.path.exists(color_dir_envn):
      os.environ["NCARG_COLORMAPS"] = color_dir_envn

    grib2_dir_envn = os.environ.get("NIO_GRIB2_CODETABLES")
    if (not grib2_dir_envn is None) and os.path.exists(grib2_dir_envn):
      os.environ["NIO_GRIB2_CODETABLES"] = grib2_dir_envn

#
#  If "PYNGL_RANGS" is set, use it.  Otherwise set 
#  the default RANGS directory.
#
    rangs_dir_envn = os.environ.get("PYNGL_RANGS")
    if (not rangs_dir_envn is None) and os.path.exists(rangs_dir_envn):
#
#  Check if the high-res file are there - if not issue a
#  an information message to that effect.
#
      _ck_for_rangs(rangs_dir_envn)
      os.environ["NCARG_RANGS"] = rangs_dir_envn
    else:
      os.environ["NCARG_RANGS"] = _pynglpath_ncarg() + "/rangs"

    ures_dir_envn = os.environ.get("PYNGL_USRRESFILE")
    if (not ures_dir_envn is None) and os.path.exists(ures_dir_envn):
      os.environ["NCARG_USRRESFILE"] = ures_dir_envn
    else:
      os.environ["NCARG_USRRESFILE"] = "~/.hluresfile"

    sres_dir_envn = os.environ.get("PYNGL_SYSRESFILE")
    if (not sres_dir_envn is None) and os.path.exists(sres_dir_envn):
      os.environ["NCARG_SYSRESFILE"] = sres_dir_envn

    ares_dir_envn = os.environ.get("PYNGL_SYSAPPRES")
    if (not ares_dir_envn is None) and os.path.exists(ares_dir_envn):
      os.environ["NCARG_SYSAPPRES"] = ares_dir_envn
    else:
      os.environ["NCARG_SYSAPPRES"] = _pynglpath_ncarg() + "/sysappres"

    first_call_to_open_wks = first_call_to_open_wks + 1

#
#  Lists of triplets for color tables must be numpy arrays.
#
  if (rlist.has_key("wkColorMap")):
#
#  Type of the elements of the color map must be array and not list.
#
    if type(rlist["wkColorMap"][0]) == type([0]):
      print ("opn_wks: lists of triplets for color tables must be NumPy arrays")
      return None

#
#  Call the wrapped function and return.
#
  iopn = open_wks_wrap(wk_type,wk_name,rlist1,rlist2,pvoid())
  del rlist
  del rlist1
  del rlist2
  return(iopn)

################################################################

def overlay(plot_id1,plot_id2):
  """
Overlays one plot onto another.
Ngl.overlay(PlotId_base, PlotId_overlay)
PlotId_base -- The id of the plot on which you want to overlay
               PlotId_overlay.
PlotId_overlay -- The id of the plot you want to overlay on
                  PlotId_base.
  """
  NhlAddOverlay(_int_id(plot_id1),_int_id(plot_id2),-1)

################################################################

def panel(wks,plots,dims,rlistc=None):
  """
Draws multiple plots on a single frame.  Each plot must be the same
size in order for this procedure to work correctly.
Ngl.panel(wks, plots, dims, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
plots -- An array of plot identifiers, each one created by calling any
         of the graphics routines like Ngl.xy or Ngl.contour_map.
dims -- An array of integers indicating the configuration of the plots
        on the frame. dims can either be two integers representing the
        number of rows and columns of the paneled lots, or a list of
        integers representing the number of plots per row.
 
res -- An optional instance of the Resources class having PyNGL
       resources as attributes.
  """
  _set_spc_defaults(1)
  rlist = _crt_dict(rlistc)  
  rlist1 = {}
  rlist2 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:3] == "ngl"):
      if (len(key) == 21 and key[0:21] == "nglPanelFigureStrings"):
        _set_spc_res(key[3:],rlist[key])
        _set_spc_res("PanelFigureStringsCount",len(rlist[key]))
      elif (key[0:25] == "nglPanelFigureStringsJust"):
        if(_check_res_value(rlist[key],"TopLeft",0)):
          _set_spc_res(key[3:],0)
        elif(_check_res_value(rlist[key],"CenterLeft",1)): 
          _set_spc_res(key[3:],1)
        elif(_check_res_value(rlist[key],"BottomLeft",2)): 
          _set_spc_res(key[3:],2)
        elif(_check_res_value(rlist[key],"TopCenter",3)): 
          _set_spc_res(key[3:],3)
        elif(_check_res_value(rlist[key],"CenterCenter",4)): 
          _set_spc_res(key[3:],4)
        elif(_check_res_value(rlist[key],"BottomCenter",5)): 
          _set_spc_res(key[3:],5)
        elif(_check_res_value(rlist[key],"TopRight",6)):
          _set_spc_res(key[3:],6)
        elif(_check_res_value(rlist[key],"CenterRight",7)): 
          _set_spc_res(key[3:],7)
        elif(_check_res_value(rlist[key],"BottomRight",8)): 
          _set_spc_res(key[3:],8)
      else:
        _set_spc_res(key[3:],rlist[key])
    elif (key[0:2] == "lb"):
      if (key == "lbLabelAlignment"):
        if (_check_res_value(rlist[key],"BoxCenters",0)):
          _set_spc_res("PanelLabelBarAlignment",0)
        elif (_check_res_value(rlist[key],"InteriorEdges",1)):
          _set_spc_res("PanelLabelBarAlignment",1)
        elif (_check_res_value(rlist[key],"ExternalEdges",2)):
          _set_spc_res("PanelLabelBarAlignment",2)
        else:
          _set_spc_res("PanelLabelBarAlignment",rlist[key])
      elif (key == "lbPerimOn"):
        if (rlist[key] == 1):
          _set_spc_res("PanelLabelBarPerimOn",1)
        elif (rlist[key] == 0):
          _set_spc_res("PanelLabelBarPerimOn",0)
        else:
          _set_spc_res("PanelLabelBarPerimOn",rlist[key])
      elif (key == "lbLabelAutoStride"):
        if (rlist[key] == 1):
          _set_spc_res("PanelLabelBarAutoStride",1)
        elif (rlist[key] == 0):
          _set_spc_res("PanelLabelBarAutoStride",0)
        else:
          _set_spc_res("PanelLabelBarAutoStride",rlist[key])
      elif (key == "lbLabelFontHeightF"):
        _set_spc_res("PanelLabelBarFontHeightF",rlist[key])
      elif (key == "lbOrientation"):
        if (_check_res_value(rlist[key],"Vertical",1)):
          _set_spc_res("PanelLabelBarOrientation",1)
        elif (_check_res_value(rlist[key],"Horizontal",0)):
          _set_spc_res("PanelLabelBarOrientation",0)
        else:
          _set_spc_res("PanelLabelBarOrientation",rlist[key])
        

      rlist1[key] = rlist[key]
  panel_wrap(wks,_pseq2lst(plots),len(plots),dims,len(dims),rlist1,rlist2,pvoid())
  del rlist
  del rlist1

################################################################

def polygon(wks,plot,x,y,rlistc=None):
  """
Draws a filled polygon on an existing plot.
Ngl.polygon(wks, plot, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
plot -- The id of the plot on which you want to draw the polygon
x, y -- One-dimensional (masked) NumPy arrays or Python lists containing
        the x, y coordinates of the polygon, which must be in the same 
        coordinate space as the plot.
res -- An optional instance of the Resources class having
       GraphicStyle resources as attributes.
  """

  return(_poly(wks,plot,x,y,NhlPOLYGON,0,rlistc))

################################################################

def polygon_ndc(wks,x,y,rlistc=None):
  """
Draws a filled polygon on the viewport.
Ngl.polygon_ndc(wks, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
x, y -- One-dimensional (masked) NumPy arrays or Python lists containing
        the x, y NDC coordinates (values from 0 to 1) of the polygon.
res -- An optional instance of the Resources class having
       GraphicStyle resources as attributes.
  """
  return(_poly(wks,0,x,y,NhlPOLYGON,1,rlistc))

################################################################

def polyline(wks,plot,x,y,rlistc=None):
  """
Draw polylines on an existing plot.
Ngl.polyline(wks, plot, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
plot -- The id of the plot on which you want to draw the polylines.
x, y -- One-dimensional (masked) NumPy arrays or Python lists containing
        the x, y coordinates of the polylines, which must be in the same 
        coordinate space as the plot.
res -- An optional instance of the Resources class having
       GraphicStyle resources as attributes.
  """
  return(_poly(wks,plot,x,y,NhlPOLYLINE,0,rlistc))

################################################################

def polyline_ndc(wks,x,y,rlistc=None):
  """
Draws polylines on the viewport.
Ngl.polyline_ndc(wks, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
x, y -- One-dimensional (masked) NumPy arrays or Python lists containing
        the x, y NDC coordinates (values from 0 to 1) of the polylines.
res -- An optional instance of the Resources class having
       GraphicStyle resources as attributes.
  """
  return(_poly(wks,0,x,y,NhlPOLYLINE,1,rlistc))

################################################################

def polymarker(wks,plot,x,y,rlistc=None):  # plot converted in poly
  """
Draw polymarkers on an existing plot.
Ngl.polymarker(wks, plot, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
plot -- The id of the plot on which you want to draw the polymarkers.
x, y -- One-dimensional (masked) NumPy arrays or Python lists containing
        the x, y coordinates of the polymarkers, which must be in the same 
        coordinate space as the plot.
res -- An optional instance of the Resources class having
       GraphicStyle resources as attributes.
  """
  return(_poly(wks,plot,x,y,NhlPOLYMARKER,0,rlistc))

################################################################

def polymarker_ndc(wks,x,y,rlistc=None):
  """
Draws polymarkers on the viewport.
Ngl.polymarker_ndc(wks, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
x, y -- One-dimensional (masked) NumPy arrays or Python lists containing
        the x, y NDC coordinates (values from 0 to 1) of the polymarkers.
res -- An optional instance of the Resources class having
       GraphicStyle resources as attributes.
  """
  return(_poly(wks,0,x,y,NhlPOLYMARKER,1,rlistc))

################################################################

def pynglpath(name):
  """
Returns the full path names of various installed PyNGL components.
pname = Ngl.pynglpath(name)
name -- A string representing abbreviated name for which you want a
        directory path returned.
  """
#
#  Return absolute pathnames for various directories.
#
  if (name == "tmp"):
    tmp_dir = os.environ.get("TMPDIR")
    if (not tmp_dir is None) and os.path.exists(tmp_dir):
      return tmp_dir
    else:
      return "/tmp"
  elif (name == "examples"):
    examples_dir_envn = os.environ.get("PYNGL_EXAMPLES")
#
# Create the path to the pynglex examples.
#
    examples_dir_dflt = os.path.join(_pynglpath_ncarg(),"pynglex")

    if (not examples_dir_envn is None) and os.path.exists(examples_dir_envn):
      return examples_dir_envn
    elif (os.path.exists(examples_dir_dflt)):
      return examples_dir_dflt
    else:
      print ("pynglpath: examples directory does not exist.")
      return None
  elif (name == "data"):
    data_dir_envn = os.environ.get("PYNGL_DATA")
    data_dir_dflt = os.path.join(_pynglpath_ncarg(),"data")
    if (not data_dir_envn is None) and os.path.exists(data_dir_envn):
      return data_dir_envn
    elif (os.path.exists(data_dir_dflt)):
      return data_dir_dflt
    else:
      print ("pynglpath: data directory does not exist.")
      return None
  elif (name == "colormaps"):
    color_dir_envn = os.environ.get("PYNGL_COLORMAPS")
    color_dir_dflt = os.path.join(_pynglpath_ncarg(),"colormaps")
    if (not color_dir_envn is None) and os.path.exists(color_dir_envn):
      return color_dir_envn
    elif (os.path.exists(color_dir_dflt)):
      return color_dir_dflt
    else:
      print ("pynglpath: colormaps directory does not exist.")
      return None
  elif (name == "rangs"):
    rangs_dir_envn = os.environ.get("PYNGL_RANGS")
    rangs_dir_dflt = os.path.join(_pynglpath_ncarg(),"rangs")
    if (not rangs_dir_envn is None) and os.path.exists(rangs_dir_envn):
      return rangs_dir_envn
    else: 
      return rangs_dir_dflt
  elif (name == "grib2_codetables"):
    print ("name",name)
    grib2_dir_envn = os.environ.get("NIO_GRIB2_CODETABLES")
    grib2_dir_dflt = os.path.join(_pynglpath_ncarg(),"grib2_codetables")
    if (not grib2_dir_envn is None) and os.path.exists(grib2_dir_envn):
      return grib2_dir_envn
    else: 
      return grib2_dir_dflt
  elif (name == "usrresfile"):
    ures_dir_envn = os.environ.get("PYNGL_USRRESFILE")
    ures_dir_dflt = commands.getoutput("ls ~/.hluresfile")
    if (not ures_dir_envn is None) and os.path.exists(ures_dir_envn):
      return ures_dir_envn
    elif (os.path.exists(ures_dir_dflt)):
      return ures_dir_dflt
    else:
      print ("pynglpath: useresfile directory does not exist.")
      return None
  elif (name == "sysresfile"):
    sres_dir_envn = os.environ.get("PYNGL_SYSRESFILE")
    sres_dir_dflt = os.path.join(_pynglpath_ncarg(),"sysresfile")
    if (not sres_dir_envn is None) and os.path.exists(sres_dir_envn):
      return sres_dir_envn
    elif (os.path.exists(sres_dir_dflt)):
      return sres_dir_dflt
    else:
      print ("pynglpath: sysresfile directory does not exist.")
      return None
  elif (name == "sysappres"):
    ares_dir_envn = os.environ.get("PYNGL_SYSAPPRES")
    ares_dir_dflt = os.path.join(_pynglpath_ncarg(),"sysappres")
    if (not ares_dir_envn is None) and os.path.exists(ares_dir_envn):
      return ares_dir_envn
    elif (os.path.exists(ares_dir_dflt)):
      return ares_dir_dflt
    else:
      print ("pynglpath: sysappres directory does not exist.")
      return None
  elif (name == "ncarg"):
    return _pynglpath_ncarg()
  else:
    print ('pynglpath: input name "%s" not recognized' % (name))

################################################################

def read_colormap_file(colormap_name):
  """
This function either reads a PyNGL-standard colormap, given its name,
or expects to read a colormap from a given file.  It supports reading
either RGB-tuples or RGBA-tuples (or a mixture).
It always returns a colormap comprised of RGBA-tuples [N,4]
cmap = Ngl.read_colormap_file (colormap_name)
colormap_name -- Either the name of a PyNGL-standard colormap, or the
                 filename of a user-supplied colormap.
  """
# This function was taken from the NCL version written by R.Brownrigg.

  MAXCOLORS = 256     # symbolic constant, used below

  # ----------------------------------------------------------
  # Inner convenience function to test string as suitable for 
  # conversion to numeric.
  def isNumerical(s):
    try:
      float(s)
      return True
    except ValueError:
      return False

  # ------------------------------------------------------------
  # Inner convenience function to find appropriate pathname for 
  # the given filename.
  def _get_cmap_file_path(colormap_name):
    # Is this one of our standard named colormaps? There are several well-defined
    # locations and suffixes to try...
    tmp = os.getenv("NCARG_COLORMAPS")
    if not tmp is None:
        paths = tmp.split(":")
    else:
        paths = [os.path.join(pynglpath("ncarg"),"colormaps")]

    suffixes = [ ".rgb", ".gp", ".ncmap" ]

    # loop over the product of possible paths and possible suffixes...
    for path in paths:
        path1 = os.path.join(path,colormap_name)
        for suffix in suffixes:
            path2 = path1+suffix
            if(os.path.exists(path2)):
              return path2

    # if still here, just return colormap_name literally; presumably is a 
    # filename for a user-managed colormap...
    return colormap_name

  # get an appropriate pathname for the given colortable name and load it..
  pathname = _get_cmap_file_path(colormap_name)
  f = open(pathname)
  lines = f.readlines()

  # parse up to MAXCOLORS rgba tuples from the file just read...
  tmpCmap   = numpy.zeros((MAXCOLORS,4),'f')
  numColors = 0
  maxValue  = -1.0
  i = 0
  while (i < len(lines) and numColors < MAXCOLORS):
      if (len(lines[i]) == 0):
          lines[i] = "#"  # zero-lengthed lines cause us grief...
      lines[i].strip()
      tokens = lines[i].split()
      if (len(tokens) >= 3):
          red   = -1.0
          green = -1.0
          blue  = -1.0
          if (isNumerical(tokens[0])):
              red = float(tokens[0])
          if (isNumerical(tokens[1])):
              green = float(tokens[1])
          if (isNumerical(tokens[2])):
              blue = float(tokens[2])
          if (len(tokens) > 3 and isNumerical(tokens[3])):
              alpha = float(tokens[3])
          else:
              alpha = -1.0  # used a marker, replaced appropriately below...

          # were we able to get a rgba-tuple?
          #
          if (red >= 0 and green >= 0 and blue >= 0):
              # yes, add it to our colormap...
              tmpCmap[numColors,0] = red
              tmpCmap[numColors,1] = green
              tmpCmap[numColors,2] = blue
              tmpCmap[numColors,3] = alpha
              numColors = numColors + 1
              # keep track of the magnitude of these values; used to rescale below...
              if (red > maxValue):
                  maxValue = red
              if (green > maxValue):
                  maxValue = green
              if (blue > maxValue):
                  maxValue = blue
      i = i + 1

  # copy tmpCmap into appropriately sized array
  cmap = numpy.zeros([numColors, 4],'f')
  cmap = tmpCmap[0:numColors,:]

  # normalize the values
  # this logical taken directly from HLU code in "Palette.c"
  if (maxValue <= 1):
      cmap[:,3] = numpy.where(cmap[:,3] < 0, 1., cmap[:,3])
  elif (maxValue < 256):
      cmap[:,3] = numpy.where(cmap[:,3] < 0, 255., cmap[:,3])
      cmap = cmap / 255.
  elif (maxValue == 256):
      cmap[:,3] = numpy.where(cmap[:,3] < 0, 256., cmap[:,3])
      cmap = cmap / 256.
  elif (maxValue == 65536):
      cmap[:,3] = numpy.where(cmap[:,3] < 0, 65535., cmap[:,3])
      cmap = cmap / 65535. 
  elif (maxValue == 65536):
      cmap[:,3] = numpy.where(cmap[:,3] < 0, 65536., cmap[:,3])
      cmap = cmap / 65536.
  else:
      cmap[:,3] = numpy.where(cmap[:,3] < 0, maxValue, cmap[:,3])
      cmap = cmap / maxValue
  return cmap

################################################################

def regline(x, y, return_info=True):
  """
Calculates the linear regression coefficient between two series, and
returns a masked array with the same fill_value as y. If no missing
values are specified (via a masked array), then 1e20 is assumed.
rc = Ngl.regline (x,y)
x,y -- One-dimensional numpy or masked arrays of the same length.
return_info -- An optional logical that indicates whether additional
               calculations should be returned in a list:
               xave -- average of x
               yave -- average of y
               tval -- t-statistic (assuming null-hypothesis)
               rstd  -- standard error of the regression coefficient
               yintercept  -- y-intercept at x=0
               nptxy  -- number of points used
  """

# Deal with masked arrays.
  x2,fill_value_x = _get_arr_and_force_fv(x)
  y2,fill_value_y = _get_arr_and_force_fv(y)

  result = fplib.regline(x2, y2, fill_value_x, fill_value_y, return_info)

  del x2,fill_value_x
  del y2
# 
#  Return a masked array with y's fill value as the fill_value.
#  Return the additional calculated values if desired.
# 
  if not result is None:
    if HAS_MA:
      if (return_info == True): 
        return [ma.masked_array(result[0]),result[1]]
      else:
        return ma.masked_array(result[0],fill_value=fill_value_y)
    else:
      if (return_info == True): 
        return [result[0],result[1]]
      else:
        return result[0]

################################################################

def remove_annotation(plot_id1,plot_id2):
  """
Removes an annotation from the given plot.
Ngl.remove_annotation(PlotId_base, annotation_id)
PlotId_base -- The id of the plot from which you want to remove the
               annotation.
annotation_id -- The id of the annotation which was attached to
                 PlotId_base via call to Ngl.add_annotation.
  """
  NhlRemoveAnnotation(_int_id(plot_id1),_int_id(plot_id2))

################################################################

def remove_overlay(plot_id1,plot_id2,restore=False):
  """
Removes an overlaid plot from the given plot.
Ngl.remove_overlay(PlotId_base, PlotId_overlay, restore=False)
PlotId_base -- The id of the plot from which you want to remove the
               overlay.
PlotId_overlay -- The id of the plot which was overlaid on PlotId_base.
restore -- An optional logical value. If True and the member plot
           initially was a base plot of an overlay with its own
           members, the member plots are returned to the plot being
           removed.
  """
  NhlRemoveOverlay(_int_id(plot_id1),_int_id(plot_id2),restore)

################################################################

def retrieve_colormap(wks):
  """
Retrieves the current color map associated with the given workstation
and returns a 2-dimensional NumPy array of RGB values.
cmap = Ngl.retrieve_colormap(wks)
wks -- The identifier returned from calling Ngl.open_wks.
  """
  return get_MDfloat_array(wks,"wkColorMap")

################################################################

def rgbhls(r,g,b):
  """
Converts from the RGB color space to HLS.
h, l, s = Ngl.rgbhls(r, g, b)
r, g, b -- Intensity values for red, green, and blue in the range
           [0.1.].
Return Values
h -- The hue of the input point in HLS color space, in the range
     [0.,360.). A value of (0.,0.,1.) in the input space will result
     in a hue of 0. in the output space.
l -- The lightness value of the input point in HLS color space in the
     range [0.,100.]. Lightness is a measure of the quantity of light
     - a lightness of 0. is black, and a lightness of 100. is
     white. The pure hues occur at lightness value 50.
s -- The saturation value of the input point in HLS color space in the
     range [0.,100.]. Saturation is a measure of how much white light
     is mixed with the color. Saturation values of 0. represent grays
     (with a gray value equal to the lightness value L). Saturation
     values of 100. are fully saturated colors. The hue is undefined
     when S=0. The fully saturated pure hues occur when S=100. and
     L=50. The saturation value should be thought of as a percentage.
  """
  if (_is_scalar(r) and _is_scalar(g) and _is_scalar(b)):
    return(c_rgbhls(r,g,b))
  elif (_is_numpy_array(r) and _is_numpy_array(g) and _is_numpy_array(b)):
    ishape = r.shape
    dimc = len(r.ravel())
    hr = numpy.zeros(dimc,'f')
    lr = numpy.zeros(dimc,'f')
    sr = numpy.zeros(dimc,'f')
    for i in xrange(dimc):
      hr[i],lr[i],sr[i] = c_rgbhls(r.ravel()[i],g.ravel()[i],b.ravel()[i])
    hr.shape = lr.shape = sr.shape = ishape
    del dimc,ishape
    return hr,lr,sr
  elif ( _is_list_or_tuple(r) and _is_list_or_tuple(g) and \
         _is_list_or_tuple(b) ):
    ri = numpy.array(r,'f')
    gi = numpy.array(g,'f')
    bi = numpy.array(b,'f')
    ishape = ri.shape
    dimc = len(ri.ravel())
    hr = numpy.zeros(dimc,'f')
    lr = numpy.zeros(dimc,'f')
    sr = numpy.zeros(dimc,'f')
    for i in xrange(dimc):
      hr[i], lr[i], sr[i] = c_rgbhls(ri.ravel()[i],gi.ravel()[i],bi.ravel()[i])
    hr.shape = lr.shape = sr.shape = ishape
    del ri,gi,bi,dimc,ishape
    return hr,lr,sr
  else:
    print ("rgbhls: arguments must be scalars, arrays, lists or tuples.")


################################################################

def rgbhsv(r,g,b):
  """
Converts from the RGB color space to HSV.
h, s, v = Ngl.rgbhsv(r, g, b)
r, g, b -- Intensity values for red, green, and blue in the range
           [0.1.].
Return values
h -- Represents the hue of the input point in HSV color space. A value
     of (R,0.,0.) in the input space will result in a hue of 0. in the
     output space.
s -- The saturation value of the input point in HSV color space, in
     the range [0.,1.]. Saturation is a measure of how much white
     light is mixed with the color. Saturation values of 0. represent
     grays (with a gray value equal to V). Saturation values of 1. are
     fully saturated colors. The hue is technically undefined when
     S=0.; the code leaves H at its previous value when
     S=0. (0. initially). The fully saturated pure hues occur when
     S=1. and V=1.
v -- The value in HSV space, in the range [0.,1.].
  """
  if (_is_scalar(r) and _is_scalar(g) and _is_scalar(b)):
    return(c_rgbhsv(r,g,b))
  if (_is_numpy_array(r) and _is_numpy_array(g) and _is_numpy_array(b)):
    ishape = r.shape
    dimc = len(r.ravel())
    hr = numpy.zeros(dimc,'f')
    sr = numpy.zeros(dimc,'f')
    vr = numpy.zeros(dimc,'f')
    for i in xrange(dimc):
      hr[i],sr[i],vr[i] = c_rgbhsv(r.ravel()[i],g.ravel()[i],b.ravel()[i])
    hr.shape = sr.shape = vr.shape = ishape
    del ishape,dimc
    return hr,sr,vr
  elif ( _is_list_or_tuple(r) and _is_list_or_tuple(g) and \
         _is_list_or_tuple(b) ):
    ri = numpy.array(r,'f')
    gi = numpy.array(g,'f')
    bi = numpy.array(b,'f')
    ishape = ri.shape
    dimc = len(ri.ravel())
    hr = numpy.zeros(dimc,'f')
    sr = numpy.zeros(dimc,'f')
    vr = numpy.zeros(dimc,'f')
    for j in xrange(dimc):
      hr[j], sr[j], vr[j] = c_rgbhsv(ri.ravel()[j],gi.ravel()[j],bi.ravel()[j])
    hr.shape = sr.shape = vr.shape = ishape
    del ri,gi,bi,ishape,dimc
    return hr,sr,vr
  else:
    print ("rgbhsv: arguments must be scalars, arrays, lists or tuples.")

################################################################

def rgbyiq(r,g,b):
  """
Converts from the RGB color space to YIQ.
y, i, q = Ngl.rgbyiq(r, g, b)
r, g, b -- Intensity values for red, green, blue in the range [0.1.].
Return values
y -- Y component (luminance) values in the range [0.,1.].
i -- I component (chrominance orange-blue) values in the range [-0.6,
     0.6].
q -- Q component (chrominance purple-green) values in the range
     [-0.52, 0.52].
  """
#
#  Check if input is a NumPy array, scalar, list, or tuple.
#
  if (_is_scalar(r) and _is_scalar(g) and _is_scalar(b)):
    return(c_rgbyiq(r,g,b))
  elif (_is_numpy_array(r) and _is_numpy_array(g) and _is_numpy_array(b)):
    ishape = r.shape
    dimc = len(r.ravel())
    yr = numpy.zeros(dimc,'f')
    ir = numpy.zeros(dimc,'f')
    qr = numpy.zeros(dimc,'f')
    for i in xrange(dimc):
      yr[i],ir[i],qr[i] = c_rgbyiq(r.ravel()[i],g.ravel()[i],b.ravel()[i])
    yr.shape = ir.shape = qr.shape = ishape
    del ishape,dimc
    return yr,ir,qr
  elif ( _is_list_or_tuple(r) and _is_list_or_tuple(g) and \
         _is_list_or_tuple(b) ):
    ri = numpy.array(r,'f')
    gi = numpy.array(g,'f')
    bi = numpy.array(b,'f')
    ishape = ri.shape
    dimc = len(ri.ravel())
    yr = numpy.zeros(dimc,'f')
    ir = numpy.zeros(dimc,'f')
    qr = numpy.zeros(dimc,'f')
    for i in xrange(dimc):
      yr[i], ir[i], qr[i] = c_rgbyiq(ri.ravel[i],gi.ravel[i],bi.ravel[i])
    yr.shape = ir.shape = qr.shape = ishape
    del ri,gi,bi,ishape,dimc
    return yr,ir,qr
  else:
    print ("rgbyiq: arguments must be scalars, arrays, lists or tuples.")

################################################################

def set_values(obj,rlistc):
  """
Sets resource values for a specified plot object.
ier = Ngl.set_values(plotid, res)
plotid -- The identifier returned from calling any object creation
          function, like Ngl.xy, Ngl.contour_map, or Ngl.open_wks.
res -- An optional instance of the Resources class having PyNGL
       resources as attributes containing the resources you want to
set.
  """
  rlist = _crt_dict(rlistc)
  values = NhlSetValues(_int_id(obj),rlist)
  del rlist
  return values


################################################################

def skewt_bkg(wks, Opts):
  """
Creates a background chart for Skew T, Log P plotting.
sbkg = Ngl.skewt_bkg(wks, res)
wks -- The identifier returned from calling Ngl.open_wks.
res -- A required instance of the Resources class having special
       "skt" resources as attributes.
  """
#
#  This program generates a skew-t, log p thermodynamic diagram.  
#  This program was derived to reproduce the USAF skew-t, log p diagram
#  (form dod-wpc 9-16-1  current as of march 1978).
#
#  wks is a workstation identifier and Opts is an NGL resource list.
#
#  Based on Fortran code supplied by Tom Schlatter and 
#  Joe Wakefield [NOAA/PROFS] supplied fortran codes.
#
#  history
#  -------
#  don baker      01 jul 85    original version.  [NOAA/PROFS]
#  don baker      01 dec 85    updated for product version.
#  dennis shea       oct 98    created the NCL version
#  dennis shea     9 feb 99    fix: MoistAdiabat labels at top of curves
#
  localOpts                       = Resources()
  localOpts.sktDrawIsotherm       = True
  localOpts.sktDrawIsobar         = True
  localOpts.sktDrawMixRatio       = True
  localOpts.sktDrawDryAdiabat     = True
  localOpts.sktDrawMoistAdiabat   = True  # aka: saturation or pseudo adibat
  localOpts.sktDrawWind           = True
  localOpts.sktDrawStandardAtm    = True
  localOpts.sktDrawColLine        = True
  localOpts.sktDrawColAreaFill    = False
  localOpts.sktDrawFahrenheit     = True  # Fahrenheit "x" axis
  localOpts.sktDrawHeightScale    = False
  localOpts.sktDrawHeightScaleFt  = True  # default is feet [otherwise km]
  localOpts.sktDrawStandardAtmThk = 2.0
  localOpts.Font                  = "helvetica"
  localOpts.tiMainString          = "   "
  localOpts.vpXF                  = 0.07
  localOpts.vpYF                  = 0.925
  localOpts.vpWidthF              = 0.85
  localOpts.vpHeightF             = 0.85


#
#  Override localOpts attributes with Opts attributes for
#  Opts attributes that overlap localOpts attributes; set
#  new localOpts attributes for Opts attributes that do not
#  overlap localOpts attributes.
#
  if (not isinstance(Opts,Resources)):
    print ("skewt_bkg: argument 2 must be an Ngl Resources instance")
    return None
  OptsAtts = _crt_dict(Opts)
  if (len(_crt_dict(Opts)) != 0):
    for key in OptsAtts.keys():
      setattr(localOpts,key,OptsAtts[key])
#
#  Check for new resource names and convert them to the original ones.
#
    for new_name in OptsAtts.keys():
      if (RscConv.has_key(new_name)):
        setattr(localOpts,RscConv[new_name],OptsAtts[new_name])
#
#  Check for new sktTemperatureUnits or sktHeightScaleUnits resources,
#  as these take string values rather than True/False values.
#  The original names (sktDrawFahrenheit/sktHeightScaleFt) for these
#  two resources took True/False values.
#
        if (hasattr(localOpts,"sktTemperatureUnits")):
          if(string.lower(localOpts.sktTemperatureUnits) == "celsius"):
            localOpts.sktDrawFahrenheit = False    # default is True
          elif(string.lower(localOpts.sktTemperatureUnits) == "fahrenheit"):
            localOpts.sktDrawFahrenheit = True    # default is True
          else:
            localOpts.sktDrawFahrenheit = True    # default is True
            print ("Warning - skewt_bkg: 'sktTemperatureUnits' must be set to 'fahrenheit' or 'celsius'. Defaulting to 'fahrenheit'.")

        if (hasattr(localOpts,"sktHeightScaleUnits")):
          if(string.lower(localOpts.sktHeightScaleUnits) == "km"):
            localOpts.sktDrawHeightScaleFt = False    # default is True
          elif(string.lower(localOpts.sktHeightScaleUnits) == \
                            "feet"):
            localOpts.sktDrawHeightScaleFt = True    # default is True
          else:
            localOpts.sktDrawHeightScaleFt = True    # default is True
            print ("Warning - skewt_bkg: 'sktHeightScaleUnits' must be set to 'feet' or 'km'. Defaulting to 'feet'.")

#
#  Declare isotherm values (Celcius) and pressures (hPa) where 
#  isotherms intersect the edge of the skew-t diagram.
#
  temp = numpy.array(                                         \
        [                                                     \
           -100.,-90.,-80.,-70.,-60.,-50.,-40.,-30.,          \
            -20.,-10.,  0., 10., 20., 30., 40., 50.           \
          ],'f')
  lendt = numpy.array(                                        \
          [                                                   \
            132., 181., 247., 337., 459., 625., 855.,1050.,   \
           1050.,1050.,1050.,1050.,1050.,1050.,1050.,1050.    \
          ],'f')
  rendt = numpy.array(                                        \
          [                                                   \
            100., 100., 100., 100., 100., 100., 100., 135.,   \
            185., 251., 342., 430., 500., 580., 730., 993.    \
          ],'f')
          
  ntemp = len(temp)
  if (len(temp) != len(lendt) or len(lendt) != len(rendt)):
    print ("skewt_bkg: lengths of temp, lendt, rendt do not match")

#
#  Declare pressure values [hPa] and x coordinates of the endpoints 
#  of each isobar.  These x,y values are computed from the equations 
#  in the transform functions listed at the beginning of this program.
#  Refer to a skew-t diagram for reference if necessary.
#
  pres = numpy.array(                                \
         [                                           \
          1050., 1000.,  850.,  700.,  500.,  400.,  \
           300.,  250.,  200.,  150.,  100.          \
         ],'f')
  xpl  = numpy.array(                                \
         [                                           \
          -19.0, -19.0, -19.0, -19.0, -19.0, -19.0,  \
          -19.0, -19.0, -19.0, -19.0, -19.0          \
         ],'f')
  xpr  = numpy.array(                                \
         [                                           \
           27.10, 27.10, 27.10, 27.10, 22.83, 18.60, \
           18.60, 18.60, 18.60, 18.60, 18.60         \
         ],'f')
  npres = len(pres)
  if (len(pres) != len(xpl) or len(xpl) != len(xpr)):
    print (("skewt_bkg: lengths of pres, xpl, xpr do not match"))

#
#  Declare adiabat values [C] and pressures where adiabats 
#  intersect the edge of the skew-t diagram.  Refer to a 
#  skew-t diagram if necessary.
#
  theta  = numpy.array(                                \
           [                                           \
            -30., -20., -10.,   0.,  10.,  20.,  30.,  \
             40.,  50.,  60.,  70.,  80.,  90., 100.,  \
            110., 120., 130., 140., 150., 160., 170.   \
           ],'f')
  lendth = numpy.array(                                \
           [                                           \
            880., 670., 512., 388., 292., 220., 163.,  \
            119., 100., 100., 100., 100., 100., 100.,  \
            100., 100., 100., 100., 100., 100., 100.   \
           ],'f')
  rendth = numpy.array(                                      \
           [                                                 \
            1050., 1050., 1050., 1050., 1050., 1050., 1050., \
            1050., 1003.,  852.,  728.,  618.,  395.,  334., \
             286.,  245.,  210.,  180.,  155.,  133.,  115.  \
           ],'f')
  ntheta = len(theta)
  if (len(theta) != len(lendth) or len(lendth) != len(rendth)):
    print ("skewt_bkg: lengths of pres, xpl, xpr do not match")

#
#  Declare moist adiabat values and pressures of the tops of the
#  moist adiabats.  All moist adiabats to be plotted begin at 1050 mb.
#
  pseudo = numpy.array(                                 \
           [                                            \
              32., 28., 24., 20., 16., 12.,  8.         \
           ],'f')
  lendps = numpy.array(                                 \
           [                                            \
              250., 250., 250., 250., 250., 250., 250.  \
           ],'f')
  npseudo= len(pseudo)          # moist adiabats

#
#  Declare mixing ratio lines.  All mixing ratio lines will begin
#  at 1050 mb and end at 400 mb.
#
  mixrat = numpy.array(                        \
           [                                   \
              20., 12., 8., 5., 3., 2., 1.     \
           ],'f')
  nmix  = len(mixrat)           # mixing ratios

#
#  Declare local stuff: arrays/variables for storing x,y positions
#  during iterations to draw curved line, etc.
#
  sx    = numpy.zeros(200,'f')
  sy    = numpy.zeros(200,'f')
  xx    = numpy.zeros(  2,'f')
  yy    = numpy.zeros(  2,'f')
  m2f   =    3.2808            # meter-to-feet
  f2m   = 1./3.2808            # feet-to-meter

#
#  Define absolute x,y max/min bounds corresponding to the outer
#  edges of the diagram.  These are computed by inserting the appropriate
#  pressures and temperatures at the corners of the diagram.
#
                    # xmin = _skewtx ( -33.60,_skewty(1050.)) [t=deg C]
  xmin = -18.9551048  # xmin = _skewtx (-109.10,_skewty( 100.)) [t=deg C]
  xmax =  27.0973729  # xmax = _skewtx (  51.75,_skewty(1050.)) [t=deg C]
  ymax =  -0.9346217  # ymax = _skewty (1050.)
  ymin =  44.0600000  # ymin = _skewty ( 100.)

#
#  Specify arrays to hold corners of the diagram in x,y space.
#
  xc = numpy.array(                                 \
       [                                            \
          xmin, xmin, xmax, xmax, 18.60, 18.6, xmin \
       ],'f')
  yc = numpy.array(                                 \
       [                                            \
          ymin, ymax, ymax,  9.0, 17.53, ymin, ymin \
       ],'f')

#
#  Depending on how options are set, create Standard Atm Info.

  if (localOpts.sktDrawStandardAtm or  \
      localOpts.sktDrawHeightScale or  \
      localOpts.sktDrawWind):

#
#  U.S. Standard ATmosphere (km), source: Hess/Riegel.
#
    zsa = numpy.array(range(0,17),'f')
    psa = numpy.array(                                       \
          [                                                  \
           1013.25, 898.71, 794.90, 700.99, 616.29, 540.07,  \
            471.65, 410.46, 355.82, 307.24, 264.19, 226.31,  \
            193.93, 165.33, 141.35, 120.86, 103.30
          ],'f')
    tsa = numpy.array(                                       \
          [                                                  \
              15.0,   8.5,    2.0,   -4.5,  -11.0,  -17.5,   \
             -24.0, -30.5,  -37.0,  -43.5,  -50.0,  -56.5,   \
             -56.5, -56.5,  -56.5,  -56.5,  -56.5            \
          ],'f')
    nlvl = len(psa)

#
#  Plot.
#
  if (localOpts.sktDrawColLine):
    colGreen  = "Green"
    colBrown  = "Orange4"
    colTan    = "DarkGoldenRod1"
  else:
    colGreen  = "Foreground"
    colBrown  = "Foreground"
    colTan    = "Foreground"

#
#  Draw outline of the skew-t, log p diagram.  Proceed in the upper left
#  corner of the diagram and draw counter-clockwise.  The array locations
#  below that are hardcoded refer to points on the background where the
#  skew-t diagram deviates from a rectangle, along the right edge.  Remember,
#  the set call defines a rectangle, so as long as the boundary is along
#  the edge of the set call, the points plotted are combinations of the min
#  and max x,y values in the set call.
#

  if (localOpts.sktDrawFahrenheit):
    tf = numpy.array(range(-20,110,20),'i')             # deg F
    tc = 0.55555 * (tf - 32.)                           # deg C
  else:
    tc = numpy.array(range(-30,50,10),'f')

#
#  Don't draw the plot or advance the frame in the call to xy.
#  Specify location/size of the skewT diagram.
#
  xyOpts             = Resources()
  xyOpts.nglDraw     = False
  xyOpts.nglFrame    = False
  xyOpts.vpXF        = localOpts.vpXF
  xyOpts.vpYF        = localOpts.vpYF
  xyOpts.vpWidthF    = localOpts.vpWidthF
  xyOpts.vpHeightF   = localOpts.vpHeightF
  if (hasattr(localOpts,"nglMaximize")):
    xyOpts.nglMaximize = localOpts.nglMaximize

#
#  Define y tick mark labels.
#
  xyOpts.tmYLMode   = "Explicit"
  xyOpts.tmYLValues = _skewty(pres[1:]) # skip 1050
  xyOpts.tmYLLabels =                            \
          [                                      \
           "1000", "850", "700", "500", "400",   \
            "300", "250", "200", "150", "100"    \
          ]

#
#  Define x tick mark labels.
#
  xyOpts.tmXBMode   = "Explicit"
  xyOpts.tmXBValues = _skewtx (tc, _skewty(1050.)) # transformed vals
  if (localOpts.sktDrawFahrenheit):
      xyOpts.tmXBLabels = tf                     # plot the nice deg F
  else:
      xyOpts.tmXBLabels = tc                     # plot the nice deg C

  xyOpts.trXMinF       = xmin
  xyOpts.trXMaxF       = xmax
  xyOpts.trYMinF       = ymax       # Note: ymin > ymax
  xyOpts.trYMaxF       = ymin
  xyOpts.xyComputeXMin = False
  xyOpts.xyComputeXMax = False
  xyOpts.xyComputeYMin = False
  xyOpts.xyComputeYMax = False
  xyOpts.tmXTOn        = False
  xyOpts.tmYROn        = False
  xyOpts.tmXTBorderOn  = False
  xyOpts.tmXBBorderOn  = False
  xyOpts.tmYRBorderOn  = False
  xyOpts.tmYLBorderOn  = False

#
#  Tune the plot.
#
  xyOpts.tmXBMajorLengthF        = 0.01
  xyOpts.tmXBMajorThicknessF     = 1.0         # default is 2.0
  xyOpts.tmXBMajorOutwardLengthF = 0.01
  xyOpts.tmXTMajorLengthF        = 0.
#
#  Suppress the tickmarks on the Y axis - need to turn
#  nglScale off, since it will override the tickmark settings
#  for the Y axis by making them the same as the X axis.
#
  xyOpts.tmYLMajorLengthF        = 0.
  xyOpts.tmYLMinorLengthF        = 0.
  xyOpts.nglScale                = False       

  xyOpts.tmXBLabelFontHeightF = 0.014
  xyOpts.tmYLLabelFontHeightF = xyOpts.tmXBLabelFontHeightF
  if (localOpts.sktDrawFahrenheit):
      xyOpts.tiXAxisString        = "Temperature (F)"
  else:
      xyOpts.tiXAxisString        = "Temperature (C)"
  xyOpts.tiXAxisFont          = localOpts.Font
  xyOpts.tiXAxisFontColor     = "Foreground"   # colTan
  xyOpts.tiXAxisFontHeightF   = 0.0125
  xyOpts.tiYAxisFont          = localOpts.Font
  xyOpts.tiYAxisString        = "P (hPa)"
  xyOpts.tiYAxisOffsetXF      = 0.0200
  xyOpts.tiYAxisOffsetYF      = -0.0200
  xyOpts.tiYAxisFontColor     = "Foreground"   # colTan
  xyOpts.tiYAxisFontHeightF   = xyOpts.tiXAxisFontHeightF
  xyOpts.tiMainString         = localOpts.tiMainString
  if (hasattr(localOpts,"tiMainFuncCode")):
    xyOpts.tiMainFuncCode     = localOpts.tiMainFuncCode
#
#  Uncomment if X or Y axis labels are allowed to be set by the user.
#
# if (hasattr(localOpts,"tiXAxisFuncCode")):
#   xyOpts.tiXAxisFuncCode    = localOpts.tiXAxisFuncCode
# if (hasattr(localOpts,"tiYAxisFuncCode")):
#   xyOpts.tiYAxisFuncCode    = localOpts.tiYAxisFuncCode
 
  xyOpts.tiMainFont           = localOpts.Font
  xyOpts.tiMainFontColor      = "Foreground"
  xyOpts.tiMainFontHeightF    = 0.025
  xyOpts.tiMainOffsetXF       = -0.1

#
#  Special for the right hand side.
#
  if (localOpts.sktDrawHeightScale):  
    xyOpts.trXMaxF      = _skewtx (55. , _skewty(1013.)) # extra wide
    xyOpts.tmYUseLeft   = False # Keep right axis independent of left.
    xyOpts.tmYRBorderOn = True
    xyOpts.tmYROn       = True  # Turn on right axis tick marks.
    xyOpts.tmYRLabelsOn = True  # Turn on right axis labels.
    xyOpts.tmYRLabelFontHeightF    = xyOpts.tmYLLabelFontHeightF
    xyOpts.tmYRMajorThicknessF     = xyOpts.tmXBMajorThicknessF
    xyOpts.tmYRMajorLengthF        = xyOpts.tmXBMajorLengthF
    xyOpts.tmYRMajorOutwardLengthF = xyOpts.tmXBMajorOutwardLengthF
    xyOpts.tmYRMinorOn             = False       # No minor tick marks.
    xyOpts.tmYRMode                = "Explicit"  # Define tick mark labels.

    zkm = numpy.array(range(0,17),'f')
    pkm = ftcurv(zsa, psa, zkm)
    zft = numpy.array(                                    \
          [                                               \
             0.,  2.,  4.,  6.,  8., 10., 12., 14., 16.,  \
            18., 20., 25., 30., 35., 40., 45., 50.        \
          ],'f')
    pft = ftcurv(zsa, psa, f2m * zft)  # p corresponding to zkm

    if (localOpts.sktDrawHeightScaleFt):
      znice =  zft
      pnice = _skewty(pft)
      zLabel= "Height (1000 Feet)"
    else:
      znice = zkm
      pnice = _skewty(pkm)
      zLabel= "Height (Km)"
#
#  At each "nice" pressure value, put a "height" value label.
#
    xyOpts.tmYRValues   = pnice
    xyOpts.tmYRLabels   = znice

#
#  Draw outline and the x and y axes.
#
  xyplot = xy (wks,xc,yc,xyOpts)

#
#  right *label* MUST be added AFTER xy created.
#
  if (localOpts.sktDrawHeightScale):
    txOpts                   = Resources()
    txOpts.txAngleF          = 270.
    txOpts.txFontColor       = "Foreground"   # colTan
    txOpts.txFontHeightF     = xyOpts.tmYLLabelFontHeightF
    xlab                     = _skewtx (53., _skewty(1013.))
    ylab                     = _skewty (350.)
    text (wks,xyplot,zLabel,xlab,ylab,txOpts) 
    del txOpts

  if (localOpts.sktDrawColAreaFill):
    color1 = "PaleGreen2"            # "LightGreen"
    color2 = "Background"            # "Azure"
    gsOpts = Resources()
    for i in xrange(0,ntemp-1):
      if (i%2 == 0):                 # alternate colors
        gsOpts.gsFillColor = color1
      else:
        gsOpts.gsFillColor = color2

      nx = 3
      sy[0] = _skewty(lendt[i  ])
      sx[0] = _skewtx( temp[i  ], sy[0])
      sy[1] = _skewty(lendt[i+1] )
      sx[1] = _skewtx( temp[i+1], sy[1])
      sy[2] = _skewty(rendt[i+1] )
      sx[2] = _skewtx( temp[i+1], sy[2])
      sy[3] = _skewty(rendt[i  ] )   
      sx[3] = _skewtx( temp[i  ], sy[3])


#
#  Make sure the right sides line up with vertical line x=18.6 
#  and the left sides line up with vertical line x=xmin.
#
      if (i > 6 and i < 10):
        sx[2] = sx[3] = 18.6
      if (i < 6):
        sx[0] = sx[1] = -18.955

#
#  Special cases.
#
      if (temp[i] == -40.):
        nx = 5
        sy[0:nx+1] = numpy.array(                                 \
                     [                                            \
                       2.9966, ymax, ymax, 38.317, ymin, ymin     \
                     ],'f')
        sx[0:nx+1] = numpy.array(                                 \
                     [                                            \
                       xmin, xmin, -17.0476, 18.60, 18.60, 18.359 \
                     ],'f')
      if (temp[i] ==   0.):
        nx = 4
        sy[0:nx+1] = numpy.array(                                 \
                     [                                            \
                        ymax, ymax, 16.148, 17.53, 20.53          \
                     ],'f')
        sx[0:nx+1] = numpy.array(                                 \
                     [                                            \
                       -0.8476, 4.5523, 20.045, 18.60, 18.60      \
                     ],'f')
      if (temp[i] == 30.):
        nx = 4
        sy[0:nx+1] = numpy.array(                                 \
                     [                                            \
                       ymax, ymax, 6.021, 9.0, 10.422             \
                     ],'f')
        sx[0:nx+1] = numpy.array(                                 \
                     [                                            \
                       15.3523 , 20.7523 , 27.0974, 27.0974, 25.6525  \
                     ],'f')
      polygon(wks, xyplot, sx[0:nx+1], sy[0:nx+1], gsOpts)
#
#  Upper left triangle.
#
    gsOpts.gsFillColor = color2
    sy[0:3] = numpy.array(                \
                 [                        \
                   ymin, ymin, 38.747     \
                 ],'f')
    sx[0:3] = numpy.array(                \
                 [                        \
                   -14.04, -18.955, -18.955 \
                 ],'f')
    polygon(wks, xyplot, sx[0:3], sy[0:3], gsOpts)
#
#  Lower right triangle.
#
    gsOpts.gsFillColor = color2
    sy[0:3] = numpy.array(                \
                 [                        \
                   ymax, 0.1334, ymax     \
                 ],'f')
    sx[0:3] = numpy.array(                \
                 [                        \
                   xmax, xmax, 26.1523    \
                 ],'f')
    polygon(wks, xyplot, sx[0:3],sy[0:3],gsOpts)
    del gsOpts

#
#  Draw diagonal isotherms.
#  [brown with labels interspersed at 45 degree angle]
#
  if (localOpts.sktDrawIsotherm):
    gsOpts                   = Resources()
    gsOpts.gsLineDashPattern = 0            # solid
    gsOpts.gsLineColor       = colTan
    gsOpts.gsLineThicknessF  = 1.0
    #gsOpts.gsLineLabelFontColor   = colTan
    #gsOpts.gsLineLabelFontHeightF = 0.0125

    txOpts                   = Resources()
    txOpts.txAngleF          = 45.
    txOpts.txFontColor       = gsOpts.gsLineColor
    txOpts.txFontHeightF     = 0.0140
    txOpts.txFontThicknessF  = 1.0

    for i in range(0,len(temp)-2):
      yy[1] = _skewty(rendt[i])
      xx[1] = _skewtx( temp[i], yy[1])
      yy[0] = _skewty(lendt[i])
      xx[0] = _skewtx( temp[i], yy[0])
      #gsOpts.gsLineLabelString  = int(temp[i])
      polyline(wks, xyplot, xx, yy, gsOpts)

      xlab  = xx[1] + 0.625
      ylab  = yy[1] + 0.55
      label = int(temp[i])
      text(wks, xyplot, str(label), xlab, ylab, txOpts)
    del gsOpts
    del txOpts

#
#  Draw horizontal isobars.
#
  if (localOpts.sktDrawIsobar):
      gsOpts                   = Resources()
      gsOpts.gsLineDashPattern = 0            # solid
      gsOpts.gsLineColor       = colTan
      gsOpts.gsLineThicknessF  = 1.0
      #gsOpts.gsLineLabelFontColor    = colTan
      #gsOpts.gsLineLabelFontHeightF  = 0.0125

      for i in range(0,npres):
        xx[0] = xpl[i]
        xx[1] = xpr[i]
        ypl   = _skewty(pres[i])
        yy[0] = ypl
        yy[1] = ypl
        polyline(wks, xyplot, xx, yy, gsOpts)
      del gsOpts

#
#  Draw saturation mixing ratio lines.  These lines run 
#  between 1050 and 400 mb.  The 20 line intersects the 
#  sounding below 400 mb, thus a special case is made for 
#  it.  The lines are dashed green.  The temperature where 
#  each line crosses 400 mb is computed in order to get x,y 
#  locations of the top of the lines.
#
  if (localOpts.sktDrawMixRatio):
    gsOpts                   = Resources()   # polyline graphic style opts
    gsOpts.gsLineThicknessF  = 1.0
#
#  saturation  mix ratio only.
#
    gsOpts.gsLineDashPattern = 2        
    gsOpts.gsLineColor       = colGreen 

    txOpts                   = Resources()
    txOpts.txAngleF          = 65.     
    txOpts.txFontColor       = colGreen
    txOpts.txFontHeightF     = 0.0100  

    yy[1] = _skewty( 400.)    # y at top [right end of slanted line]
    yy[0] = _skewty(1000.)    # y at bottom of line [was 1050.]

    for i in range(0,nmix):
      if (mixrat[i] == 20.):
        yy[1] = _skewty(440.)
        tmix  = _dtmrskewt(mixrat[i],440.)
      else:
        yy[1] = _skewty(400.)
        tmix  = _dtmrskewt(mixrat[i],400.)
      xx[1] = _skewtx(tmix,yy[1])
      tmix  = _dtmrskewt(mixrat[i],1000.)   # was 1050
      xx[0] = _skewtx(tmix,yy[0])
      polyline (wks,xyplot,xx,yy,gsOpts)   # dashed green

      xlab  = xx[0]-0.25
      ylab  = yy[0]-0.45
      label = int(mixrat[i])
      text(wks, xyplot, str(label), xlab, ylab, txOpts)
    del gsOpts
    del txOpts

#
#  Draw dry adiabats.  Iterate in 10 mb increments to compute the x,y
#  points on the curve.
#
  if (localOpts.sktDrawDryAdiabat):
    gsOpts                   = Resources()
    gsOpts.gsLineDashPattern = 0            
    gsOpts.gsLineColor       = colTan     
    gsOpts.gsLineThicknessF  = 1.0

    txOpts                   = Resources()
    txOpts.txAngleF          = 300.
    txOpts.txFontColor       = colTan
    txOpts.txFontHeightF     = 0.01
    txOpts.txFontThicknessF  = 1.0

    pinc = 10.
    for i in range(0,ntheta):
      p = lendth[i]-pinc
      for j in range(0,len(sy)):
        p = p+pinc
        if (p > rendth[i]):
          sy[j] = _skewty(rendth[i])
          t     = _dtdaskewt(theta[i],p)   # get temp on dry adiabat at p
          sx[j] = _skewtx(t,sy[j])
          break 
        sy[j] = _skewty(p)
        t     = _dtdaskewt(theta[i],p)
        sx[j] = _skewtx(t,sy[j])
      #polyline (wks,xyplot,sx[:j-1],sy[:j-1],gsOpts)     # whole line  

      if (theta[i] < 170.):
        polyline (wks,xyplot,sx[1:j],sy[1:j],gsOpts)  # label room  
        ylab  = _skewty(lendth[i]+5.)
        t     = _dtdaskewt(theta[i],lendth[i]+5.)
        xlab  = _skewtx(t,ylab)
        label = int(theta[i])
        text(wks,xyplot,str(label),xlab,ylab,txOpts)
      else:                                            # no label
        polyline (wks,xyplot,sx[:j],sy[:j],gsOpts)     # whole line
    del gsOpts
    del txOpts

#
#  Draw moist adiabats up to 230 [was 250] mb.
#  Draw the lines.  Dterate in 10 mb increments from 1060 mb.
#
  if (localOpts.sktDrawMoistAdiabat):
    gsOpts                   = Resources()
    gsOpts.gsLineColor       = colGreen
    gsOpts.gsLineThicknessF  = 0.5
    gsOpts.gsLineDashPattern = 0

    txOpts                   = Resources()
    txOpts.txAngleF          = 0.
    txOpts.txFontColor       = colGreen
    txOpts.txFontHeightF     = 0.0125
    txOpts.txFontThicknessF  = 1.0

    pinc = 10.

    for i in range(0,npseudo):
      p = 1060.
      for j in range (0, len (sy)):
        p = p - pinc
        if (p < 230.):     # was "250"
          break
        sy[j] = _skewty(p)
        t     = _dsatlftskewt(pseudo[i],p)    # temp on moist adiabat at p.
        sx[j] = _skewtx(t,sy[j])

      polyline (wks, xyplot, sx[:j-1], sy[:j-1], gsOpts)

      ylab  = _skewty(p + 0.5*pinc)
      t     = _dsatlftskewt(pseudo[i], p + 0.75*pinc)
      xlab  = _skewtx(t,ylab)
      label = int(pseudo[i])     # 9 Feb 99 fix
      text(wks, xyplot, str(label), xlab, ylab, txOpts)

    del gsOpts
    del txOpts

  if (localOpts.sktDrawStandardAtm):
      gsOpts                   = Resources()
      gsOpts.gsLineColor       = colTan   
      gsOpts.gsLineThicknessF  = localOpts.sktDrawStandardAtmThk
      gsOpts.gsLineDashPattern = 0             

      for i in range(0,nlvl):
         sy[i] = _skewty(psa[i])
         sx[i] = _skewtx(tsa[i], sy[i])

      polyline (wks, xyplot, sx[0:nlvl], sy[0:nlvl], gsOpts)
      del gsOpts

#
#  Draw vertical line upon which to plot wind barbs.
#
  if (localOpts.sktDrawWind):
      gsOpts = Resources()
      gsOpts.gsLineColor       = "Foreground"
      gsOpts.gsLineThicknessF  = 0.5
      gsOpts.gsLineDashPattern = 0
      gsOpts.gsMarkerIndex     = 4   # "hollow_circle"=> std pres
      gsOpts.gsMarkerColor     = "Foreground"

      presWind      = pres
      presWind[0]   = 1013.          # override 1050
      xWind         = _skewtx (45. , _skewty(presWind[0])) 
      sx[0:npres] = xWind            # "x" location of wind plot
      try:
        sy[0:npres] = _skewty(presWind).astype(numpy.Float0)
      except:
        sy[0:npres] = _skewty(presWind).astype(numpy.float)
      polyline   (wks, xyplot, sx[0:npres], sy[0:npres], gsOpts)
      polymarker (wks, xyplot, sx[1:npres], sy[1:npres], gsOpts)
                                     # zwind => Pibal reports
      zftWind = numpy.array(                                      \
                              [0.,  1.,  2.,  3.,  4.,  5.,  6.,  \
                               7.,  8.,  9., 10., 12., 14., 16.,  \
                              18., 20., 25., 30., 35., 40., 45.,  \
                              50.],'f')
      zkmWind = zftWind*f2m
      pkmWind = ftcurv(zsa, psa, zkmWind)
      nzkmW   = len(zkmWind)

      sx[0:nzkmW]  = xWind              # "x" location of wind plot
      try:
        sy[0:nzkmW]  = _skewty(pkmWind).astype(numpy.Float0)
      except:
        sy[0:nzkmW]  = _skewty(pkmWind).astype(numpy.float)

      gsOpts.gsMarkerIndex      = 16     # "circle_filled" -> Pibal
      gsOpts.gsMarkerSizeF      = 0.0035 # 0.007 is default
      gsOpts.gsMarkerThicknessF = 0.5    # 1.0 is default
      polymarker (wks, xyplot, sx[0:nzkmW], sy[0:nzkmW], gsOpts)
      del gsOpts

  return xyplot

################################################################

def skewt_plt(wks, skewt_bkgd, P, TC, TDC, Z, WSPD, WDIR, 
             dataOpts=None):
  """
Plots soundings and (optionally) winds on Skew T, Log P charts created
by Ngl.skewt_bkg.
splt = Ngl.skewt_plt(wks, bkgd, P, TC, TDC, Z, WSPD, WDIR, dataOpts=None)
wks -- The identifier returned from calling Ngl.open_wks.
bkgd -- The identifier returned from calling Ngl.skewt_bkg.
P -- An array of pressure values (mb/hPa).
TC -- An array of the same length as P containing temperature values.  By
      default these are assumed to be in Fahrenheit.  If you are using
      Celsius, then you need to specify this using the resource
      sktTemperatureUnits.
TDC -- An array of the same length as P containing dew point
       temperature values.  By default these are assumed to be in 
       Fahrenheit.  If you are using Celsius, then you need to 
       specify this using the resource sktTemperatureUnits.
Z -- An array of the same length as P containing geopotential values
     (gpm).
WSPD -- An array of the same length as P containing wind speed values
        (knots or m/s).
WDIR -- An array of the same length as P containing meteorological
        wind direction values.
dataOpts -- An optional instance of the Resources class having
            special "skt" resources as attributes.
  """
#
#  p    =  pressure     [mb / hPa]
#  tc   = temperature   [F or C]
#  tdc  = dew pt temp   [F or C]
#  z    = geopotential  [gpm]
#  wspd = wind speed    [knots or m/s]
#  wdir = meteorological wind direction
#

#
# Make sure if we have masked arrays, they get converted to
# numpy arrays.
#
  P2,fill_value_P2       = _get_arr_and_fv(P)
  Z2,fill_value_Z2       = _get_arr_and_fv(Z)
  TC2,fill_value_TC2     = _get_arr_and_fv(TC)
  TDC2,fill_value_TDC2   = _get_arr_and_fv(TDC)
  WSPD2,fill_value_WSPD2 = _get_arr_and_fv(WSPD)
  WDIR2,fill_value_WDIR2 = _get_arr_and_fv(WDIR)

#
#  Check for new resource names in dataOpts and convert them to
#  the original ones and set them as dataOpts attributes.
#
  OptsAtts = _crt_dict(dataOpts)
  for new_name in OptsAtts.keys():
    if (RscConv.has_key(new_name)):
      setattr( dataOpts,RscConv[new_name],OptsAtts[new_name])
#
#  Set missing values for variables
#  used in plotting the sounding and 
#  in calculating thermodynamic quantities.
#
  Pmissing    = _get_skewt_msg("P","sktPmissingV",
                                   "sktPressureMissingV",
                                  dataOpts,fill_value_P2)
  TCmissing   = _get_skewt_msg("TC","sktTCmissingV",
                                    "sktTemperatureMissingV",
                                    dataOpts,fill_value_TC2)
  TDCmissing  = _get_skewt_msg("TDC","sktTDCmissingV",
                                     "sktDewPointMissingV",
                                     dataOpts,fill_value_TDC2)
  Zmissing    = _get_skewt_msg("Z","sktZmissingV",
                                   "sktGeopotentialMissingV",
                                   dataOpts,fill_value_Z2)
  WSPDmissing = _get_skewt_msg("WSPD","sktWSPDmissingV",
                                      "sktWindSpeedMissingV",
                                      dataOpts,fill_value_WSPD2)
  WDIRmissing = _get_skewt_msg("WDIR","sktWDIRmissingV",
                                      "sktWindDirectionMissingV",
                                       dataOpts,fill_value_WDIR2)
  Hmissing    = _get_skewt_msg("H","sktHmissingV",
                                   "sktHeightWindBarbPositionMissingV",
                                   dataOpts,None)
#
  mv0 = numpy.logical_and(numpy.logical_not(_ismissing( P2,Pmissing)),   \
                          numpy.logical_not(_ismissing(TC2,TCmissing)))
  mv1 = numpy.logical_and(mv0,numpy.logical_not(_ismissing(TDC2,TDCmissing)))
  mv2 = numpy.logical_and(mv1,numpy.greater_equal(P2,100.))
  idx = ind(mv2)
  del mv0,mv1,mv2
  p   = numpy.take(  P2,idx)
  tc  = numpy.take( TC2,idx)
  tdc = numpy.take(TDC2,idx)

#
#  Check if the temperature and pressure data values are out of range.
#
  if (numpy.any(tc > 150.)):
      print ("skewt_plt: temperature values are out of range for Fahrenheit or Celsius.")
      return None
  if (numpy.any(tdc > 150.)):
      print ("skewt_plt: dew point temperature values are out of range for Fahrenheit or Celsius.")
      return None
  if (numpy.any(p > 1100.)):
      print ("skewt_plt: pressure values are out of range (must be in millibars).")
      return None

#
#  Local options describing data and ploting.
#
  localOpts           = Resources()
  localOpts.sktPrintZ    = True     # print geopotential (Z) on skewT diagram
  localOpts.sktPlotWindP = True     # plot wind barbs at p lvls
  localOpts.sktWspdWdir  = True     # wind speed and dir [else: u,v]
  localOpts.sktPlotWindH = False    # plot wind barbs at h lvls [pibal; special]
  localOpts.sktHspdHdir  = True     # wind speed and dir [else: u,v]
  localOpts.sktThermoInfo= True     # print thermodynamic info
  localOpts.sktCape      = True     # plot CAPE parcel profile if cape > 0
  localOpts.sktParcel    = 0        # subscript corresponding to initial parcel

#
#  Override localOpts attributes with dataOpts attributes for
#  dataOpts attributes that overlap localOpts attributes; set
#  new localOpts attributes for dataOpts attributes that do not
#  overlap localOpts attributes.
#
  if not dataOpts is None:
    if (not isinstance(dataOpts,Resources)):
      print ("skewt_plt: last argument must be an Ngl Resources instance.")
      return None
    OptsAtts = _crt_dict(dataOpts)
    if (len(OptsAtts) != 0):
      for key in OptsAtts.keys():
        setattr(localOpts,key,OptsAtts[key])
#
#  Check for new resource names in dataOpts and convert them to
#  the original ones and set them for localOpts.
#
      for new_name in OptsAtts.keys():
        if (RscConv.has_key(new_name)):
          setattr(localOpts,RscConv[new_name],OptsAtts[new_name])
#
#  Check for new sktPressureWindBarbComponents or sktHeightWindBarbComponents
#  resources, as these take string values rather than True/False values.
#  The original names (sktWspdWdir/sktHspdHdir) for these two resources
#  took True/False values.
#
        if (hasattr(localOpts,"sktPressureWindBarbComponents")):
          if(string.lower(localOpts.sktPressureWindBarbComponents) == "uv"):
            localOpts.sktWspdWdir = False    # default is True
          elif(string.lower(localOpts.sktPressureWindBarbComponents) == \
                            "speeddirection"):
            localOpts.sktWspdWdir = True    # the default
          else:
            localOpts.sktWspdWdir = True    # the default
            print ("Warning - skewt_plt: 'sktPressureWindBarbComponents' must be set to 'SpeedDirection' or 'UV'. Defaulting to 'SpeedDirection'.")

        if (hasattr(localOpts,"sktHeightWindBarbComponents")):
          if(string.lower(localOpts.sktHeightWindBarbComponents) == "uv"):
            localOpts.sktHspdHdir = False    # default is True
          elif(string.lower(localOpts.sktHeightWindBarbComponents) == \
                            "speeddirection"):
            localOpts.sktHspdHdir = True    # the default
          else:
            localOpts.sktHspdHdir = True    # the default
            print ("Warning - skewt_plt: 'sktHeightWindBarbComponents' must be set to 'SpeedDirection' or 'UV'. Defaulting to 'SpeedDirection'.")

  vpXF                 = get_float(skewt_bkgd,"vpXF")
  vpYF                 = get_float(skewt_bkgd,"vpYF")
  vpWidthF             = get_float(skewt_bkgd,"vpWidthF")
  vpHeightF            = get_float(skewt_bkgd,"vpHeightF")
  tiMainFont           = get_string(skewt_bkgd,"tiMainFont")
  tiMainFontHeightF    = get_float(skewt_bkgd,"tiMainFontHeightF")
  tiMainOffsetXF       = get_float(skewt_bkgd,"tiMainOffsetXF")
  tmYLLabelFontHeightF = get_float(skewt_bkgd,"tmYLLabelFontHeightF")

#
#  Specify various colors.
#
  colForeGround     = "Foreground"
  sktcolTemperature = "Foreground"
  sktcolDewPt       = "RoyalBlue"
  sktcolPpath       = "Red"
  sktcolZLabel      = "Foreground"
  sktcolWindP       = "Black"   
  sktcolWindZ       = "Blue"   
  sktcolWindH       = "OrangeRed3"    
  sktcolThermoInfo  = "Goldenrod4"

#
#  Change defaults.
#
  if (hasattr(localOpts,"sktcolTemperature")):
    sktcolTemperature  = localOpts.sktcolTemperature
  if (hasattr(localOpts,"sktcolDewPt")):
    sktcolDewPt  = localOpts.sktcolDewPt
  if (hasattr(localOpts,"sktcolPpath")):
    sktcolPpath  = localOpts.sktcolPpath 
  if (hasattr(localOpts,"sktcolZLabel")):
    sktcolZLabel  = localOpts.sktcolZLabel 
  if (hasattr(localOpts,"sktcolWindP")):
    sktcolWindP  = localOpts.sktcolWindP 
  if (hasattr(localOpts,"sktcolWindZ")):
    sktcolWindZ  = localOpts.sktcolWindZ 
  if (hasattr(localOpts,"sktcolWindH")):
    sktcolWindH  = localOpts.sktcolWindH 
  if (hasattr(localOpts,"sktcolThermoInfo")):
    sktcolThermoInfo  = localOpts.sktcolThermoInfo 


#
#  Graphics style settings for the polyline draw.
#
  gsOpts                   = Resources()
  gsOpts.gsLineDashPattern = 0      # solid (default)
  gsOpts.gsLineThicknessF  = 3.0    # make thicker

  if (hasattr(localOpts,"gsLineDashPattern")):
    gsOpts.gsLineDashPattern = localOpts.gsLineDashPattern
  if (hasattr(localOpts,"gsLineThicknessF")):
    gsOpts.gsLineThicknessF = localOpts.gsLineThicknessF

  yp   = _skewty(p)
  xtc  = _skewtx(tc, yp)
  gsOpts.gsLineColor  = sktcolTemperature
  polyline(wks, skewt_bkgd, xtc, yp, gsOpts)

  xtdc = _skewtx(tdc, yp)
  gsOpts.gsLineColor  = sktcolDewPt
  polyline(wks, skewt_bkgd, xtdc, yp, gsOpts)

  del gsOpts

  if (localOpts.sktThermoInfo):
    nP   = localOpts.sktParcel  # default is the lowest level [0]
    nlvls= len(p)
    plcl = -999.             # p (hPa) Lifting Condensation Lvl (lcl)
    tlcl = -999.             # temperature (C) of lcl
    plcl, tlcl = _dptlclskewt(p[nP],tc[nP],tdc[nP])
    shox = _dshowalskewt(p,tc,tdc,nlvls)     # Showwalter Index

    pwat = _dpwskewt(tdc,p,nlvls)            # precipitable water (cm)

    iprnt= 0                                # debug only (>0)
    nlLcl= 0                              
    nlLfc= 0
    nlCross= 0

    if (hasattr(localOpts,"sktTCmissingV")):
      TCmissing = localOpts.sktTCmissingV
      if (numpy.any(_ismissing(tc,TCmissing))):
        print ("skewt_plt: tc (temperature) cannot have missing values if sktThermoInfoLabelOn is True.")
        return None
    TCmissing = -999.
    cape,tpar,nlLcl,nlLfc,nlCross  =  \
         dcapethermo(p,tc,len(p),plcl,iprnt,TCmissing)
#        nglf.dcapethermo(p,tc,len(p),plcl,iprnt,TCmissing)

                                            # 0.5 is for rounding
    info = " Plcl="     + str(int(plcl+0.5)) \
         + " Tlcl[C]="  + str(int(tlcl+0.5)) \
         + " Shox="     + str(int(shox+0.5)) \
         + " Pwat[cm]=" + str(int(pwat+0.5)) \
         + " Cape[J]= " + str(int(cape))

    txOpts                   = Resources()
    txOpts.txAngleF          = 0.
    txOpts.txFont            = tiMainFont
    txOpts.txFontColor       = sktcolThermoInfo
    txOpts.txFontHeightF     = 0.5*tiMainFontHeightF
    xinfo                    = vpXF  + 0.5*vpWidthF + tiMainOffsetXF
    yinfo                    = vpYF  + 0.5*tiMainFontHeightF
    text_ndc (wks,info,xinfo,yinfo,txOpts)
    del txOpts

    if (localOpts.sktCape and cape > 0.):
      gsOpts                   = Resources()
      gsOpts.gsLineColor       = sktcolPpath
      gsOpts.gsLineDashPattern = 1         # 14
      gsOpts.gsLineThicknessF  = 2.0

      yp   = _skewty(p)
      xtp  = _skewtx(tpar, yp)
      polyline(wks, skewt_bkgd, xtp[nlLfc:nlCross+1], \
                   yp[nlLfc:nlCross+1], gsOpts)
      del gsOpts

#
#  Print geopotential if requested.
#
  if (localOpts.sktPrintZ):
    txOpts               = Resources()
    txOpts.txAngleF      = 0.
    txOpts.txFontColor   = sktcolZLabel
    txOpts.txFontHeightF = 0.9*tmYLLabelFontHeightF
#
#  Levels at which Z2 is printed.
#
    Pprint = numpy.array(                                   \
                           [1000., 850., 700., 500., 400.,  \
                             300., 250., 200., 150., 100.   \
                           ],'f')

    yz = _skewty(1000.)
    xz = _skewtx(-30., yz)        # constant "x"
    for nl in range(len(P2)):

     if ( numpy.logical_not(_ismissing(P2[nl],Pmissing)) and   \
          numpy.logical_not(_ismissing(Z2[nl],Zmissing)) and   \
          numpy.sometrue(numpy.equal(Pprint,P2[nl])) ):
       yz  = _skewty(P2[nl])
       text(wks, skewt_bkgd, str(int(Z2[nl])), xz, yz, txOpts)
    del txOpts

  if (localOpts.sktPlotWindP):
    gsOpts                   = Resources()
    gsOpts.gsLineThicknessF  = 1.0

#
#  Check if WSPD2 has a missing value attribute specified and
#  that not all WSPD2 values are missing values.
#
    if (numpy.logical_not(numpy.alltrue(_ismissing(WSPD2,WSPDmissing)))):
#
#  IDW - indices where P2/WSPD2/WDIR2 are all not missing.
#
      mv0 = numpy.logical_and(numpy.logical_not(_ismissing(P2,Pmissing)), \
            numpy.logical_not(_ismissing(WSPD2,WSPDmissing)))
      mv1 = numpy.logical_and(mv0,  \
            numpy.logical_not(_ismissing(WDIR2,WDIRmissing)))
      mv2 = numpy.logical_and(mv1,numpy.greater_equal(P2,100.))
      IDW = ind(mv2)
      if (hasattr(localOpts,"sktWthin") and localOpts.sktWthin > 1):
        nThin = localOpts.sktWthin
        idw   = IDW[::nThin]
      else:
        idw   = IDW

      pw  = numpy.take(P2,idw)

      wmsetp("wdf", 1)         # meteorological dir (Sep 2001)

#
#  Wind speed and direction.
#
      if (localOpts.sktWspdWdir):
        dirw = 0.017453 * numpy.take(WDIR2,idw)

        up   = -numpy.take(WSPD2,idw) * numpy.sin(dirw)
        vp   = -numpy.take(WSPD2,idw) * numpy.cos(dirw)
      else:
        up   = numpy.take(WSPD2,idw)      # must be u,v components
        vp   = numpy.take(WDIR2,idw)

      wbcol = wmgetp("col")                # get current wbarb color
      wmsetp("col",get_named_color_index(wks,sktcolWindP)) # set new color
      ypWind = _skewty(pw)
      xpWind = numpy.ones(len(pw),'f')
#
#  Location of wind barb.
#
      xpWind = _skewtx(45., _skewty(1013.)) * xpWind
      wmbarb(wks, xpWind, ypWind, up, vp)
      wmsetp("col",wbcol)               # restore initial color.

      mv0 = numpy.logical_and(numpy.logical_not(_ismissing( Z2,Zmissing)), \
            numpy.logical_not(_ismissing(WSPD2,WSPDmissing)))
      mv1 = numpy.logical_and(mv0, \
            numpy.logical_not(_ismissing(WDIR2,WDIRmissing)))
      mv2 = numpy.logical_and(mv1,_ismissing(P2,Pmissing))
      idz = ind(mv2)

      if (len(idz) > 0):
        zw  = numpy.take(Z2,idz)
        if (localOpts.sktWspdWdir):          # wind spd,dir (?)
          dirz = 0.017453 * numpy.take(WDIR2,idz)
          uz   = -numpy.take(WSPD2,idz) * numpy.sin(dirz)
          vz   = -numpy.take(WSPD2,idz) * numpy.cos(dirz)
        else:
          uz   = WSPD2(idz)              # must be u,v components
          vz   = WDIR2(idz)

#
#  idzp flags where Z2 and P2 have non-missing values.
#
        mv0  = numpy.logical_not(_ismissing(P2,Pmissing))
        mv1  = numpy.logical_not(_ismissing(Z2,Zmissing))
        mv2  = numpy.logical_and(mv0,mv1)
        idzp = ind(mv2)
        Zv   = numpy.take(Z2,idzp)
        Pv   = numpy.take(P2,idzp)
        pz   = ftcurv(Zv,Pv,zw)               # map zw to p levels.

        wbcol = wmgetp("col")
        wmsetp("col",get_named_color_index(wks,sktcolWindZ)) 
        yzWind = _skewty(pz)
        xzWind = numpy.ones(len(pz),'f')
        xzWind = _skewtx(45., _skewty(1013.)) * xzWind
 
        wmbarb(wks, xzWind, yzWind, uz, vz )
        wmsetp("col",wbcol)

#
#  Allows other winds to be input as attributes of sounding.
#
  if (localOpts.sktPlotWindH):
    if (hasattr(localOpts,"sktHeight") and hasattr(localOpts,"sktHspd") and  \
        hasattr(localOpts,"sktHdir")):
      dimHeight = len(localOpts.sktHeight)
      dimHspd   = len(localOpts.sktHspd  )
      dimHdir   = len(localOpts.sktHdir  )
      if (dimHeight == dimHspd and dimHeight == dimHdir and \
          numpy.logical_not(numpy.alltrue(_ismissing(localOpts.sktHeight,Hmissing)))):
        if (localOpts.sktHspdHdir):
          dirh = 0.017453 * localOpts.sktHdir
          uh   = -localOpts.sktHspd * numpy.sin(dirh)
          vh   = -localOpts.sktHspd * numpy.cos(dirh)
        else:
          uh   = localOpts.sktHspd
          vh   = localOpts.sktHdir

        mv0  = numpy.logical_not(_ismissing(P2,Pmissing))
        mv1  = numpy.logical_not(_ismissing(Z2,Zmissing))
        mv2  = numpy.logical_and(mv0,mv1)
        idzp = ind(mv2)
        Zv   = numpy.take(Z2,idzp)
        if (len(Zv) == 0):
          print ("Warning - skewt_plt: attempt to plot wind barbs at specified heights when there are no coordinates where pressure and geopotential are both defined.")
        else:
          Pv   = numpy.take(P2,idzp)
          ph   = ftcurv(Zv,Pv,localOpts.sktHeight)
          wbcol = wmgetp("col")             # get current color index
          wmsetp("col",get_named_color_index(wks,sktcolWindH)) # set new color
  
          yhWind = _skewty(ph)
          xhWind = numpy.ones(len(ph),'f')
          xhWind = _skewtx(45., _skewty(1013.)) * xhWind
          if (not yhWind is None) and (not xhWind is None):
            wmbarb(wks, xhWind, yhWind, uh, vh )
          wmsetp("col",wbcol)              # reset to initial color value
    else:
      print ("skewt_plt: sktHeightWindBarbsOn = True but sktHeightWindBarbPositions/sktHeightWindBarbSpeeds/sktHeightWindBarbDirections are missing")
  
  return skewt_bkgd

################################################################

def streamline(wks,uarray,varray,rlistc=None):
  """
Creates and draws streamlines, and returns a PlotId of the plot created.
plot = Ngl.streamline(wks, u, v, res=None)
wks -- The identifier returned from calling Ngl.open_wks
u,v -- The streamline data. Masked arrays allowed.
res -- An optional instance of the Resources class having PyNGL
       resources as attributes.
  """

# Get NumPy array from masked arrays, if necessary.
  uar2,uar_fill_value = _get_arr_and_fv(uarray)
  var2,var_fill_value = _get_arr_and_fv(varray)

  _set_spc_defaults(1)
  rlist = _crt_dict(rlistc)  
 
#  Separate the resource dictionary into those resources
#  that apply to VectorField and those that apply to
#  StreamlinePlot.
#
  rlist1 = {}
  rlist2 = {}
  rlist3 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:2] == "vf"):
      rlist1[key] = rlist[key]
    elif(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist2[key] = rlist[key]

#
# In addition, if this plot is potentially going to be overlaid
# on an Irregular Plot Class (in order to lineariize or logize it)
# then we need to keep track of all the tickmark resources, because
# we'll have to reapply them to the IrregularPlot class.
#
      if(key[0:2] == "vp" or key[0:2] == "tm" or key[0:6] == "pmTick"):
        rlist3[key] = rlist[key]
    
# Set missing value resources, if necessary
  _set_msg_val_res(rlist1,uar_fill_value,"vector_u")
  _set_msg_val_res(rlist1,var_fill_value,"vector_v")

  _set_streamline_res(rlist,rlist2)    # Set some addtl streamline resources
  _set_tickmark_res(rlist,rlist3)      # Set some addtl tickmark resources

#
#  Call the wrapped function and return.
#
  strm = streamline_wrap(wks,uar2,var2,"double","double",            \
                         uar2.shape[0],uar2.shape[1],0,              \
                         pvoid(),"",0,pvoid(),"", 0, 0, pvoid(), pvoid(),\
                         rlist1,rlist2,rlist3,pvoid())
  del rlist
  del rlist1
  del rlist2
  del rlist3
  return(_lst2pobj(strm))

################################################################

def streamline_map(wks,uarray,varray,rlistc=None):
  """
Creates and draws streamlines over a map, and returns a PlotId of the
plot created.
plot = Ngl.streamline_map(wks, u, v, res=None)
wks -- The identifier returned from calling Ngl.open_wks
u,v -- The streamline data. Masked arrays allowed.
res -- An optional instance of the Resources class having PyNGL
       resources as attributes.
  """

# Get NumPy array from masked arrays, if necessary.
  uar2,uar_fill_value = _get_arr_and_fv(uarray)
  var2,var_fill_value = _get_arr_and_fv(varray)

  _set_spc_defaults(1)
  rlist = _crt_dict(rlistc)  
 
#  Separate the resource dictionary into those resources
#  that apply to VectorField, MapPlot, and StreamlinePlot.
#
  rlist1 = {}
  rlist2 = {}
  rlist3 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:2] == "vf"):
      rlist1[key] = rlist[key]
    elif( (key[0:2] == "mp") or (key[0:2] == "vp") or (key[0:3] == "pmA") or \
          (key[0:3] == "pmO") or (key[0:3] == "pmT") or (key[0:2] == "tm") or \
          (key[0:2] == "ti") ):
      rlist3[key] = rlist[key]
    elif(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist2[key] = rlist[key]

# Set missing value resources, if necessary
  _set_msg_val_res(rlist1,uar_fill_value,"vector_u")
  _set_msg_val_res(rlist1,var_fill_value,"vector_v")

  _set_map_res(rlist,rlist3)           # Set some addtl map resources
  _set_streamline_res(rlist,rlist2)    # Set some addtl streamline resources
    
# 
# Test for masking a lambert conformal plot.
#
  mask_list = _test_for_mask_lc(rlist,rlist3)

#
#  Call the wrapped function and return.
#
  strm = streamline_map_wrap(wks,uar2,var2,"double","double",         \
                         uar2.shape[0],uar2.shape[1],0,               \
                         pvoid(),"",0,pvoid(),"", 0, 0, pvoid(), pvoid(), \
                         rlist1,rlist2,rlist3,pvoid())
  lstrm = _lst2pobj(strm) 

  if mask_list["MaskLC"]:
    lstrm = _mask_lambert_conformal(wks, lstrm, mask_list, rlist3)

  del rlist
  del rlist1
  del rlist2
  del rlist3

  return(lstrm)

################################################################

def streamline_scalar(wks,uarray,varray,tarray,rlistc=None):
  """
Creates and draws streamlines colored according to a scalar field, and
returns a PlotId of the plot created.
plot = Ngl.streamline_scalar(wks, u, v, data, res=None)
wks -- The identifier returned from calling Ngl.open_wks
u,v -- The streamline data. Masked arrays allowed.
data -- The scalar data. Masked arrays allowed.
res -- An optional instance of the Resources class having PyNGL
       resources as attributes.
  """

# Get NumPy array from masked arrays, if necessary.
  uar2,uar_fill_value = _get_arr_and_fv(uarray)
  var2,var_fill_value = _get_arr_and_fv(varray)
  tar2,tar_fill_value = _get_arr_and_fv(tarray)

  _set_spc_defaults(1)
  rlist = _crt_dict(rlistc)  
 
#  Separate the resource dictionary into those resources
#  that apply to VectorField, ScalarField, and StreamlinePlot.
#
  rlist1 = {}
  rlist2 = {}
  rlist3 = {}
  rlist4 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:2] == "vf"):
      rlist1[key] = rlist[key]
    elif(key[0:2] == "sf"):
      rlist2[key] = rlist[key]
    elif(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist3[key] = rlist[key]
#
# In addition, if this plot is potentially going to be overlaid
# on an Irregular Plot Class (in order to lineariize or logize it)
# then we need to keep track of all the tickmark resources, because
# we'll have to reapply them to the IrregularPlot class.
#
      if(key[0:2] == "vp" or key[0:2] == "tm" or key[0:6] == "pmTick"):
        rlist4[key] = rlist[key]
    
# Set missing value resources, if necessary
  _set_msg_val_res(rlist1,uar_fill_value,"vector_u")
  _set_msg_val_res(rlist1,var_fill_value,"vector_v")
  _set_msg_val_res(rlist2,tar_fill_value,"scalar")

  _set_streamline_res(rlist,rlist3)    # Set some addtl vector resources
  _set_labelbar_res(rlist,rlist3,True) # Set some addtl labelbar resources
  _set_tickmark_res(rlist,rlist4)      # Set some addtl tickmark resources

#
#  Call the wrapped function and return.
#
  ivct = streamline_scalar_wrap(wks,uar2,var2,tar2,  \
                     "double","double","double",         \
                     uar2.shape[0],uar2.shape[1],0,               \
                     pvoid(),"",0,pvoid(),"", 0, 0, 0, pvoid(), pvoid(), \
                     pvoid(),rlist1,rlist2,rlist3,rlist4,pvoid())

  del rlist
  del rlist1
  del rlist2
  del rlist3
  del rlist4
  return _lst2pobj(ivct)

################################################################

def streamline_scalar_map(wks,uarray,varray,tarray,rlistc=None):
  """
Creates and draws streamlines over a map colored according to a scalar
field, and returns a PlotId of the plot created.
plot = Ngl.streamline_scalar_map(wks, u, v, data, res=None)
wks -- The identifier returned from calling Ngl.open_wks
u,v -- The streamline data. Masked arrays allowed.
data -- The scalar data. Masked arrays allowed.
res -- An optional instance of the Resources class having PyNGL
       resources as attributes.
  """

# Get NumPy array from masked arrays, if necessary.
  uar2,uar_fill_value = _get_arr_and_fv(uarray)
  var2,var_fill_value = _get_arr_and_fv(varray)
  tar2,tar_fill_value = _get_arr_and_fv(tarray)

  _set_spc_defaults(1)
  rlist = _crt_dict(rlistc)  
 
#  Separate the resource dictionary into those resources
#  that apply to VectorField, ScalarField, MapPlot, and 
#  StreamlinePlot.
#
  rlist1 = {}
  rlist2 = {}
  rlist3 = {}
  rlist4 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:2] == "vf"):
      rlist1[key] = rlist[key]
    elif(key[0:2] == "sf"):
      rlist2[key] = rlist[key]
    elif( (key[0:2] == "mp") or (key[0:2] == "vp") or (key[0:3] == "pmA") or \
          (key[0:3] == "pmO") or (key[0:3] == "pmT") or (key[0:2] == "tm") or \
          (key[0:2] == "ti") ):
      rlist4[key] = rlist[key]
    elif(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist3[key] = rlist[key]
    
# Set missing value resources, if necessary
  _set_msg_val_res(rlist1,uar_fill_value,"vector_u")
  _set_msg_val_res(rlist1,var_fill_value,"vector_v")
  _set_msg_val_res(rlist2,tar_fill_value,"scalar")

  _set_map_res(rlist,rlist4)           # Set some addtl map resources
  _set_streamline_res(rlist,rlist3)    # Set some addtl streamline resources
  _set_labelbar_res(rlist,rlist3,True) # Set some addtl labelbar resources

# 
# Test for masking a lambert conformal plot.
#
  mask_list = _test_for_mask_lc(rlist,rlist4)

#
#  Call the wrapped function and return.
#
  ivct = streamline_scalar_map_wrap(wks,uar2,var2,tar2,  \
                     "double","double","double",         \
                     uar2.shape[0],uar2.shape[1],0,               \
                     pvoid(),"",0,pvoid(),"", 0, 0, 0, pvoid(), pvoid(), \
                     pvoid(),rlist1,rlist2,rlist3,rlist4,pvoid())

  livct = _lst2pobj(ivct)

  if mask_list["MaskLC"]:
    livct = _mask_lambert_conformal(wks, livct, mask_list, rlist4)

  del rlist
  del rlist1
  del rlist2
  del rlist3
  del rlist4
  return (livct)

################################################################

def taylor_diagram(wks, RATIO, CC, rOpts):

  #--------------------------------------------------------------------
  # This version of taylor_diagram supports "paneling"
  #--------------------------------------------------------------------

  #
  # Generate a Taylor Diagram:
  # Generate Multiple Aspects of Model Performance in a Single Diagram
  # Taylor, K. E., J. Geophys. Res., 106, D7, 7183-7192, 2001
  #
  # An example:
  # http://www.grida.no/climate/ipcc_tar/wg1/fig8-4.htm
  #
  # This expects one or more datasets. The left dimension 
  # is the number of datasets. The rightmost is the number of pts.
  #
  # Markers are at: 
  # http://www.ncl.ucar.edu/Document/Graphics/Resources/gs.shtml
  #
  # By default, the function can handle up to 10 variable comparisons..
  # To expand ...  modify the 'Colors' and 'Markers' attributes.
  # The user can change / add some default settings.
  #
  # The defaults that the user can modify:
  #
  # rOpts                       = Ngl.Resources()          # 'made-up' resources
  # rOpts.Colors                = ["blue","red","green"]
  # rOpts.Markers               = [ 2, 3, 6 ]              # Marker Indices
  # rOpts.markerTxOffset        = 0.0175                   # offset for text above marker
  # rOpts.stnRad                = [ 1. ]                   #  [ 0.50, 0.75, 1.5 ] 
  # rOpts.centerDiffRMS         = False                    #  True mean draw additional radii from REF 
  # rOpts.caseLabelsFontHeightF = 0.05
  # rOpts.varLabelsFontHeightF  = 0.013
  # rOpts.varLabelsYloc         = 0.65
  # rOpts.legendWidth           = 0.015
  # rOpts.legendHeight          = 0.030*nCase
  # rOpts.taylorDraw            = True
  # rOpts.taylorFrame           = True                     
  #                                                        # standard NCL resources
  # rOpts.tiMainString          = "Taylor"                 # not using title makes plot bigger
  # rOpts.gsMarkerSizeF         = 0.0085                   # marker size   
  # rOpts.gsMarkerThicknessF    = 1.0
  # rOpts.txFontHeightF         = 0.0125                   # text size 
  # rOpts.tiMainFontHeightF     = 0.0225                   # tiMainString size
  #
  # It returns to the user a graphic object containing the 
  # Taylor background and plotted x/y pts.
  # This graphic object contains a simple Taylor background appropriate
  # for standardized data and the markers for the datasets.
  # ==================================================================
  # This version allows paneling:
  #      The 'cumbersome' "dum" variables were added by 
  #      Adam Phillips to allow paneling via "Ngl.add_?".
  # ==================================================================
  # PyNGL version: 
  #      Fred Castruccio (fredc@ucar.edu)
  # ==================================================================

  
  dimR                  = RATIO.shape
  nCase                 = dimR[0]                   # # of cases [models] 
  nVar                  = dimR[1]                   # # of variables

                                                    # x/y coordinates for plotting
  X    = numpy.zeros( (nCase,nVar) , dtype=RATIO.dtype )
  Y    = numpy.zeros( (nCase,nVar) , dtype=RATIO.dtype )

  for nc in range(nCase):
     angle      = numpy.arccos( CC[nc,:] )             # array operation                                    
     X[nc,:]    = RATIO[nc,:] * numpy.cos( angle )     
     Y[nc,:]    = RATIO[nc,:] * numpy.sin( angle )    

  xyMin                 = 0
  xyOne                 = 1.00
  xyMax                 = 1.65
  xyMax_Panel           = xyMax+ 0.10                # paneling purposes
 
  if (rOpts and hasattr(rOpts,"txFontHeightF"))  : 
      FontHeightF       = rOpts.txFontHeightF        # user wants to specify size
  else :
      FontHeightF       = 0.0175
 
# ----------------------------------------------------------------
# Part 1:
# base plot: Based upon request of Mark Stevens
# basic x-y and draw the 1.0 observed and the outer curve at 1.65
# ----------------------------------------------------------------
  
  rxy = Resources() 
  rxy.nglDraw           = False
  rxy.nglFrame          = False
  rxy.vpHeightF         = 0.65
  rxy.vpWidthF          = 0.65
  rxy.tmYLBorderOn      = False
  rxy.tmXBBorderOn      = False

  rxy.tiYAxisString     = "Standardized Deviations (Normalized)"
  rxy.tiYAxisFontHeightF= FontHeightF                # default=0.025 
  
  rxy.tmXBMode          = "Explicit" 
  rxy.tmXBValues        = [0.0,0.25,0.50,0.75,1.00,1.25,1.5]    # major tm
  rxy.tmXBLabels        = ["    ","0.25","0.50","0.75","REF" ,"1.25","1.50"]
  if (rOpts and hasattr(rOpts,"OneX") )  :           # eg: rOpts.OneX="1.00" 
      rxy.tmXBLabels        = ["    ","0.25","0.50","0.75",rOpts.OneX,"1.25","1.50"]

  rxy.tmXBMajorLengthF  = 0.015                      # default=0.02 for a vpHeightF=0.6
  rxy.tmXBLabelFontHeightF = FontHeightF
  rxy.tmXBMinorOn       = False
  rxy.trXMaxF           = xyMax_Panel

  rxy.tmYLMode          = "Manual"
  rxy.tmYLMinorOn       = False
  rxy.tmYLMajorLengthF  = rxy.tmXBMajorLengthF
  rxy.tmYLLabelFontHeightF = FontHeightF
  rxy.tmYLMode          = "Explicit" 
  rxy.tmYLValues        = [0.0, .25, 0.50, 0.75, 1.00, 1.25, 1.5] # major tm
  rxy.tmYLLabels        = ["0.00","0.25","0.50","0.75","1.00","1.25","1.50"]
  rxy.trYMaxF           = xyMax_Panel

  rxy.tmYRBorderOn      = False
  rxy.tmYROn            = False      # Turn off right tick marks.

  rxy.tmXTBorderOn      = False
  rxy.tmXTOn            = False      # Turn off right tick marks.

  rxy.xyDashPatterns    = [ 0 ]      # line characteristics (dash,solid)
  rxy.xyLineThicknesses = [ 2.]      # choose line thickness

  rxy.nglFrame          = False      # Don't advance the frame.

                                     # create outer 'correlation axis'
  npts    = 200                      # arbitrary
  xx      = numpy.linspace(xyMin,xyMax,npts) 
  yy      = numpy.sqrt(xyMax**2 - xx**2    )   # outer correlation line (xyMax)

  sLabels = ["0.0","0.1","0.2","0.3","0.4","0.5","0.6",    # correlation labels
             "0.7","0.8","0.9","0.95","0.99","1.0"      ]  # also, major tm
  cLabels = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,
             0.7,0.8,0.9,0.95,0.99,1.0      ]
  rad     = 4. * numpy.arctan(1.0) / 180.
  angC    = numpy.arccos(cLabels) / rad                       # angles: correlation labels
                                                                       
  if (rOpts and hasattr(rOpts,"tiMainString")) :
      rxy.tiMainString      = rOpts.tiMainString
      if (hasattr(rOpts,"tiMainFontHeightF")) :
           rxy.tiMainFontHeightF = rOpts.tiMainFontHeightF
  else :
           rxy.tiMainFontHeightF = 0.0225              # default  0.025              

  taylor = xy(wks,xx,yy,rxy)                       # Create and draw XY plot.

  rsrRes  = Resources()
  rsrRes.gsLineThicknessF  = rxy.xyLineThicknesses[0]  # line thickness
  rsrRes.gsLineDashPattern = 0                         # solid line pattern
                                                       # draw x and y to xyMax
  dum0 = add_polyline(wks,taylor, [0.,  0.], [0.,xyMax], rsrRes)
  dum1 = add_polyline(wks,taylor, [0.,xyMax], [0.,  0.], rsrRes)

  xx   = numpy.linspace(xyMin, xyOne ,npts)               # draw 1.0 standard radius
  yy   = numpy.sqrt(xyOne - xx**2)   
  rsrRes.gsLineDashPattern = 1                         # dashed line pattern
  rsrRes.gsLineThicknessF  = rxy.xyLineThicknesses[0]  # line thickness
  dum2 = add_polyline(wks,taylor,xx,yy, rsrRes)
  del xx
  del yy
                               
  if (rOpts and hasattr(rOpts,"stnRad") ) :
      rsrRes.gsLineThicknessF  = 1                     # rxy.xyLineThicknesses[0]
      nStnRad = numpy.size(rOpts.stnRad)

      dum3  = []
      for n in range(nStnRad):
         rr = rOpts.stnRad[n]
         xx = numpy.linspace(xyMin, rr ,npts) 
         yy = numpy.sqrt(rr**2   - xx**2)   
         dum3.append(add_polyline(wks,taylor,xx,yy, rsrRes))

      del xx
      del yy

  tmYLLabelFont = get_integer(taylor, "tmYLLabelFont")
  tmYLLabelFontHeightF = get_integer(taylor, "tmYLLabelFontHeightF")

# ----------------------------------------------------------------
# Part 2:
# Correlation labels
# ----------------------------------------------------------------
  radC    = xyMax                                 # for correlation labels
  xC      = radC * numpy.cos(angC*rad)
  yC      = radC * numpy.sin(angC*rad)
  xC      = xC + 0.020 * numpy.cos(rad*angC)         # added to get some separation
  yC      = yC + 0.060 * numpy.sin(rad*angC)

  txRes               = Resources()           # text mods desired
  txRes.txFontHeightF = FontHeightF               # match YL 
  txRes.tmYLLabelFont = tmYLLabelFont             # match YL
  txRes.txAngleF      = -45.
  if ( not hasattr(rOpts, "drawCorLabel") or rOpts.drawCorLabel) : 
      dum4 = add_text(wks,taylor,"Correlation",1.30,1.30,txRes)
  txRes.txAngleF      = 0.0 
  txRes.txFontHeightF = FontHeightF*0.50          # bit smaller

  plRes               = Resources()
  plRes.gsLineThicknessF = 2.
  txRes.txJust        = "CenterLeft"              # Default="CenterCenter".
  txRes.txFontHeightF = FontHeightF               # match YL 
  tmEnd = 0.975
  radTM = xyMax*tmEnd                             # radius end: major TM 
  xTM   = numpy.zeros( 2 , dtype=float)
  yTM   = numpy.zeros( 2 , dtype=float)

  dum5 = []
  dum6 = []
  for i in range(numpy.size(sLabels)):               # Loop to draw strings
    txRes.txAngleF = angC[i]
    dum5.append(add_text(wks, taylor, sLabels[i],xC[i],yC[i],txRes))   # cor label
    xTM[0]   = xyMax * numpy.cos(angC[i]*rad)        # major tickmarks at
    yTM[0]   = xyMax * numpy.sin(angC[i]*rad)        # correlation labels
    xTM[1]   = radTM * numpy.cos(angC[i]*rad)             
    yTM[1]   = radTM * numpy.sin(angC[i]*rad)
    dum6.append(add_polyline(wks,taylor,xTM,yTM,plRes))
                                                  # minor tm locations
  mTM     = [0.05,0.15,0.25,0.35,0.45,0.55,0.65,
             0.75,0.85,0.91,0.92,0.93,0.94,0.96,0.97,0.98  ]
  angmTM  = numpy.arccos(mTM)/rad                    # angles: correlation labels
  radmTM  = xyMax*(1.-(1.-tmEnd)*0.5)             # radius end: minor TM 

  dum7 = []
  for i in range(numpy.size(mTM)):                   # manually add tm
    xTM[0]   = xyMax * numpy.cos(angmTM[i]*rad)      # minor tickmarks
    yTM[0]   = xyMax * numpy.sin(angmTM[i]*rad)
    xTM[1]   = radmTM * numpy.cos(angmTM[i]*rad)          
    yTM[1]   = radmTM * numpy.sin(angmTM[i]*rad)
    dum7.append(add_polyline(wks,taylor,xTM,yTM,plRes))
                                                  # added for Wanli
  if ( rOpts and hasattr(rOpts, "ccRays") ) :
      angRL = numpy.arccos(rOpts.ccRays)/rad         # angles: radial lines

      rlRes = Resources()
      rlRes.gsLineDashPattern= 2                  # line pattern
      rlRes.gsLineThicknessF = 1                  # choose line thickness
      if (hasattr(rOpts, "ccRays_color")) :
        rlRes.gsLineColor = rOpts.ccRays_color
      else :
        rlRes.gsLineColor    =  "black"

      dum8 = []
      for i in range(numpy.size(angRL)):
         xRL     = xyMax * numpy.cos(angRL[i]*rad)
         yRL     = xyMax * numpy.sin(angRL[i]*rad)
         dum8.append(add_polyline(wks,taylor, [0, xRL], [0,  yRL], rlRes))


# ----------------------------------------------------------------
# Part 3:
# Concentric about 1.0 on XB axis
# I think this is correct. Still test mode.
# ----------------------------------------------------------------
  if (rOpts and hasattr(rOpts,"centerDiffRMS") and rOpts.centerDiffRMS) :
      respl                    = Resources()     # polyline mods desired
      respl.gsLineThicknessF   = 1.0                 # line thickness
      respl.gsLineDashPattern  = 2                   # short dash lines
      respl.gsLineColor        = "black"             # line color     
      if (hasattr(rOpts,"centerDiffRMS_color")) :
          respl.gsLineColor    =  rOpts.centerDiffRMS_color

      dx   = 0.25
      ncon = 4                                       # 0.75, 0.50, 0.25, 0.0
      npts = 100                                     # arbitrary
      ang  = numpy.linspace(180,360,npts)*rad

      dum9 = []

      for n in range(ncon+1):
         rr  = n*dx                                  # radius from 1.0 [OBS] abscissa
         xx  = 1. + rr * numpy.cos(ang)
         yy  = abs( rr * numpy.sin(ang) )
         if (n <= 2) :
             dum9.append(add_polyline(wks,taylor,xx,yy,respl))
         if (n == 3) :
             n3 = int( 0.77*npts )
             dum9.append(add_polyline(wks,taylor,xx[0:n3+1],yy[0:n3+1],respl))
         if (n == 4) :
             n4 = int( 0.61*npts )
             dum9.append(add_polyline(wks,taylor,xx[0:n4+1],yy[0:n4+1],respl))
	     
      del ang
      del xx
      del yy


# ---------------------------------------------------------------
# Part 4:
# generic resources that will be applied to all users data points
# of course, these can be changed 
# http://www.ncl.ucar.edu/Document/Graphics/Resources/gs.shtml
# ---------------------------------------------------------------
  if (rOpts and hasattr(rOpts,"Markers")) :
      Markers = rOpts.Markers
  else :
      Markers = [ 4, 6, 8,  0, 9, 12, 7, 2, 11, 16]  # Marker Indices

  if (rOpts and hasattr(rOpts,"Colors")) :
      Colors  = rOpts.Colors
  else :
      Colors  = [ "red", "blue", "green", "cyan", "orange",
                  "torquoise", "brown", "yellow", "purple", "black"]

  if (rOpts and hasattr(rOpts,"gsMarkerThicknessF")) :
      gsMarkerThicknessF = rOpts.gsMarkerThicknessF
  else :
      gsMarkerThicknessF = 1.0

  if (rOpts and hasattr(rOpts,"gsMarkerSizeF")) :
      gsMarkerSizeF      = rOpts.gsMarkerSizeF
  else :
      gsMarkerSizeF      = 0.0085                    # Default: 0.007

  gsRes = Resources()
  gsRes.gsMarkerThicknessF = gsMarkerThicknessF      # default=1.0
  gsRes.gsMarkerSizeF      = gsMarkerSizeF           # Default: 0.007 

  ptRes = Resources()                            # text options for points
  ptRes.txJust             = "BottomCenter"          # Default="CenterCenter".
  ptRes.txFontThicknessF   = 1.2                     # default=1.00
  ptRes.txFontHeightF      = 0.0125                  # default=0.05
  if (rOpts and hasattr(rOpts,"txFontHeightF")) :
      ptRes.txFontHeightF  = rOpts.txFontHeightF

  markerTxYOffset          = 0.0175                  # default
  if (rOpts and hasattr(rOpts,"markerTxYOffset")) :
      markerTxYOffset = rOpts.markerTxYOffset        # user defined offset

  dum10 = []
  dum11 = []

  for n in range(nCase):
     gsRes.gsMarkerIndex   = Markers[n]              # marker style (+)
     gsRes.gsMarkerColor   = Colors[n]               # marker color
     ptRes.txFontColor     = gsRes.gsMarkerColor
     for i in range(nVar) :
       dum10.append(add_polymarker(wks,taylor,X[n,i],Y[n,i],gsRes))
       print ('X(n,i) = %f  Y(n,i) = %f' %(X[n,i], Y[n,i]))
       dum11.append(add_text(wks,taylor,str(i+1),X[n,i],Y[n,i]+markerTxYOffset,ptRes))


# ---------------------------------------------------------------
# Part 5: # add case legend and variable labels
# ---------------------------------------------------------------

#  if (rOpts and hasattr(rOpts,"caseLabels")) : 

#      if (hasattr(rOpts,"caseLabelsFontHeightF")) :
#          caseLabelsFontHeightF = rOpts.caseLabelsFontHeightF
#      else :
#          caseLabelsFontHeightF = 0.05  

#      lgres                    = Resources()
#      lgres.lgMarkerColors     = Colors        # colors of markers
#      lgres.lgMarkerIndexes    = Markers       # Markers 
#      lgres.lgMarkerSizeF      = gsMarkerSizeF # Marker size
#      lgres.lgItemType         = "Markers"     # draw markers only
#      lgres.lgLabelFontHeightF = caseLabelsFontHeightF  # font height of legend case labels

#      if (hasattr(rOpts,"legendWidth")) :
#          lgres.vpWidthF       = rOpts.legendWidth
#      else :
#          lgres.vpWidthF       = 0.15          # width of legend (NDC)

#      if (hasattr(rOpts,"legendHeight")) :
#          lgres.vpHeightF      = rOpts.legendHeight
#      else :
#          lgres.vpHeightF      = 0.030*nCase   # height of legend (NDC)

#      lgres.lgPerimOn          = False         # turn off perimeter
#      nModel                   = numpy.size( rOpts.caseLabels )
#      print nModel, rOpts.caseLabels
#      lbid = legend_ndc(wks,nModel,rOpts.caseLabels,0.35,-0.35,lgres)
	 
  if (rOpts and hasattr(rOpts,"caseLabels")) : 
    nCase    = numpy.size(rOpts.caseLabels)
      
    if (hasattr(rOpts,"caseLabelsFontHeightF")) :
      caseLabelsFontHeightF = rOpts.caseLabelsFontHeightF
    else :
      caseLabelsFontHeightF = 0.05 

      txres = Resources()
      txres.txFontHeightF = caseLabelsFontHeightF
      txres.txJust = "CenterLeft"              # justify to the center left

      delta_y = 0.1   
      delta_x = 0.05  
      if (rOpts and hasattr(rOpts,"caseLabelsXloc")) :
          xs  = rOpts.caseLabelsXloc            # user specified
      else :
          xs  = 1.                
      
      if (rOpts and hasattr(rOpts,"caseLabelsYloc")) :
          ys  = rOpts.caseLabelsYloc            # user specified
      else :
          ys  = max( [nCase*delta_y , 0.30]) 
	  
      gsres               = Resources()
      gsres.gsMarkerSizeF = gsMarkerSizeF
      
      for i in range(nCase):     
         if (i==0) :
             dum12 = []
             dum13 = []
	     
         gsres.gsMarkerColor	 = Colors[i]	 # colors of markers
         gsres.gsMarkerIndex	 = Markers[i]	 # Markers 
         dum13.append(add_polymarker(wks, taylor, xs-delta_x, ys, gsres) )   # Draw a polymarker.

         txres.txFontColor     = Colors[i]        # colors of markers
         dum12.append(add_text(wks,taylor, rOpts.caseLabels[i], xs, ys, txres))
         ys = ys- delta_y
  
  if (rOpts and hasattr(rOpts,"varLabels")) : 
      nVar    = numpy.size(rOpts.varLabels)

      if (hasattr(rOpts,"varLabelsFontHeightF")) :
          varLabelsFontHeightF = rOpts.varLabelsFontHeightF
      else :
          varLabelsFontHeightF = 0.013

      txres = Resources()
      txres.txFontHeightF = varLabelsFontHeightF
      txres.txJust = "CenterLeft"              # justify to the center left

      delta_y = 0.06   
      if (rOpts and hasattr(rOpts,"varLabelsYloc")) :
          ys  = rOpts.varLabelsYloc            # user specified
      else :
          ys  = max( [nVar*delta_y , 0.30])
      
      for i in range(nVar):     
            if (i==0) :
              dum12 = []

              dum12.append(add_text(wks,taylor, str(i+1) + " - " + rOpts.varLabels[i], .125,ys,txres))
              ys = ys- delta_y
  
  if (not hasattr(rOpts,"taylorDraw") or \
      (hasattr(rOpts,"taylorDraw") and rOpts.taylorDraw)) : 
	    draw(taylor)
  if (not hasattr(rOpts,"taylorFrame") or \
      (hasattr(rOpts,"taylorFrame") and rOpts.taylorFrame)) : 
      frame(wks)

  return taylor



################################################################

def text(wks, plot, text, x, y, rlistc=None):
  """
Draws text strings on an existing plot.
txt = Ngl.text(wks, plot, text, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
plot -- The id of the plot which you want to draw the text strings on.
text -- An array of text strings.
x, y -- One-dimensional arrays containing the x, y coordinates of the
        text strings, which must be in the same coordinate space as
        the plot.
res -- An optional variable containing a list of TextItem resources,
       attached as attributes.
  """
  _set_spc_defaults(0)
  rlist = _crt_dict(rlistc)
  rlist1 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist1[key] = rlist[key]
  itxt = text_wrap(wks,_pobj2lst(plot),text,x,y,"double","double",rlist1,pvoid())
  del rlist
  del rlist1
  return(_lst2pobj(itxt))

################################################################

def text_ndc(wks, text, x, y, rlistc=None):
  """
Draws text strings on the viewport.
txt = Ngl.text_ndc(wks, text, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
text -- An array of text strings.
x, y -- Scalars, one-dimensional NumPy arrays, or Python lists
        containing the x, y NDC coordinates (values from 0 to 1) of
        the text strings.
res -- An (optional) instance of the Resources class having TextItem
       resources as attributes.
  """
  _set_spc_defaults(0)
  rlist = _crt_dict(rlistc)
  rlist1 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist1[key] = rlist[key]

  itxt = text_ndc_wrap(wks,text,x,y,"double","double",rlist1,pvoid())
  del rlist
  del rlist1
  return (_lst2pobj(itxt))

################################################################

def update_workstation(obj):
  """
Flushes all output to a specified workstation.
Ngl.update_workstation(wks)
wks -- The identifier returned from calling Ngl.open_wks.
  """
  NhlUpdateWorkstation(_int_id(obj))

################################################################

def vector(wks,uarray,varray,rlistc=None):
  """
Creates and draws vectors, and returns a PlotId of the plot created.
plot = Ngl.vector(wks, u, v, res=None)
wks -- The identifier returned from calling Ngl.open_wks
u,v -- The vector data. Masked arrays allowed.
res -- An optional instance of the Resources class having PyNGL
       resources as attributes.
  """
#
#  Make sure the arrays are 2D.
#
  if len(uarray.shape) != 2 or len(varray.shape) != 2:
    print ("vector - arrays must be 2D")
    return None

# Get NumPy array from masked arrays, if necessary.
  uar2,uar_fill_value = _get_arr_and_fv(uarray)
  var2,var_fill_value = _get_arr_and_fv(varray)

  _set_spc_defaults(1)
  rlist = _crt_dict(rlistc)  
 
#  Separate the resource dictionary into those resources
#  that apply to VectorField and those that apply to
#  VectorPlot.
#
  rlist1 = {}
  rlist2 = {}
  rlist3 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:2] == "vf"):
      rlist1[key] = rlist[key]
    elif(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist2[key] = rlist[key]
#
# In addition, if this plot is potentially going to be overlaid
# on an Irregular Plot Class (in order to lineariize or logize it)
# then we need to keep track of all the tickmark resources, because
# we'll have to reapply them to the IrregularPlot class.
#
      if(key[0:2] == "vp" or key[0:2] == "tm" or key[0:6] == "pmTick"):
        rlist3[key] = rlist[key]
    
# Set missing value resources, if necessary
  _set_msg_val_res(rlist1,uar_fill_value,"vector_u")
  _set_msg_val_res(rlist1,var_fill_value,"vector_v")

  _set_vector_res(rlist,rlist2)        # Set some addtl vector resources
  _set_labelbar_res(rlist,rlist2,True) # Set some addtl labelbar resources
  _set_tickmark_res(rlist,rlist3)      # Set some addtl tickmark resources

#
#  Call the wrapped function and return.
#
  ivct = vector_wrap(wks,uar2,var2,"double","double",             \
                     uar2.shape[0],uar2.shape[1],0,               \
                     pvoid(),"",0,pvoid(),"", 0, 0, pvoid(), pvoid(), \
                     rlist1,rlist2,rlist3,pvoid())
  del rlist
  del rlist1
  del rlist2
  del rlist3
  return _lst2pobj(ivct)

################################################################

def vector_map(wks,uarray,varray,rlistc=None):
  """
Creates and draws vectors over a map, and returns a PlotId of the plot
created.
plot = Ngl.vector_map(wks, u, v, res=None)
wks -- The identifier returned from calling Ngl.open_wks
u,v -- The vector data. Masked arrays allowed.
res -- An optional instance of the Resources class having PyNGL
       resources as attributes.
  """
#
#  Make sure the arrays are 2D.
#
  if len(uarray.shape) != 2 or len(varray.shape) != 2:
    print ("vector_map - arrays must be 2D")
    return None

# Get NumPy array from masked arrays, if necessary.
  uar2,uar_fill_value = _get_arr_and_fv(uarray)
  var2,var_fill_value = _get_arr_and_fv(varray)

  _set_spc_defaults(1)
  rlist = _crt_dict(rlistc)  
 
#  Separate the resource dictionary into those resources
#  that apply to VectorField, MapPlot, and VectorPlot.
#
  rlist1 = {}
  rlist2 = {}
  rlist3 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:2] == "vf"):
      rlist1[key] = rlist[key]
    elif( (key[0:2] == "mp") or (key[0:2] == "vp") or (key[0:3] == "pmA") or \
          (key[0:3] == "pmO") or (key[0:3] == "pmT") or (key[0:2] == "tm") or \
          (key[0:2] == "ti") ):
      rlist3[key] = rlist[key]
    elif(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist2[key] = rlist[key]

# Set missing value resources, if necessary
  _set_msg_val_res(rlist1,uar_fill_value,"vector_u")
  _set_msg_val_res(rlist1,var_fill_value,"vector_v")

  _set_map_res(rlist,rlist3)           # Set some addtl map resources
  _set_vector_res(rlist,rlist2)        # Set some addtl vector resources
  _set_labelbar_res(rlist,rlist2,True) # Set some addtl labelbar resources
    
# 
# Test for masking a lambert conformal plot.
#
  mask_list = _test_for_mask_lc(rlist,rlist3)

#
#  Call the wrapped function and return.
#
  ivct = vector_map_wrap(wks,uar2,var2,"double","double",         \
                     uar2.shape[0],uar2.shape[1],0,               \
                     pvoid(),"",0,pvoid(),"", 0, 0, pvoid(), pvoid(), \
                     rlist1,rlist2,rlist3,pvoid())

  livct = _lst2pobj(ivct)

  if mask_list["MaskLC"]:
    livct = _mask_lambert_conformal(wks, livct, mask_list, rlist3)

  del rlist
  del rlist1
  del rlist2
  del rlist3
  return (livct)

################################################################

def vector_scalar(wks,uarray,varray,tarray,rlistc=None):
  """
Creates and draws vectors colored according to a scalar field, and
returns a PlotId of the plot created.
plot = Ngl.vector_scalar(wks, u, v, data, res=None)
wks -- The identifier returned from calling Ngl.open_wks
u,v -- The vector data. Masked arrays allowed.
data -- The scalar data. Masked arrays allowed.
res -- An optional instance of the Resources class having PyNGL
       resources as attributes.
  """
#
#  Make sure the arrays are 2D.
#
  if len(uarray.shape) != 2 or len(varray.shape) != 2 or \
     len(tarray.shape) != 2:
    print ("vector_scalar - arrays must be 2D")
    return None

# Get NumPy array from masked arrays, if necessary.
  uar2,uar_fill_value = _get_arr_and_fv(uarray)
  var2,var_fill_value = _get_arr_and_fv(varray)
  tar2,tar_fill_value = _get_arr_and_fv(tarray)

  _set_spc_defaults(1)
  rlist = _crt_dict(rlistc)  
 
#  Separate the resource dictionary into those resources
#  that apply to VectorField, ScalarField, and VectorPlot.
#
  rlist1 = {}
  rlist2 = {}
  rlist3 = {}
  rlist4 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:2] == "vf"):
      rlist1[key] = rlist[key]
    elif(key[0:2] == "sf"):
      rlist2[key] = rlist[key]
    elif(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist3[key] = rlist[key]
#
# In addition, if this plot is potentially going to be overlaid
# on an Irregular Plot Class (in order to lineariize or logize it)
# then we need to keep track of all the tickmark resources, because
# we'll have to reapply them to the IrregularPlot class.
#
      if(key[0:2] == "vp" or key[0:2] == "tm" or key[0:6] == "pmTick"):
        rlist4[key] = rlist[key]
    
# Set missing value resources, if necessary
  _set_msg_val_res(rlist1,uar_fill_value,"vector_u")
  _set_msg_val_res(rlist1,var_fill_value,"vector_v")
  _set_msg_val_res(rlist2,tar_fill_value,"scalar")

  _set_vector_res(rlist,rlist3)        # Set some addtl vector resources
  _set_labelbar_res(rlist,rlist3,True) # Set some addtl labelbar resources
  _set_tickmark_res(rlist,rlist4)      # Set some addtl tickmark resources

#
#  Call the wrapped function and return.
#
    
  ivct = vector_scalar_wrap(wks,uar2,var2,tar2,  \
                     "double","double","double",         \
                     uar2.shape[0],uar2.shape[1],0,               \
                     pvoid(),"",0,pvoid(),"", 0, 0, 0, pvoid(), pvoid(), \
                     pvoid(),rlist1,rlist2,rlist3,rlist4,pvoid())

  del rlist
  del rlist1
  del rlist2
  del rlist3
  del rlist4
  return _lst2pobj(ivct)

################################################################

def vector_scalar_map(wks,uarray,varray,tarray,rlistc=None):
  """
Creates and draws vectors over a map colored according to a scalar
field, and returns a PlotId of the plot created.
plot = Ngl.vector_scalar_map(wks, u, v, data, res=None)
wks -- The identifier returned from calling Ngl.open_wks
u,v -- The vector data. Masked arrays allowed.
data -- The scalar data. Masked arrays allowed.
res -- An optional instance of the Resources class having PyNGL
       resources as attributes.
  """
#
#  Make sure the arrays are 2D.
#
  if len(uarray.shape) != 2 or len(varray.shape) != 2 or \
     len(tarray.shape) != 2:
    print ("vector_scalar_map - arrays must be 2D")
    return None

# Get NumPy array from masked arrays, if necessary.
  uar2,uar_fill_value = _get_arr_and_fv(uarray)
  var2,var_fill_value = _get_arr_and_fv(varray)
  tar2,tar_fill_value = _get_arr_and_fv(tarray)

  _set_spc_defaults(1)
  rlist = _crt_dict(rlistc)  
 
#  Separate the resource dictionary into those resources
#  that apply to VectorField, ScalarField, MapPlot, and 
#  VectorPlot.
#
  rlist1 = {}
  rlist2 = {}
  rlist3 = {}
  rlist4 = {}
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
    if (key[0:2] == "vf"):
      rlist1[key] = rlist[key]
    elif(key[0:2] == "sf"):
      rlist2[key] = rlist[key]
    elif( (key[0:2] == "mp") or (key[0:2] == "vp") or (key[0:3] == "pmA") or \
          (key[0:3] == "pmO") or (key[0:3] == "pmT") or (key[0:2] == "tm") or \
          (key[0:2] == "ti") ):
      rlist4[key] = rlist[key]
    elif(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      rlist3[key] = rlist[key]
    
# Set missing value resources, if necessary
  _set_msg_val_res(rlist1,uar_fill_value,"vector_u")
  _set_msg_val_res(rlist1,var_fill_value,"vector_v")
  _set_msg_val_res(rlist2,tar_fill_value,"scalar")

  _set_map_res(rlist,rlist4)           # Set some addtl map resources
  _set_vector_res(rlist,rlist3)        # Set some addtl vector resources
  _set_labelbar_res(rlist,rlist3,True) # Set some addtl labelbar resources

# 
# Test for masking a lambert conformal plot.
#
  mask_list = _test_for_mask_lc(rlist,rlist4)

#
#  Call the wrapped function and return.
#
  ivct = vector_scalar_map_wrap(wks,uar2,var2,tar2,  \
                     "double","double","double",         \
                     uar2.shape[0],uar2.shape[1],0,               \
                     pvoid(),"",0,pvoid(),"", 0, 0, 0, pvoid(), pvoid(), \
                     pvoid(),rlist1,rlist2,rlist3,rlist4,pvoid())

  livct = _lst2pobj(ivct)

  if mask_list["MaskLC"]:
    livct = _mask_lambert_conformal(wks, livct, mask_list, rlist4)

  del rlist
  del rlist1
  del rlist2
  del rlist3
  del rlist4
  return (livct)

################################################################

def vinth2p(datai, hbcofa, hbcofb, plevo, psfc, intyp, p0, ii, kxtrp):     
  """
Interpolates CCSM hybrid coordinates to pressure coordinates.  A
multi-dimensional NumPy array of the same shape as datai is
returned, except that the input level coordinate is replaced by
plevo.
array = Ngl.vinth2p(datai, hbcofa, hbcofb, plevo, psfc, intyp, p0, ilev,
                    kxtrp)
datai -- A NumPy array of 3 or 4 dimensions. This array needs to
         contain a level dimension in hybrid coordinates. The order of
         the dimensions is specific. The three rightmost dimensions
         must be level x lat x lon [e.g. TS(time,lev,lat,lon)]. The
         order of the level dimension must be top-to-bottom.
hbcofa -- A one-dimensional NumPy array or Python list containing
          the hybrid A coefficients. Must have the same dimension as
          the level dimension of datai. The order must be
          top-to-bottom.
hbcofb -- A one-dimensional NumPy array or Python list containing
          the hybrid B coefficients. Must have the same dimension as
          the level dimension of datai. The order must be
          top-to-bottom.
plevo -- A one-dimensional NumPy array of output pressure levels in
         mb.
psfc -- A multi-dimensional NumPy array of surface pressures in
        Pa. Must have the same dimension sizes as the corresponding
        dimensions of datai.
intyp -- A scalar integer value equal to the interpolation type: 1 =
         LINEAR, 2 = LOG, 3 = LOG LOG.
p0 -- A scalar value equal to surface reference pressure in mb.
ilev -- Not used at this time. Set to 1.
kxtrp -- A logical value. If False, then no extrapolation is done when
         the pressure level is outside of the range of psfc.
  """

  return fplib.vinth2p(datai, hbcofa, hbcofb, plevo, psfc, 
                       intyp, p0, ii, kxtrp)

################################################################

def wmbarb(wks,x,y,u,v):
  """
Draws wind barbs at specified locations.
Ngl.wmbarb(wks, x, y, dx, dy)
wks -- The identifier returned from calling Ngl.open_wks.
x, y -- Scalars, one-dimensional NumPy arrays or Python lists
        specifying X and Y coordinate values.
dx, dy -- Scalars, one-dimensional NumPy arrays or Python lists
          specifying X and Y components of wind vectors at the
          associated (x,y) coordinates.
  """
#
#  Get the GKS workstaton ID.
#
  gksid = get_integer(wks,"wkGksWorkId")

#
#  Process depending on whether we have scalar coordinates,
#  NumPy arrays, or Python lists or tuples.
#
  t = type(numpy.array([0],'i'))
  if (type(x) == t):
    if ( (type(y) != t) or (type(u) != t) or (type(v) != t)):
      print ("wmbarb: If any argument is a NumPy array, they must all be.")
      return 1
    rx = numpy.ravel(x)
    ry = numpy.ravel(y)
    ru = numpy.ravel(u)
    rv = numpy.ravel(v)
    for i in range(len(rx)):
      c_wmbarbp(gksid,rx[i],ry[i],ru[i],rv[i])
  elif(type(x) == types.ListType):
    l = types.ListType
    if ( (type(y) != l) or (type(u) != l) or (type(v) != l)):
      print ("wmbarb: If any argument is a Python list, they must all be.")
      return 1
    for i in range(len(x)):
      c_wmbarbp(gksid,x[i],y[i],u[i],v[i])
  elif(type(x) == types.TupleType):
    l = types.TupleType
    if ( (type(y) != l) or (type(u) != l) or (type(v) != l)):
      print ("wmbarb: If any argument is a Python tuple, they must all be.")
      return 1
    for i in range(len(x)):
      c_wmbarbp(gksid,x[i],y[i],u[i],v[i])
  elif (type(x)==types.IntType or type(x)==types.LongType or \
        type(x)==types.FloatType):
    c_wmbarbp(gksid,x,y,u,v)
  return 0

################################################################

def wmbarbmap(wks,x,y,u,v):
  """
Draws wind barbs over maps at specified locations.
Ngl.wmbarbmap(wks, lat, lon, u, v)
wks -- The identifier returned from calling Ngl.open_wks.
lat, lon -- Scalars, one-dimensional NumPy arrays or Python lists
            specifying latitude and longitude coordinate values (in
            degrees).
u, v -- Scalars, one-dimensional NumPy arrays or Python lists
        specifying the zonal and meridional "x" and "y" wind
        components at the associated lat,lon coordinates.
  """
  ezf = wmgetp("ezf")
  wdf = wmgetp("wdf")
  wmsetp("ezf",1)
  wmsetp("wdf",1)
  wmbarb(wks,x,y,u,v)
  wmsetp("ezf",ezf)
  wmsetp("wdf",wdf)

################################################################

def wmgetp(pname):
  """
Retrieves control parameter values for the Ngl.wmbarb and Ngl.wmbarbmap
procedures.
value = Ngl.wmgetp(pname)
pname -- Name of the parameter whose value you want to retrieve.
value -- The return value of the given input parameter.
  """
  iparms = [                                                                \
             "alo", "aoc", "asc", "awc", "cbc", "cc1", "cc2", "cc3", "cfc", \
             "col", "dbc", "dtc", "hib", "hic", "hif", "his", "lc1", "lc2", \
             "lc3", "lob", "lof", "los", "mxs", "nbz", "nms", "pai", "rbs", \
             "rc1", "rc2", "rc3", "rc4", "rc5", "rev", "rfc", "rls", "ros", \
             "sc1", "sc2", "sc3", "sc4", "slf", "sty", "t1c", "t2c", "wbf", \
             "wfc", "wty", "ezf", "smf", "loc", "wdf", "unt",               \
             "ALO", "AOC", "ASC", "AWC", "CBC", "CC1", "CC2", "CC3", "CFC", \
             "COL", "DBC", "DTC", "HIB", "HIC", "HIF", "HIS", "LC1", "LC2", \
             "LC3", "LOB", "LOF", "LOS", "MXS", "NBZ", "NMS", "PAI", "RBS", \
             "RC1", "RC2", "RC3", "RC4", "RC5", "REV", "RFC", "RLS", "ROS", \
             "SC1", "SC2", "SC3", "SC4", "SLF", "STY", "T1C", "T2C", "WBF", \
             "WFC", "WTY", "EZF", "SMF", "LOC", "WDF", "UNT"                \
           ] 

  rparms = [                                                                \
             "arc", "ard", "arl", "ars", "beg", "bet", "cht", "cmg", "cs1", \
             "cs2", "dts", "dwd", "end", "lin", "lwd", "oer", "rht", "rmg", \
             "sht", "sig", "sl1", "sl2", "smt", "swi", "tht", "wba", "wbc", \
             "wbd", "wbl", "wbr", "wbs", "wbt", "wht", "blw",               \
             "ARC", "ARD", "ARL", "ARS", "BEG", "BET", "CHT", "CMG", "CS1", \
             "CS2", "DTS", "DWD", "END", "LIN", "LWD", "OER", "RHT", "RMG", \
             "SHT", "SIG", "SL1", "SL2", "SMT", "SWI", "THT", "WBA", "WBC", \
             "WBD", "WBL", "WBR", "WBS", "WBT", "WHT", "BLW"                \
           ]

  cparms = [ "erf", "fro", "ERF", "FRO" ]

  if (not isinstance(pname,types.StringType)):
    print ("wmgetp: Parameter '" + str(pname) + "' is not a string type." )
    return None
  if (iparms.count(pname) > 0):
    return c_wmgetip(pname)
  elif (rparms.count(pname) > 0):
    return c_wmgetrp(pname)
  elif (cparms.count(pname) > 0):
    return c_wmgetcp(pname)
  else:
    print (\
      "wmgetp: specified value for " + pname + " is not of a recognized type.")
  return None

################################################################

def wmsetp(pname,val):
  """
Sets control parameter values for Ngl.wmbarb and Ngl.wmbarbmap procedures.
Ngl.wmsetp(pname, pvalue)
pname -- Name of the parameter to set.
pvalue -- Value of the parameter you want to set.
  """
  if (not isinstance(pname,types.StringType)):
    print ("wmsetp: Parameter '" + str(pname) + "' is not a string type." )
    return None
  if (isinstance(val,types.FloatType)):
    c_wmsetrp(pname,val)
  elif (isinstance(val,types.IntType)): 
    c_wmsetip(pname,val)
  elif (isinstance(val,types.StringType)):
    c_wmsetcp(pname,val)
  else:
    print (\
      "wmsetp: specified value for " + pname + " is not of a recognized type.")
  return None

################################################################

def wmstnm(wks,x,y,imdat):
  """
Draws station model data at specified locations.
Ngl.wmstnm(wks, x, y, imdat)
wks -- The identifier returned from calling Ngl.open_wks.
x, y -- Scalars, one-dimensional NumPy arrays or Python lists
        specifying X and Y coordinate values.
imdat -- A string of 50 characters encoded as per the WMO/NOAA guidelines. 
         See the online documentation for details.
  """
#
#  Get the GKS workstaton ID.
#
  gksid = get_integer(wks,"wkGksWorkId")

#
#  Process depending on whether we have scalar coordinates,
#  NumPy arrays, or Python lists or tuples.
# 
  xa = _arg_with_scalar(numpy.array(x))
  ya = _arg_with_scalar(numpy.array(y))
  if (type(imdat) == type('a')):
    imdata = numpy.array([imdat])
  else:
    imdata = numpy.array(imdat)
  for i in xrange(len(xa)):
    c_wmstnmp(gksid,xa[i],ya[i],imdata[i])

  del xa,ya,imdata
  return None

################################################################

def wrf_avo(u, v, msfu, msfv, msfm, cor, dx, dy, opt=0):
  """
Calculates absolute vorticity from WRF model output.
u - X-wind component. An array whose rightmost three dimensions are
bottom_top x south_north x west_east_stag.
v -- Y-wind component. An array whose rightmost three dimensions are
bottom_top x south_north_stag x west_east, and whose leftmost
dimensions are the same as u's.
msfu -- Map scale factor on u-grid. An array whose rightmost two
dimensions are the same as u's. If it contains additional leftmost
dimensions, they must be the same as the u and v arrays.
msfv -- Map scale factor on v-grid. An array with the same number of
dimensions as msfu, whose rightmost two dimensions are the same as
v's. If it contains additional leftmost dimensions, they must be the
same as the u and v arrays.
msfm -- Map scale factor on mass grid. An array with the same number
of dimensions as msfu and msfv, whose rightmost two dimensions are
south_north x west_east. If it contains additional leftmost
dimensions, they must be the same as the u and v arrays.
cor -- Coriolis sine latitude term. An array of the same
dimensionality as msfm.
dx -- A scalar representing the grid spacing in X.
dy -- A scalar representing the grid spacing in Y.
opt -- [optional] An integer option, not in use yet. Set to 0.
  """

  u2    = _promote_scalar(u)
  v2    = _promote_scalar(v)
  msfu2 = _promote_scalar(msfu)
  msfv2 = _promote_scalar(msfv)
  msfm2 = _promote_scalar(msfm)
  cor2  = _promote_scalar(cor)
  dx2   = _promote_scalar(dx)
  dy2   = _promote_scalar(dy)

  return fplib.wrf_avo(u2,v2,msfu2,msfv2,msfm2,cor2,dx2,dy2,opt)

################################################################

def wrf_dbz(P, T, qv, qr, qs=None, qg=None, ivarint=0, iliqskin=0):
  """
Calculates simulated equivalent radar reflectivity factor [dBZ] from
WRF model output.
dbz = Ngl.wrf_dbz (P, T, qv, qr, qs, qg, ivarint, iliqskin)
P -- Full pressure (perturbation + base state pressure). The rightmost
dimensions are bottom_top x south_north x west_east. Units must be
[Pa].
T -- Temperature in [K]. An array with the same dimensionality as
P. This variable can be calculated by wrf_tk.
qv -- Water vapor mixing ratio in [kg/kg]. An array with the same
dimensionality as P.
qr -- Rain mixing ratio in [kg/kg]. An array with the same
dimensionality as P.
qs -- [optional] Snow mixing ratio in [kg/kg]. A scalar or an array
with the same dimensionality as P.  If not set, a scalar value of 0.0
will be used.
qg -- [optional] Graupel mixing ratio in [kg/kg]. A scalar or array
with the same dimensionality as P. If not set, a scalar value of 0.0
will be used.
ivarint -- [optional, default=0] A scalar option for the behavior of
intercept parameters for the size distributions of rain, snow, and
graupel. See description below.
iliqskin -- [optional, default=0] A scalar option for scattering. If set to 1,
frozen particles that are at a temperature above freezing will be
assumed to scatter as a liquid particle.
  """

#
# Promote p and theta to numpy arrays that have at least a dimension of 1.
#
  p2  = _promote_scalar(P)
  t2  = _promote_scalar(T)
  qv2 = _promote_scalar(qv)
  qr2 = _promote_scalar(qr)

  zero = 0.0
  if not qs is None:
    if _is_scalar(qs):
      qs2 = numpy.zeros(qv.shape)
      qs2[:] = qs
    else:
      qs2 = _promote_scalar(qs)
  else:
    qs2 = numpy.zeros(qv.shape)
  if not qg is None:
    if _is_scalar(qg):
      qg2 = numpy.zeros(qv.shape)
      qg2[:] = qg
    else:
      qg2 = _promote_scalar(qg)
  else:
    qg2 = numpy.zeros(qv.shape)

  ivar2 = _promote_scalar(ivarint)
  iliq2 = _promote_scalar(iliqskin)
  return fplib.wrf_dbz(p2,t2,qv2,qr2,qs2,qg2,ivar2,iliq2)

################################################################

def wrf_ll_to_ij(lon, lat, map_proj, truelat1=-999.,truelat2=-999.,stand_lon=999., \
                 ref_lat=-999,ref_lon=-999,pole_lat=90,pole_lon=0,knowni=-999,\
                 knownj=-999,dx=-999, dy=-999, latinc=-999., loninc=-999):
  """
Converts lon/lat values to i/j index values.
lon,lat - lat,lon values to convert
map_proj -- map projection
  """

  lon2       = _promote_scalar(lon)
  lat2       = _promote_scalar(lat)
  map_proj2  = _promote_scalar(map_proj)
  truelat12  = _promote_scalar(truelat1)
  truelat22  = _promote_scalar(truelat2)
  stand_lon2 = _promote_scalar(stand_lon)
  ref_lat2   = _promote_scalar(ref_lat)
  ref_lon2   = _promote_scalar(ref_lon)
  pole_lat2  = _promote_scalar(pole_lat)
  pole_lon2  = _promote_scalar(pole_lon)
  knowni2    = _promote_scalar(knowni)
  knownj2    = _promote_scalar(knownj)
  dx2        = _promote_scalar(dx)
  dy2        = _promote_scalar(dy)
  latinc2    = _promote_scalar(latinc)
  loninc2    = _promote_scalar(loninc)

  return fplib.wrf_ll_to_ij(lon2,lat2,map_proj2,truelat12,truelat22,stand_lon2, \
                            ref_lat2,ref_lon2,pole_lat2,pole_lon2,knowni2, knownj2,\
                            dx2, dy2, latinc2,loninc2)

################################################################

def wrf_ij_to_ll(iloc, jloc, map_proj, truelat1=-999.,truelat2=-999.,stand_lon=999., \
                 ref_lat=-999,ref_lon=-999,pole_lat=90,pole_lon=0,knowni=-999,\
                 knownj=-999,dx=-999, dy=-999, latinc=-999., loninc=-999):
  """
Converts i/j index values to lon/lat values.
lon,lat - lat,lon values to convert
map_proj -- map projection
  """

  iloc2      = _promote_scalar(iloc)
  jloc2      = _promote_scalar(jloc)
  map_proj2  = _promote_scalar(map_proj)
  truelat12  = _promote_scalar(truelat1)
  truelat22  = _promote_scalar(truelat2)
  stand_lon2 = _promote_scalar(stand_lon)
  ref_lat2   = _promote_scalar(ref_lat)
  ref_lon2   = _promote_scalar(ref_lon)
  pole_lat2  = _promote_scalar(pole_lat)
  pole_lon2  = _promote_scalar(pole_lon)
  knowni2    = _promote_scalar(knowni)
  knownj2    = _promote_scalar(knownj)
  dx2        = _promote_scalar(dx)
  dy2        = _promote_scalar(dy)
  latinc2    = _promote_scalar(latinc)
  loninc2    = _promote_scalar(loninc)

  return fplib.wrf_ll_to_ij(iloc2,jloc2,map_proj2,truelat12,truelat22,stand_lon2, \
                            ref_lat2,ref_lon2,pole_lat2,pole_lon2,knowni2, knownj2,\
                            dx2, dy2, latinc2,loninc2)

################################################################

def wrf_pvo(u, v, th, p, msfu, msfv, msfm, cor, dx, dy, opt=0):
  """
Calculates potential vorticity from WRF model output.
u - X-wind component. An array whose rightmost three dimensions are
bottom_top x south_north x west_east_stag.
v -- Y-wind component. An array whose rightmost three dimensions are
bottom_top x south_north_stag x west_east, and whose leftmost
dimensions are the same as u's.
theta -- Potential temperature in K. An array whose rightmost
dimensions are bottom_top x south_north x west_east, and whose
leftmost dimensions are the same as u's.
P -- Full pressure (perturbation + base state pressure). An array with
the same dimensionality as theta. Units must be [Pa].
msfu -- Map scale factor on u-grid. An array whose rightmost two
dimensions are the same as u's. If it contains additional leftmost
dimensions, they must be the same as the u and v arrays.
msfv -- Map scale factor on v-grid. An array with the same number of
dimensions as msfu, whose rightmost two dimensions are the same as
v's. If it contains additional leftmost dimensions, they must be the
same as the u and v arrays.
msfm -- Map scale factor on mass grid. An array with the same number
of dimensions as msfu and msfv, whose rightmost two dimensions are
south_north x west_east. If it contains additional leftmost
dimensions, they must be the same as the u and v arrays.
cor -- Coriolis sine latitude term. An array of the same
dimensionality as msfm.
dx -- A scalar representing the grid spacing in X.
dy -- A scalar representing the grid spacing in Y.
opt -- [optional] An integer option, not in use yet. Set to 0.
  """

  u2    = _promote_scalar(u)
  v2    = _promote_scalar(v)
  th2   = _promote_scalar(th)
  p2    = _promote_scalar(p)
  msfu2 = _promote_scalar(msfu)
  msfv2 = _promote_scalar(msfv)
  msfm2 = _promote_scalar(msfm)
  cor2  = _promote_scalar(cor)
  dx2   = _promote_scalar(dx)
  dy2   = _promote_scalar(dy)

  return fplib.wrf_pvo(u2,v2,th2,p2,msfu2,msfv2,msfm2,cor2,dx2,dy2,opt)

################################################################

def wrf_rh(qv, p, t):
  """
Calculates relative humidity from ARW WRF model output.
rh = Ngl.wrf_rh (qv,p,t)
qv -- Water vapor mixing ratio in [kg/kg]. The rightmost dimensions
must be bottom_top x south_north x west_east.
p -- Full pressure (perturbation + base state pressure) with the same
dimension structure as qv. Units must be [Pa].
t -- Temperature in [K] with the same dimension structure as qv. This
variable can be calculated by Ngl.wrf_tk.
  """
#
# Promote p and theta to numpy arrays that have at least a dimension of 1.
#
  qv2 = _promote_scalar(qv)
  p2  = _promote_scalar(p)
  t2  = _promote_scalar(t)

  return fplib.wrf_rh(qv2,p2,t2)

################################################################

def wrf_slp(z,t,p,q):
  """
Calculates sea level pressure from ARW WRF model output.
z -- Geopotential height in [m] with at least 3 dimensions. It must be
on the ARW WRF unstaggered grid. The rightmost three dimensions must
be level bottom_top x lat (south_north) x lon (west_east).
t -- Temperature in [K]. An array with the same dimensionality as
Z. This variable can be calculated by wrf_tk.
p -- Full pressure (perturbation + base state pressure) in [Pa]. An
array of the same dimensionality as Z.
q -- Water vapor mixing ratio in [kg/kg]. An array of the same
dimensionality as Z.
  """
#
# Promote input arrays to numpy arrays that have at least a dimension of 1.
#
  z2 = _promote_scalar(z)
  t2 = _promote_scalar(t)
  p2 = _promote_scalar(p)
  q2 = _promote_scalar(q)

  return fplib.wrf_slp(z2,t2,p2,q2)

################################################################

def wrf_td(p, qv):
  """
Calculates dewpoint temperature in [C] from ARW WRF model output.
td = Ngl.wrf_td (p,qv)
p -- Full pressure (perturbation + base state pressure). The rightmost
dimensions are bottom_top x south_north x west_east. Units must be
[Pa].
qv -- Water vapor mixing ratio in [kg/kg]. An array with the same dimensionality as P.
  """

#
# Promote p and theta to numpy arrays that have at least a dimension of 1.
#
  p2  = _promote_scalar(p)
  qv2 = _promote_scalar(qv)

  return fplib.wrf_td(p2, qv2)

################################################################

def wrf_tk(p, theta):
  """
Calculates temperature in [K] from ARW WRF model output.
tk = Ngl.wrf_tk (p,theta)
P -- Full pressure (perturbation + base state pressure). The rightmost
dimensions must be bottom_top x south_north x west_east. Units must be
[Pa].
theta -- Potential temperature (i.e, perturbation + reference
temperature) with the same dimension structure as P. Units must be
[K].
  """

#
# Promote p and theta to numpy arrays that have at least a dimension of 1.
#
  p2     = _promote_scalar(p)
  theta2 = _promote_scalar(theta)

  return fplib.wrf_tk(p2, theta2)

################################################################

def wrf_map_resources(wrf_file,map_opts,zoom_in=False,nest_time=0,Ystart=0,Yend=-1,Xstart=0,Xend=-1):
  """
Sets a bunch of graphical map resources needed to plot data
in the projection defined by the given WRF ARW file.
Ngl.wrf_map_resources (wrf_file,res)
wrf_file -- Either the name of a WRF output file, or a file pointer
to a WRF output file that's already been opened by Nio.open_file.
res -- A resource list (created by Ngl.Resources()) to attach additional 
resources to.
  """
#
# Set resources depending on what kind of map projection is on the file.
#
#   MAP_PROJ = 0 : "CylindricalEquidistant"
#   MAP_PROJ = 1 : "LambertConformal"
#   MAP_PROJ = 2 : "Stereographic"
#   MAP_PROJ = 3 : "Mercator"
#   MAP_PROJ = 6 : "Lat/Lon"
#

  if (type(wrf_file) == type('s')):
    try:
      import Nio
      wfile = Nio.open_file(wrf_file,'r')
    except:
      print("wrf_map_resources: couldn't open specified WRF output file")
      return
  else:
    wfile = wrf_file

# Check if MAP_PROJ is on the file.
  if(not hasattr(wfile,"MAP_PROJ")):
    return

  map_opts.tfDoNDCOverlay = _get_res_value_keep(map_opts, "tfDoNDCOverlay", True)

#   CylindricalEquidistant
  if(wfile.MAP_PROJ == 0):
    map_opts.mpProjection   = "CylindricalEquidistant"
    map_opts.mpGridSpacingF = 45
    map_opts.mpCenterLatF   = _get_res_value_keep(map_opts, "mpCenterLatF", 0.0)
    if(hasattr(wfile,"STAND_LON")):
      map_opts.mpCenterLonF  = _get_res_value_keep(map_opts, "mpCenterLonF",wfile.STAND_LON)
    elif(hasattr(wfile,"CEN_LON")):
      map_opts.mpCenterLonF  = _get_res_value_keep(map_opts, "mpCenterLonF",wfile.CEN_LON)
    else:
      print("Ngl.wrf_map_resources: Error: Found neither STAND_LON or CEN_LON on file")
      return

#   LambertConformal projection
  if(wfile.MAP_PROJ == 1):
    map_opts.mpProjection        = "LambertConformal"
    map_opts.mpLambertParallel1F = _get_res_value_keep(map_opts, "mpLambertParallel1F",wfile.TRUELAT1)
    map_opts.mpLambertParallel2F = _get_res_value_keep(map_opts, "mpLambertParallel2F",wfile.TRUELAT2)
    if(hasattr(wfile,"STAND_LON")):
      map_opts.mpLambertMeridianF  = _get_res_value_keep(map_opts, "mpLambertMeridianF",wfile.STAND_LON)
    elif(hasattr(wfile,"CEN_LON")):
      map_opts.mpLambertMeridianF  = _get_res_value_keep(map_opts, "mpLambertMeridianF",wfile.CEN_LON)
    else:
      print("Ngl.wrf_map_resources: Error: Found neither STAND_LON or CEN_LON in file")
      return
  
#   Stereographic projection
  if(wfile.MAP_PROJ == 2):
    map_opts.mpProjection   = "Stereographic"
    map_opts.mpCenterLatF   = _get_res_value_keep(map_opts, "mpCenterLatF", wfile.CEN_LAT)
    if(hasattr(wfile,"STAND_LON")):
      map_opts.mpCenterLonF  = _get_res_value_keep(map_opts, "mpCenterLonF",wfile.STAND_LON)
    elif(hasattr(wfile,"CEN_LON")):
      map_opts.mpCenterLonF  = _get_res_value_keep(map_opts, "mpCenterLonF",wfile.CEN_LON)
    else:
      print("Ngl.wrf_map_resources: Error: Found neither STAND_LON or CEN_LON in file")
      return
  
#   Mercator projection
  if(wfile.MAP_PROJ == 3):
    map_opts.mpProjection   = "Mercator"
    map_opts.mpCenterLatF   = _get_res_value_keep(map_opts, "mpCenterLatF", 0.0)
    if(hasattr(wfile,"STAND_LON")):
      map_opts.mpCenterLonF  = _get_res_value_keep(map_opts, "mpCenterLonF",wfile.STAND_LON)
    elif(hasattr(wfile,"CEN_LON")):
      map_opts.mpCenterLonF  = _get_res_value_keep(map_opts, "mpCenterLonF",wfile.CEN_LON)
    else:
      print("Ngl.wrf_map_resources: Error: Found neither STAND_LON or CEN_LON in file")
      return
  
#    global WRF CylindricalEquidistant
  if(wfile.MAP_PROJ == 6):
    map_opts.mpProjection   = "CylindricalEquidistant"
    map_opts.mpGridSpacingF = 45
    map_opts.mpCenterLonF   = _get_res_value_keep(map_opts, "mpCenterLonF",wfile.CEN_LON)
    if( hasattr(wfile,"POLE_LAT") ):
      map_opts.mpCenterRotF = _get_res_value_keep(map_opts, "mpCenterRotF", 90.0 - wfile.POLE_LAT) 
      del map_opts.mpCenterLonF
      calcen = -190.
      map_opts.mpCenterLonF  = _get_res_value_keep(map_opts, "mpCenterLonF", calcen )

  varnames = wfile.variables.keys()  

  if("XLAT" in varnames and "XLONG" in varnames):
    lat = wfile.variables["XLAT"][nest_time,:,:]
    lon = wfile.variables["XLONG"][nest_time,:,:]
  elif("XLAT_M" in varnames and "XLONG_M" in varnames):
    lat = wfile.variables["XLAT_M"][nest_time,:,:]
    lon = wfile.variables["XLONG_M"][nest_time,:,:]
  else:
    print("Ngl.wrf_map_resources: Error: Found neither XLAT/XLONG or XLAT_M/XLONG_M on file")
    return

  nlat = lat.shape[0]
  nlon = lat.shape[1]

# Use numpy.where here!
  for ii in range(nlat):
    for jj in range(nlon):
      if (lon[ii,jj] < 0.0):
        lon[ii,jj] = lon[ii,jj] + 360.

# Set some resources common to all map projections.
# "LowRes" is the default that NCL uses, so you don't need to
# set it here. However, if you want a higher resolution, use 
# "MediumRes". If you want higher resolution for the coastlines,
# then set it to "HighRes", but then you also need to download
# the RANGS-GSHHS database.  Higher resolutions take longer to
# draw.

  map_opts.mpOutlineOn           = _get_res_value_keep(map_opts, "mpOutlineOn", True)
  map_opts.mpFillOn              = _get_res_value_keep(map_opts, "mpFillOn", False)
  map_opts.mpDataBaseVersion     = _get_res_value_keep(map_opts, "mpDataBaseVersion","MediumRes")
  map_opts.mpOutlineBoundarySets = _get_res_value_keep(map_opts, "mpOutlineBoundarySets", "GeophysicalAndUSStates")
  map_opts.mpPerimLineThicknessF = _get_res_value_keep(map_opts, "mpPerimLineThicknessF", 1.0)
  map_opts.tmXBLabelFontHeightF  = _get_res_value_keep(map_opts, "tmXBLabelFontHeightF", 0.01)
  map_opts.tmYLLabelFontHeightF  = _get_res_value_keep(map_opts, "tmYLLabelFontHeightF", 0.01)

# Select portion of the map to view.
  map_opts.mpLimitMode           = _get_res_value_keep(map_opts, "mpLimitMode","Corners")
  map_opts.mpLeftCornerLatF      = _get_res_value_keep(map_opts, "mpLeftCornerLatF", lat[0,0])
  map_opts.mpLeftCornerLonF      = _get_res_value_keep(map_opts, "mpLeftCornerLonF", lon[0,0])
  map_opts.mpRightCornerLatF     = _get_res_value_keep(map_opts, "mpRightCornerLatF",lat[nlat-1,nlon-1])
  map_opts.mpRightCornerLonF     = _get_res_value_keep(map_opts, "mpRightCornerLonF",lon[nlat-1,nlon-1])

  if ( map_opts.mpRightCornerLonF < 0.0 ):
    map_opts.mpRightCornerLonF  = map_opts.mpRightCornerLonF + 360.0

# Set some other resources for line colors and grid spacing.

  map_opts.mpGeophysicalLineColor      = _get_res_value_keep(map_opts, "mpGeophysicalLineColor","Gray25")
  map_opts.mpGeophysicalLineThicknessF = _get_res_value_keep(map_opts, "mpGeophysicalLineThicknessF",0.75)
  map_opts.mpGridLineColor             = _get_res_value_keep(map_opts, "mpGridLineColor","Gray25")
  map_opts.mpGridLineThicknessF        = _get_res_value_keep(map_opts, "mpGridLineThicknessF",0.75)
  map_opts.mpGridSpacingF              = _get_res_value_keep(map_opts, "mpGridSpacingF",5)
  map_opts.mpLimbLineColor             = _get_res_value_keep(map_opts, "mpLimbLineColor","Gray25")
  map_opts.mpLimbLineThicknessF        = _get_res_value_keep(map_opts, "mpLimbLineThicknessF",0.75)
  map_opts.mpNationalLineColor         = _get_res_value_keep(map_opts, "mpNationalLineColor","Gray25")
  map_opts.mpNationalLineThicknessF    = _get_res_value_keep(map_opts, "mpNationalLineThicknessF",0.75)
  map_opts.mpPerimLineColor            = _get_res_value_keep(map_opts, "mpPerimLineColor","Gray25")
  map_opts.mpPerimOn                   = _get_res_value_keep(map_opts, "mpPerimOn",True)
  map_opts.mpUSStateLineColor          = _get_res_value_keep(map_opts, "mpUSStateLineColor","Gray25")
  map_opts.mpUSStateLineThicknessF     = _get_res_value_keep(map_opts, "mpUSStateLineThicknessF",0.75)
  map_opts.pmTickMarkDisplayMode       = _get_res_value_keep(map_opts, "pmTickMarkDisplayMode","Always")

# Tick mark resources
  map_opts.tmXTOn                = _get_res_value_keep(map_opts,"tmXTOn",False)
  map_opts.tmYROn                = _get_res_value_keep(map_opts,"tmYROn",False)
  map_opts.tmYRLabelsOn          = _get_res_value_keep(map_opts,"tmYRLabelsOn",True)
  map_opts.tmXBBorderOn          = _get_res_value_keep(map_opts,"tmXBBorderOn",True)
  map_opts.tmXTBorderOn          = _get_res_value_keep(map_opts,"tmXTBorderOn",True)
  map_opts.tmYLBorderOn          = _get_res_value_keep(map_opts,"tmYLBorderOn",True)
  map_opts.tmYRBorderOn          = _get_res_value_keep(map_opts,"tmYRBorderOn",True)

#
# Special section to zoom in on WRF map plot. NOTE: This hasn't been tested yet!
#
# The user must specify the index locations of the desired zoomed
# in area via the Xstart/YStart/Xend/Yend options.
#
  if zoom_in:
    y1 = Ystart
    x1 = Xstart
    if(Yend == -1):
      y2 = nlat-1
    if(Xend == -1):
      x2 = nlon-1
    if(Xstart < 0 or Xstart > (nlon-1) or Ystart < 0 or Ystart > (nlat-1)):
      print("Ngl.wrf_map_resources: Error: Invalid index values for one or more of Xstart/Xend/Ystart/Yend")
    else:
      map_opts.mpLeftCornerLatF  = lat[y1,x1]
      map_opts.mpLeftCornerLonF  = lon[y1,x1]
      map_opts.mpRightCornerLatF = lat[y2,x2]
      map_opts.mpRightCornerLonF = lon[y2,x2]

      if (map_opts.mpRightCornerLonF < 0.0):
        map_opts.mpRightCornerLonF  = map_opts.mpRightCornerLonF + 360.0

  if (type(wrf_file) == type('s')):
    wfile.close()

  return(map_opts)

################################################################

def xy(wks,xar,yar,rlistc=None):
  """
Creates and draws an XY plot, and returns a PlotId representing the XY
plot created.
xyplot = Ngl.xy(wks, x, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
x, y -- The X and Y coordinates of the curve(s). These values can be
        one-dimensional NumPy (masked) arrays, Python lists or
        two-dimensional NumPy (masked) arrays. If x and/or y are
        two-dimensional, then the leftmost dimension determines the
        number of curves.
res -- An (optional) instance of the Resources class having PyNGL
       resources as attributes.
  """
  _set_spc_defaults(1)

# Get NumPy array from masked arrays, if necessary.
  xar2,xar_fill_value = _get_arr_and_fv(xar)
  yar2,yar_fill_value = _get_arr_and_fv(yar)

#
#  Get input array dimension information.
#
  if _is_list_or_tuple(xar2):
    ndims_x = 1
    dsizes_x = (len(xar2),)
  elif _is_numpy_array(xar2):
    ndims_x = (len(xar2.shape))
    dsizes_x = xar2.shape
  else:
    print (\
      "xy: type of argument 2 must be one of: list, tuple, or NumPy array")
    return None

  if _is_list_or_tuple(yar2):
    ndims_y = 1
    dsizes_y = (len(yar2),)
  elif _is_numpy_array(yar2):
    ndims_y = (len(yar2.shape))
    dsizes_y = yar2.shape
  else:
    print (\
      "xy: type of argument 3 must be one of: list, tuple, or NumPy array")
    return None

  rlist = _crt_dict(rlistc)  
 
#
#  Separate the resource dictionary into those resources
#  that apply to various lists.
#
  ca_rlist   = {}
  xy_rlist   = {}
  xyd_rlist  = {}
  fill_rlist = {}

# Set missing value resources, if necessary
  _set_msg_val_res(rlist,xar_fill_value,"xy_x")
  _set_msg_val_res(rlist,yar_fill_value,"xy_y")

# Set list of special fill attributes
  fill_attrs = ['nglXYAboveFillColors','nglXYBelowFillColors', \
                'nglXYRightFillColors','nglXYLeftFillColors',  \
                'nglXYFillColors']
  fill_xy = False
  for key in rlist.keys():
    rlist[key] = _convert_from_ma(rlist[key])
#---Test for special fill attributes
    if key in fill_attrs:
      fill_xy         = True
      if type(rlist[key]) == type(" ") or type(rlist[key]) == type(1):
        fill_rlist[key] = [rlist[key]]    # Make sure it's a list.
      else:
        fill_rlist[key] = rlist[key]
      _set_spc_res('Frame',False)
      _set_spc_res('Draw',False)
      
    elif (key[0:2] == "ca"):
      ca_rlist[key] = rlist[key]
    elif (key[0:2] == "xy"):
      if (key[0:4] == "xyCo"):
        xy_rlist[key] = rlist[key]
      elif (key[0:4] == "xyCu"):
        xy_rlist[key] = rlist[key]
      elif (key[0:3] == "xyX"):
        xy_rlist[key] = rlist[key]
      elif (key[0:3] == "xyY"):
        xy_rlist[key] = rlist[key]
      else:
        xyd_rlist[key] = rlist[key]
    elif(key[0:3] == "ngl"):
      _set_spc_res(key[3:],rlist[key])      
    else:
      xy_rlist[key] = rlist[key]

#
# Call the wrapped function.
#
  ixy = xy_wrap(wks,xar2,yar2,"double","double",ndims_x,dsizes_x,ndims_y, \
                    dsizes_y,0,0,pvoid(),pvoid(),ca_rlist,xy_rlist,xyd_rlist,
                    pvoid())

  rval = _lst2pobj(ixy)

#---Check if we need to fill between curves.
  if fill_xy and (not rval is None):
    rval = _fill_bw_xy(wks,rval,xar,yar,fill_rlist)

    if (rlist.has_key("nglDraw") and rlist["nglDraw"]) or \
       not rlist.has_key("nglDraw"):
      draw(rval.xy)
    if (rlist.has_key("nglFrame") and rlist["nglFrame"]) or \
       not rlist.has_key("nglFrame"):
      frame(wks)

  del rlist
  del ca_rlist
  del xy_rlist
  del xyd_rlist

# rval.xy and rval.base will be None if XY plot is invalid.
  return(rval)

################################################################

def y(wks,yar,rlistc=None):
  """
Creates and draws an XY plot using index values for the X axis, and
returns a PlotId representing the XY plot created.
yplot = Ngl.y(wks, y, res=None)
wks -- The identifier returned from calling Ngl.open_wks.
y -- The Y coordinates of the curve(s). y can be a one-dimensional
     NumPy (masked) array, a Python list, or a two-dimensional NumPy
     (masked) array. If y is two-dimensional, then the leftmost dimension
     determines the number of curves and the rightmost dimension
     defines the number of points (npts).
res -- An (optional) instance of the Resources class having PyNGL
       resources as attributes.
  """
  
# Get NumPy array from masked array, if necessary.
  yar2,fill_value = _get_arr_and_fv(yar)

#
#  Get input array dimension information. We have to go through all
#  of this just to get the number of points, which we need for the
# "range" call below.
#
  if _is_list_or_tuple(yar2):
    ndims_y = 1
    dsizes_y = (len(yar2),)
  elif _is_numpy_array(yar2):
    ndims_y = (len(yar2.shape))
    dsizes_y = yar2.shape
  else:
    print (\
      "xy: type of argument 3 must be one of: list, tuple, or NumPy array")
    return None

  if (len(dsizes_y) == 1):
    npts = dsizes_y[0]
  elif (len(dsizes_y) == 2):
    npts = dsizes_y[1]
  else:
    print (\
      "y: array can have at most two dimensions")
    return None
    
# Just pass yar and let the xy function deal with setting msg val
# resources, if any.
  return xy(wks,range(0,npts),yar,rlistc)

################################################################

def yiqrgb(y,i,q):
  """
Converts from the YIQ color space to RGB.
r, g, b = Ngl.yiqrgb(y, i, q)
y -- Y component (luminance) values in the range [0.,1.].
i -- I component (chrominance orange-blue) values in the range [-0.6,
     0.6].
q -- Q component (chrominance purple-green) values in the range
     [-0.52, 0.52].
Return values
r, g, b -- The red, green, and blue intensity values in the range
           [0.,1.].
  """
  if (_is_scalar(y) and _is_scalar(i) and _is_scalar(q)):
    return(c_yiqrgb(y,i,q))
  if (_is_numpy_array(y) and _is_numpy_array(i) and _is_numpy_array(q)):
    ishape = y.shape
    dimc = len(y.ravel())
    rr = numpy.zeros(dimc,'f')
    gr = numpy.zeros(dimc,'f')
    br = numpy.zeros(dimc,'f')
    for j in xrange(dimc):
      rr[j],gr[j],br[j] = c_yiqrgb(y.ravel()[j],i.ravel()[j],q.ravel()[j])
    rr.shape = gr.shape = br.shape = ishape
    del dimc,ishape
    return rr,gr,br
  elif ( _is_list_or_tuple(y) and _is_list_or_tuple(i) and \
         _is_list_or_tuple(q) ):
    yi = numpy.array(y,'f')
    ii = numpy.array(i,'f')
    qi = numpy.array(q,'f')
    ishape = yi.shape
    dimc = len(yi.ravel())
    rr = numpy.zeros(dimc,'f')
    gr = numpy.zeros(dimc,'f')
    br = numpy.zeros(dimc,'f')
    for j in xrange(dimc):
      rr[j],gr[j],br[j] = c_yiqrgb(yi.ravel()[j],ii.ravel()[j],qi.ravel()[j])
    rr.shape = gr.shape = br.shape = ishape
    del yi,ii,qi,ishape,dimc
    return rr,gr,br
  else:
    print ("yiqrgb: arguments must be scalars, arrays, lists or tuples.")

################################################################
# This function is one of two codes contributed by Lou Wicker
# of NOAA:
#
#    _nearlyequal
#    nice_cntr_levels
#
# There was a "nice_mnmxintvl", but we decided to combine this
# into one function, "nice_cntr_levels".
#
def nearlyequal(a, b, sig_digit=None):
    """ Measures the equality (for two floats), in unit of decimal significant 
        figures.  If no sigificant digit is specified, default is 7 digits. """

    if sig_digit is None or sig_digit > 7:
        sig_digit = 7
    if a == b:
        return True
    difference = abs(a - b)
    avg = abs((a + b)/2)
    
    return numpy.log10(avg / difference) >= sig_digit
    
    
################################################################
# This function is one of two codes contributed by Lou Wicker
# of NOAA:
#
#    _nearlyequal
#    nice_cntr_levels
#
# There was a "nice_mnmxintvl", but we decided to combine this
# into one function, "nice_cntr_levels".
#
def nice_cntr_levels(lmin, lmax, outside=True, max_steps=15, cint=None, returnLevels=False, aboutZero=False):
    """ Description: Given min and max values of a data domain and the maximum
                     number of steps desired, determines "nice" values of 
                     for endpoints, the contour value, and if requested, an numpy
                     array containing the individual contour levels.
                     through the data domain. A flag controls whether the max 
                     and min are inside or outside the data range.  Another
                     flag can make sure that the 0 contour is in the array.
  
        In Args: float   lmin         the minimum value of the domain
                 float   lmax         the maximum value of the domain
                 int     max_steps    the maximum number of steps desired
                 logical outside      controls whether return min/max fall just
                                      outside or just inside the data domain.
                     if outside: 
                         min_out <= min < min_out + step_size
                                         max_out >= max > max_out - step_size
                     if inside:
                         min_out >= min > min_out - step_size
                                         max_out <= max < max_out + step_size
      
                 float    cint      if specified, the contour interval is set 
                                    to this, and the max/min bounds, based on 
                                    "outside" are returned.
                 returnLevels:  if True, an additional argument is returned that
                                is a numpy array containing the contour levels
                  aboutZero:    if True, makes sure that the contour interval will
                                be centered about zero.
      
      
        Out Args: min_out     a "nice" minimum value
                  max_out     a "nice" maximum value  
                  step_size   a step value such that 
                                     (where n is an integer < max_steps):
                                      min_out + n * step_size == max_out 
                                      with no remainder 
                  clevels     if returnLevels=True, a numpy array containing the contour levels
      
        If max==min, or a contour interval cannot be computed, returns "None"
     
        Algorithm mimics the NCAR NCL lib "nice_cntr_levels"; code adapted from 
        "nicevals.c" however, added the optional "cint" arg to facilitate user 
        specified specific interval.
     
        Lou Wicker, NSSL, August 2010 """

    table = numpy.array([1.0,2.0,2.5,4.0,5.0,10.0,20.0,25.0,40.0,50.0,100.0,200.0,
                      250.0,400.0,500.0])

    if nearlyequal(lmax,lmin):
        return None
    
    # Help people like me who can never remember - flip max/min if inputted reversed
    if lmax < lmin:
        amax = lmin
        amin = lmax
    else:
        amax = lmax
        amin = lmin

# If aboutZero == True, adjust the max/mins so that they symmetrically straddle zero

    if aboutZero:
        vmax = max(abs(lmax), abs(lmin))
        amax =  vmax
        amin = -vmax

    d = 10.0**(numpy.floor(numpy.log10(amax - amin)) - 2.0)

    if cint is None or cint == 0.0:
        t = table * d
    else:
        t = cint

    if outside:
        am1 = numpy.floor(amin/t) * t
        ax1 = numpy.ceil(amax/t)  * t
    else:
        am1 = numpy.ceil(amin/t) * t
        ax1 = numpy.floor(amax/t)  * t
    
    if cint is None or cint == 0.0:   
        cints = (ax1 - am1) / t

        # DEBUG LINE BELOW
        #print t, am1, ax1, cints

        try:
            index = numpy.where(cints < max_steps)[0][0]
        except IndexError:
            return None

        if returnLevels:
            return am1[index], ax1[index], cints[index], numpy.arange(am1[index], ax1[index]+cints[index], cints[index]) 
        else:
            return am1[index], ax1[index], cints[index]

    else:

        if returnLevels:
            return am1, ax1, cint, numpy.arange(am1, ax1+cint, cint) 
        else:
            return am1, ax1, cint


