from __future__ import division
import datetime
import itertools

import garmin

import numpy as np
import scipy.interpolate as intp

def read_tcx(infile):
    return garmin.parse(infile)

timeformat = '%Y-%m-%dT%H:%M:%SZ'
def make_time(dtstring):
    dt = datetime.datetime.strptime(dtstring, timeformat)
    return dt

def delta_seconds(td):
     return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6 


def trackpoints(tcxdata):
    """generate just the trackpoints from the activity file"""
    for act in tcxdata.Activities.Activity:
        for lap in act.Lap:
            for track in lap.Track:
                for point in track.Trackpoint:
                    yield point

def distances_and_times(trackpoints):
    """ generate distance, time pairs from a trackpoints,
    skipping those with no useful distance data"""
    return ( (float(p.DistanceMeters), make_time(p.Time)) for
             p in trackpoints if p.DistanceMeters)

# there's a problem if the first point isn't at 0 metres
def distances_and_seconds(d_and_ts):
    """ generate distance, seconds_from_start pairs from a series of
    distance, time pairs."""
    i =  iter(d_and_ts)
    d0, t0 = i.next()
    yield d0, 0.0
    for d, t in i:
        yield d, delta_seconds(t - t0)

def splits(d_and_ts, dist):
    data = np.array(list(d_and_ts))
    x = data[:,0]
    y = data[:,1]
    f = intp.interp1d(x, y)
    maxd = x[-1]
    required = np.hstack((np.arange(0, maxd, dist), [maxd]))
    result = f(required)
    result = np.diff(result)
    # we've taken the diffs for the times, so we're not interested in
    # the first distance any more.
    return required[1:], result
    
#def main():
#    import sys
#    infile = sys.argv[1]
#    splits = float(sys.argv[2])
#    tcxData = read_tcx(infile)
#    splits = make_splits(tcxData.Activities.Activity, splits)
#    for d, m, s in render_splits(splits):
#        print d, " ", m, " ", s

def calc(infile, split_dist):
    tcxData = read_tcx(infile)
    points = trackpoints(tcxData)
    ds_and_ts = distances_and_times(points)
    ds_and_ss = distances_and_seconds(ds_and_ts)
    ds, ts = splits(ds_and_ss, split_dist)
    ms, ss = divmod(ts, 60)
    return zip(ds, ms, ss)

def main():
    import sys
    infile = sys.argv[1]
    split_dist = float(sys.argv[2])
    for d, m, s in calc(infile, split_dist):
        print d, m, s

if __name__ == "__main__":
    main()
