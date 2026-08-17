#exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())
from threading import Lock
from cnoid.IRSLPlugin import IRSLPlugin

def _highlight(obj, on=True, notify=True):
    mat = obj.material
    if mat:
        if on:
            mat.ambientIntensity = 1.1
            mat.emissiveColor = mat.diffuseColor * 0.4
        else:
            mat.ambientIntensity = 0.02
            mat.emissiveColor = mat.diffuseColor * 0.02
        mat.notifyUpdate()

def get_picked():
    global picked_name
    return [ shapemap[p] for p in picked_name if p in shapemap ]

class PickedObject(object):
    """
    Examples:
        >>> po = PickedObject()
        >>> po.addObject(make_box(0))
        >>> po.addObject(make_box(1))
        >>> po.addObject(make_box(2))
        >>> po.addObject(make_box(3))
        >>> po.addObject(make_box(4))
        >>> po.addObject(make_box(5))
        # initialize objects
        >>> po.genShapeMap()
        # start picking
        >>> po.getPickedShape() ## get picked
    """
    def __init__(self, di=None, highLight=True):
        self.picked_name_list = []
        self.shape_map = {}
        self.obj_list = []
        self.obj_map = {}
        self.di = DrawInterface() if di is None else di
        self.highLight = highLight
        self.lock = Lock()
        self.connection = IRSLPlugin.instance().sigPickedName().connect( self._callback_pick )

    def __del__(self):
        self.connection.disconnect()

    def addObject(self, obj, update=True, hook=True):
        """This method is overrided, just passing arguments to addPyObject
        """
        self._addPyObject(obj, update=update, hook=hook)

    def addObjects(self, objlst, update=True, hook=True):
        """Adding objects to be drawn

        Args:
            objlst ( list[cnoid.Util.SgNode] ): list of objects to be drawn
            update (boolean, default = False) : if True, rendering scene immediately

        """
        tp=type(objlst)
        if tp is list or tp is tuple:
            for obj in objlst[:-1]:
                self._addPyObject(obj, False, hook=hook)
            self._addPyObject(objlst[-1], update=update, hook=hook)
        else:
            self._addPyObject(objlst, update=update, hook=hook)

    def _addPyObject(self, obj, update=True, hook=True):
        self.obj_list.append(obj)
        self.di.addPyObject(obj, update=update, hook=hook)

    def genShapeMap(self, generateObjectMap=True, addName=True):
        with self.lock:
            self.shape_map = {}
            for shape, coords in mkshapes.extractShapes( self.di.SgPosTransform ):
                if len(shape.name) < 1:
                    shape.name = hex(id(shape))
                self.shape_map[shape.name] = shape
                if self.highLight:
                    _highlight(shape, on=False, notify=False)
            if generateObjectMap:
                for obj in self.obj_list:
                    self.obj_map[ obj.object.name ] = obj
            self.di.flush()

    def clearPicked(self):
        with self.lock:
            self.picked_name_list = []
        self.genShapeMap() ## off high-light

    def clearAll(self):
        self.di.clear()
        self.obj_list = []
        self.obj_map = {}
        self.clearPicked()

    def _callback_pick(self, name):
        with self.lock:
            if len(name) > 0:
                self.picked_name_list.append(name)
                if self.highLight and name in self.shape_map:
                    _highlight(self.shape_map[name])

    def getPickedName(self):
        return self.picked_name_list

    def getPickedObject(self):
        return [ self.obj_map[p] for p in self.picked_name_list if p in self.obj_map ]

    def getPickedShape(self):
        return [ self.shape_map[p] for p in self.picked_name_list if p in self.shape_map ]

#
# gen picked_target
#

###
_mat_list = [( coordinates.Z, coordinates.Y),
             (-coordinates.Z, coordinates.Y),
             ( coordinates.X, coordinates.Y),
             (-coordinates.X, coordinates.Y),
             ( coordinates.Y, -coordinates.Z),
             (-coordinates.Y,  coordinates.Z),
             (fv(math.sqrt(1/3), math.sqrt(1/3),  math.sqrt(1/3)), fv(math.sqrt(1/2), 0, -math.sqrt(1/2))),
             (fv(math.sqrt(1/3), -math.sqrt(1/3), math.sqrt(1/3)), fv(math.sqrt(1/2), 0, -math.sqrt(1/2))),
             (fv(-math.sqrt(1/3), math.sqrt(1/3), math.sqrt(1/3)), fv(0, math.sqrt(1/2), -math.sqrt(1/2))),
             (fv(math.sqrt(1/3), math.sqrt(1/3),  -math.sqrt(1/3)), fv(math.sqrt(1/2), 0, math.sqrt(1/2))),
             (fv(math.sqrt(1/3), -math.sqrt(1/3), -math.sqrt(1/3)), fv(math.sqrt(1/2), 0, math.sqrt(1/2))),
             (fv(-math.sqrt(1/3), math.sqrt(1/3), -math.sqrt(1/3)), fv(0, math.sqrt(1/2), math.sqrt(1/2))),
             ]

_col_list = [(0, 0, 1),
             (0, 1, 1),
             (1, 0, 0),
             (1, 0, 1),
             (0, 1, 0),
             (1, 1, 0),
             (1, 0.5, 0), ## 1
             (0, 0.5, 1), ## 4
             (0.5, 1, 0), ## 2
             (0.5, 0, 1), ## 5
             (0, 1, 0.5), ## 3
             (1, 0, 0.5), ## 6
             ]

def _make_mat(index=0):
    index = index % len(_mat_list)
    vz, vy = _mat_list[index]
    vx = np.cross(vy, vz)
    return np.column_stack((vx, vy, vz))

def make_box(index=0, length=0.25, name=''):
    bx = mkshapes.makeBox(x=length, y=length, z=length*2, color=_col_list[index%len(_col_list)] )
    bx.object.name = name
    #
    mat = _make_mat(index)
    #
    cc = coordinates(mat)
    cc.translate(fv(0, 0, length*0.5))
    bx.newcoords(cc)
    return bx

def makeSimpleAxes(size=0.1, length=0.4, length_xy=0.25, name='', color=0, coords=None):
    if type(color) is int:
        _col = _col_list[color%len(_col_list)]
    else:
        _col = color
    xcds = coordinates(fv(length_xy*0.5, 0, 0))
    ycds = coordinates(fv(0, length_xy*0.5, 0))
    zcds = coordinates(fv(0, 0, length*0.5))
    xobj = mkshapes.makeBox(x=length_xy, y=size,      z=size,   coords=xcds, wrapped=False, color=_col)
    yobj = mkshapes.makeBox(x=size,      y=length_xy, z=size,   coords=ycds, wrapped=False)
    zobj = mkshapes.makeBox(x=size,      y=size,      z=length, coords=zcds, wrapped=False)
    mat_ = xobj.getChild(0).material
    yobj.getChild(0).setMaterial(mat_)
    zobj.getChild(0).setMaterial(mat_)
    oobj = cutil.SgPosTransform()
    oobj.addChild(xobj)
    oobj.addChild(yobj)
    oobj.addChild(zobj)
    trs = cutil.SgPosTransform()
    trs.addChild(oobj)
    ret = mkshapes.coordsWrapper(trs, original_object=oobj)
    if coords is not None:
        ret.newcoords(coords)
    ret.object.name = name
    return ret
