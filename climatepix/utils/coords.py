import fiona.transform

from pyproj import Transformer


def reproject_coords(src_crs, dst_crs, coords):
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    xs, ys = fiona.transform.transform(src_crs, dst_crs, xs, ys)
    return [[x, y] for x, y in zip(xs, ys)]


def transform_coords(coords, src_crs, dst_crs):
    transformer = Transformer.from_crs(src_crs, dst_crs, always_xy=True)
    return [transformer.transform(x, y) for x, y in coords]