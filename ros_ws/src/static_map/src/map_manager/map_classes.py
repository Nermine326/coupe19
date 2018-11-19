#!/usr/bin/python
import copy, json
import rospy
from map_loader import LoadingHelpers
from map_bases import DictManager
from map_attributes import Position2D, Shape2D, Color, MarkerRViz
import map


class Terrain():
    def __init__(self, xml):
        LoadingHelpers.checkAttribExist(xml, "type")
        self.Shape = Shape2D(xml)
        self.Layers = [Layer(l) for l in xml.findall("layer")]
        # TODO marker


class Layer():
    def __init__(self, xml):
        LoadingHelpers.checkAttribExist(xml, "name")
        self.Name = xml.get("name")
        self.Includes = [i.get("name") for i in xml.findall("include")]
        self.Walls = [Wall(w) for w in xml.findall("wall")]


class Wall():
    def __init__(self, xml):
        LoadingHelpers.checkChildExist(xml, "position", "shape")
        self.Position = Position2D(xml.find("position"))
        self.Shape    = Shape2D(xml.find("shape"))


class Waypoint():
    def __init__(self, xml):
        LoadingHelpers.checkAttribExist(xml, "name")
        self.Name = xml.get("name")
        self.Position = Position2D(xml)


class Container():
    def __init__(self, xml, xml_classes):
        self.Elements =  [Container(c, xml_classes) for c in xml.findall("container")]
        self.Elements += [Object(o, xml_classes)    for o in xml.findall("object")]

    def get_objects(self, collisions_only = False): #TODO
        objects = []
        for o in self.Dict:
            if isinstance(self.Dict[o], Container):
                objects += self.Dict[o].get_objects(collisions_only)
            elif isinstance(self.Dict[o], Object):
                if self.Dict[o].Dict["collision"] == collisions_only or collisions_only is False:
                    objects.append(json.dumps(self.Dict[o].get("*")))
            else:
                rospy.logwarn("Not recognized DictManager type found while retrieving map objects, passing.")
        return objects


class Object(object):
    def __init__(self, xml, obj_classes, check_valid = True):
        self.Position = Position2D(xml.find("position")) if xml.find("position") is not None else None
        self.Shape    = Shape2D(xml.find("shape"))       if xml.find("shape")    is not None else None
        self.Labels   = [l.get("name") for l in xml.find("labels").findall("label")] if xml.find("labels") else []
        self.Marker   = None #TODO Markers Position2D(xml.find("position")) if xml.find("position") else None

        self.Color = None
        if xml.find("color") is not None:
            LoadingHelpers.checkAttribExist(xml.find("color"), "name")
            base = [c for c in map.MapManager.Colors if c.Name == xml.find("color").get("name")]
            if base:
                self.Color = copy.deepcopy(base[0])
            else:
                self.Color = Color(xml.find("color"))

        if xml.get("class"):
            self.merge(copy.deepcopy([c for c in obj_classes if c.Name == xml.get("class")][0]))
        
        if check_valid is True: # disabled when creating a class
            self.check_valid()

    def merge(self, other): #self is prioritary
        self.Position = self.Position if self.Position is not None else other.Position
        self.Shape    = self.Shape    if self.Shape    is not None else other.Shape
        self.Color    = self.Color    if self.Color    is not None else other.Color
        self.Labels += other.Labels
        
        #self.Marker.merge(other.Marker) #TODO Markers
    
    def check_valid(self): # Checks if all values are not None (in case of class merges)
        if None in [self.Position, self.Shape]:
            print "nogood"

class Class(Object):
    def __init__(self, xml, obj_classes):
        LoadingHelpers.checkAttribExist(xml, "name")
        self.Name = xml.get("name")
        super(Class, self).__init__(xml, obj_classes, check_valid = False)