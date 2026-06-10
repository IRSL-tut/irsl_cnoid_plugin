from threading import Lock
import cnoid.IRSLPlugin

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
        >>> di = DrawInterface()
        >>> po = PickedObject(di=di)
        >>> di.addObject(make_box(0))
        >>> di.addObject(make_box(1))
        >>> di.addObject(make_box(2))
        >>> di.addObject(make_box(3))
        >>> di.addObject(make_box(4))
        >>> di.addObject(make_box(5))
        # initialize objects
        >>> po.genShapeMap()
        # start picking
    """
    def __init__(self, di=None, highLight=True):
        self.picked_name_list = []
        self.shape_map = {}
        self.di = DrawInterface() if di is None else di
        self.highLight = highLight
        self.lock = Lock()
        self.connection = cnoid.IRSLPlugin.sigPickedName().connect( self._callback_pick )

    def __del__(self):
        self.connection.disconnect()

    def genShapeMap(self):
        with self.lock:
            self.shape_map = {}
            for shape, coords in mkshapes.extractShapes( self.di.SgPosTransform ):
                if len(shape.name) < 1:
                    shape.name = hex(id(shape))
                self.shape_map[shape.name] = shape
                if self.highLight:
                    _highlight(shape, on=False, notify=False)
            self.di.flush()

    def clearPicked(self):
        with self.lock:
            self.picked_name_list = []
        self.genShapeMap()

    def _callback_pick(self, name):
        with self.lock:
            if len(name) > 0:
                self.picked_name_list.append(name)
                if self.highLight and name in self.shape_map:
                    _highlight(self.shape_map[name])

    def getPicked(self):
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
