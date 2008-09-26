# Part of the gazehound package for analzying eyetracking data
#
# Copyright (c) 2008 Board of Regents of the University of Wisconsin System
#
# Written by Nathan Vack <njvack@wisc.edu> at the Waisman Laborotory
# for Brain Imaging and Behavior, University of Wisconsin - Madison.

class Point(object):
    """ 
    A point with x, y, and time coordinates -- one point in a scan path 
    """
    
    def __init__(self, x = None, y = None, time = None):
        self.x = x
        self.y = y
        self.time = time
        
    
    def valid(criteria):
        """ Evaluate criteria() for this point. critiera() should return
            True or False.
        """
        return critera(self)

class ScanPath(object):
    """ A set of Points arranged sequentially in time """
    def __init__(self, points = [], 
                 min_x = None, min_y = None, max_x = None, max_y = None):
        self.points = points
        
    def __len__(self):
        return self.points.__len__()
        
    def __iter__(self):
        return self.points.__iter__()
        

class PointFactory(object):
    """ Maps a list of gaze point data to a list of Points """

    def __init__(self, type_to_produce = Point):
        self.type_to_produce = type_to_produce
    

    def from_component_list(self, components, attribute_list):
        """
        Produces and returns a list of points from a list of component parts
        and an attribute mapping.
        
        Arguments:
        components: A list of lists -- each item of the outer list
            containing one gaze point's data
        
        attribute_list: A list of tuples containing (attribute_name, type)
        
        This method will happily raise an IndexException if you have
        more elements in attribute_list than in any of the elements in
        component_list.
        """
            
        points = []
        for point_data in components:
            point = self.type_to_produce()
            
            for i in range(len(attribute_list)):
                attr_name = attribute_list[i][0]
                attr_type = attribute_list[i][1]
                if attr_type is not None:
                    setattr(point, attr_name, attr_type(point_data[i]))

            points.append(point)
        return points


class IViewPointFactory(PointFactory):
    """
    Maps a list of gaze point data to a list of Points, using SMI's iView
    data scheme.
    """

        
    def __init__(self, type_to_produce = Point):
        super(IViewPointFactory, self).__init__(type_to_produce)
        self.data_map = [
            ('time', int),
            ('set', str),
            ('pupil_h', int),
            ('pupil_v', int),
            ('corneal_reflex_h', int),
            ('corneal_reflex_v', int),
            ('x', int),
            ('y', int),
            ('diam_h', int),
            ('diam_v', int)
        ]
        
    def from_component_list(self, components):
        return super(IViewPointFactory, self).from_component_list(
            components, self.data_map
        )