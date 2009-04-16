# Part of the gazehound package for analzying eyetracking data
#
# Copyright (c) 2008 Board of Regents of the University of Wisconsin System
#
# Written by Nathan Vack <njvack@wisc.edu> at the Waisman Laborotory
# for Brain Imaging and Behavior, University of Wisconsin - Madison.

from __future__ import with_statement
import sys
import os.path
from optparse import OptionParser
from .. import readers, timeline, viewing, shapes
from ..writers import delimited

#def main(argv = None):
#    if argv is None:
#        argv = sys.argv
#        
#    gsr = FixationStatsRunner(argv)
#    gsr.print_analysis()




class FixationStatisticsOptionParser(object):
    """
    Parses the command line options for the analyzer
    """

    def __init__(self, argv, err = sys.stderr):
        old_err = err
        sys.stderr = err
        super(FixationStatisticsOptionParser, self).__init__()
        self.argv = argv
        parser = OptionParser()

        parser.add_option(
            "--stimuli", dest = "stim_file", 
            help = "Read stimulus timings from FILE",
            metavar = "FILE"
        )

        parser.add_option(
            "--obt-dir", dest = "object_dir",
            help = "Find .OBT files in PATH. Requires --stimuli",
            metavar = "PATH"
        )

        parser.add_option(
            "--recenter-on", dest = "recenter_on",
            help = "Recenter when stimuli named NAME are shown",
            metavar = "NAME"
        )

        self.options, self.args = parser.parse_args(argv[1:])

        if len(self.args) == 0:
            parser.error("No pointpath file specified")

        if (self.options.recenter_on is not None and 
                self.options.stim_file is None):
            parser.error("You must use --stimuli with --recenter-on")

        if self.options.object_dir is not None:
            if not os.path.isdir(self.options.object_dir):
                parser.error(self.options.object_dir+" is not a directory")
            if self.options.stim_file is None:
                parser.error("You must use --stimuli with --obt-dir")  

        self.fix_file = self.args[0]
        sys.stderr = err


class FixationStatsRunner(object):
    """docstring for FixationStatsRunner"""
    def __init__(self, argv):
        """ Construct the object graph for FixationStatsAnalyzer """
        super(FixationStatsRunner, self).__init__()
        op = FixationStatisticsOptionParser(argv)
        # Read and parse the gazestream

        with open(op.fix_file) as ff:
            ir = readers.IViewFixationReader(ff.readlines())
            self.file_data = ir
            self.pointpath = ir.pointpath()

        self.timeline = None

#        if op.options.stim_file is not None:
#            self.timeline = self.__build_timeline(op.options.stim_file)
#            if op.options.object_dir is not None:
#                r = shapes.ShapeReader(path = op.options.object_dir)
#                dec = shapes.TimelineDecorator(r)
#                self.timeline = dec.find_shape_files_and_add_to_timeline(
#                    self.timeline
#                )
#            if op.options.recenter_on is not None:
#                #TODO: Make these sepeficiable on the command line
#                rx = 400
#                ry = 300
#                limiter = shapes.Rectangle(300, 200, 500, 400)
#                self.timeline = self.timeline.recenter_on(
#                    op.options.recenter_on, rx, ry, limiter
#                )
#
#        # And build the analyzer
#        self.analyzer = FixationStatisticsAnalyzer(
#            pointpath = self.pointpath,
#            timeline = self.timeline
#        )
#
#    def print_analysis(self):
#        gsw = delimited.FixationStatsWriter()
#        gsw.write_header()
#        gsw.write([self.analyzer.general_stats()])
#        if self.timeline is not None:
#            gsw.write(self.analyzer.timeline_stats())
#
#
#    def __build_timeline(self, filename):
#        """Build the timeline from a file."""
#        timeline = None
#        with open(filename) as f:
#            lines = [l.strip() for l in f.readlines()]
#            tr = readers.TimelineReader(lines)
#            ttl = tr.timeline()
#            timeline = viewing.Combiner(
#                timeline = ttl, pointpath = self.pointpath
#            ).viewings()
#        return timeline
#
#
#class FixationStatisticsAnalyzer(object):
#
#    def __init__(self, 
#        pointpath = None,
#        strict_valid_fun = None,
#        pointpath_meta = None,
#        timeline = []):
#        super(FixationStatisticsAnalyzer, self).__init__()
#        self.pointpath = pointpath
#        self.timeline = timeline
#
#        # TODO: Don't hardcode these.
#        MAX_X = 800
#        MAX_Y = 600
#
#        def default_valid(x_width, y_width, slop_frac, point):
#            xslop = x_width*slop_frac
#            yslop = y_width*slop_frac
#            max_x = x_width+xslop
#            min_x = 0-xslop
#            max_y = y_width+yslop
#            min_y = 0-yslop
#
#            return ((point.x >= min_x and point.x < max_x) and
#            (point.y >= min_y and point.y < max_y) and not
#            (point.x == 0 and point.y == 0
#            ))
#
#        def svf(point):
#            return default_valid(MAX_X, MAX_Y, 0, point)
#
#        def lvf(point):
#            return default_valid(MAX_X, MAX_Y, .1, point)
#
#        self.strict_valid_fun = svf
#        self.lax_valid_fun = lvf
#
#        def in_fun(shape, point):
#            return (point.x, point.y) in shape
#
#        self.in_fun = in_fun
#
#    def general_stats(self):
#        """Return a FixationStats containing basic data about the pointpath"""
#
#        data = FixationStats(
#            presented = 'screen',
#            area = 'all',
#            total_points = len(self.pointpath),
#            start_ms = self.pointpath[0].time,
#            end_ms = self.pointpath[-1].time,
#            valid_strict = len(self.pointpath.valid_points(
#                self.strict_valid_fun
#            )),
#            valid_lax = len(self.pointpath.valid_points(
#                self.lax_valid_fun
#            ))
#        )
#
#        data.points_in = data.valid_strict
#        data.points_out = data.total_points - data.valid_strict
#
#        return data
#
#    def timeline_stats(self):
#        """ 
#        Return a list of FixationStats containing data about all the events
#        in the timeline.
#        """
#
#        data = []
#        doshapes = hasattr(self.timeline, 'has_shapes')
#        for pres in self.timeline:
#            stats = FixationStats(
#                presented = pres.name,
#                area = 'all',
#                total_points = len(pres.pointpath),
#                start_ms = pres.start,
#                end_ms = pres.end,
#                valid_strict = len(pres.pointpath.valid_points(
#                    self.strict_valid_fun
#                )),
#                valid_lax = len(pres.pointpath.valid_points(
#                    self.lax_valid_fun
#                ))
#            )
#            stats.points_in = stats.valid_strict
#            stats.points_out = stats.total_points - stats.valid_strict
#            data.append(stats)
#            if doshapes:
#                for ss in self.shape_stats(pres):
#                    data.append(ss)
#                    pass
#        return data
#
#    def shape_stats(self, pres):
#        stats_list = []
#        if pres.shapes is None:
#            return[FixationStats(
#                presented = pres.name, 
#                area = "Can't read shape file")
#            ]
#        for s in pres.shapes:
#            stats = FixationStats(
#                presented = pres.name,
#                area = s.name,
#                total_points = len(pres.pointpath),
#                start_ms = pres.start,
#                end_ms = pres.end,
#                valid_strict = len(pres.pointpath.valid_points(
#                    self.strict_valid_fun
#                )),
#                valid_lax = len(pres.pointpath.valid_points(
#                    self.lax_valid_fun
#                ))
#            )
#
#            def f(point):
#                return self.in_fun(s, point)
#
#            stats.points_in = len(pres.pointpath.valid_points(f))
#            stats.points_out = stats.total_points - stats.points_in
#            stats_list.append(stats)
#
#        return stats_list
#
#class FixationStats(object):
#    """A data structure containing stats about a pointpath"""
#    def __init__(self, 
#    presented = None, area = None, start_ms = 0, end_ms = 0, total_points = 0, 
#    points_in = 0, points_out = 0, valid_strict = 0, valid_lax = 0
#    ):
#        super(FixationStats, self).__init__()
#        self.presented = presented
#        self.area = area
#        self.start_ms = start_ms
#        self.end_ms = end_ms
#        self.total_points = total_points
#        self.points_in = points_in
#        self.points_out = points_out
#        self.valid_strict = valid_strict
#        self.valid_lax = valid_lax