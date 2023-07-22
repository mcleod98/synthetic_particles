import numpy as np
from PIL import Image
from functools import reduce
import typing, math

from models import EllipticalParticle, Img

def generate_images(settings: dict, session, n: int) -> None:
    planner_sets = {'xdim': settings['xdim'],
            'ydim': settings['ydim'],
            'mean_r': settings['mean_r'], 
            'mean_aspect': settings['mean_aspect'],
            'mean_n': settings['mean_n'], 
            'sd_r': settings['sd_r'], 
            'sd_aspect': settings['sd_aspect'], 
            'sd_n': settings['sd_n'], 
            'min_offset': settings['min_offset'], 
            'gutters': settings['gutters'],
            'mean_theta': settings['mean_theta'],
            'sd_theta': settings['sd_theta'],
            'n_dist': settings['n_dist']
    }
    planner = Grid_planner(**planner_sets)
    imgs = []
    counter = 0
    intervals = np.arange(0, n, 10)
    for i in range(n):
        counter += 1
        grid = np.zeros([planner_sets['xdim'], planner_sets['ydim']])
        els = planner.generate_ellipse_set()
        for e in els:
            e.draw(grid)
        Im = Img(bmp=grid)
        session.add(Im)
        for e in els:
            e.image = Im
            session.add(e)
        if i in intervals:
            print(f'Finished with sample {i+1} out of {n}')
        if counter >= 10:
            session.commit()
            counter = 0
    session.commit()
    print(f'Finished generating {n} images, uploaded to {session.bind}')

class Ellipse(EllipticalParticle):
    def __init__(self, xcenter: int, ycenter: int, a: float, b: float, rotation: float, angle_range: typing.List[typing.Tuple[float, float]] = [(0,2*np.pi)]):
        self.x = xcenter
        self.y = ycenter
        self.a = a
        self.b = b
        self.theta = rotation
        self.angle_range = angle_range
        self.occlusions = len(angle_range)
        self.occluded = 1 - (np.sum([i[1] - i[0] for i in angle_range]) / np.pi / 2)
        
    def draw(self, grid: np.ndarray) -> np.ndarray:
        thickness = (.97 - np.random.random() / 20)

        xprime = self.x * np.cos(self.theta) - self.y * np.sin(self.theta)
        yprime = self.x * np.sin(self.theta) + self.y * np.cos(self.theta)
        a = self.a ** 2
        b = self.b ** 2
        xx, yy = np.mgrid[:grid.shape[0],: grid.shape[1]]
        
        ellipse = ((xx * np.cos(self.theta) - yy * np.sin(self.theta) - xprime) ** 2 / a) + ((yy * np.cos(self.theta) + xx * np.sin(self.theta) - yprime) ** 2 / b)
        
        delx = (xx * np.cos(self.theta) - yy * np.sin(self.theta) - xprime)
        dely = (yy * np.cos(self.theta) + xx * np.sin(self.theta) - yprime)
        direct = np.arctan2(dely,delx) + np.pi
        
        masks = [((direct >= low) & (direct <= high)) for low, high in self.angle_range]
        big_mask = reduce(np.logical_or, masks)
        
        inside = ellipse < 1
        grid[inside] = False
        
        rimpts = (ellipse > thickness) & (ellipse < 1)
        final_pts = np.logical_and(big_mask, rimpts)
        grid[final_pts] = True
    
        return grid


class Grid_planner():
    def __init__(self, xdim: int, ydim: int, mean_r: float, mean_aspect: float, mean_n: float, 
                sd_r: float, sd_aspect: float, sd_n: float, 
                mean_theta: float, sd_theta: float, n_dist: typing.List[typing.Tuple[int, float]], 
                min_offset: int = 0, gutters: typing.Tuple[int, int] = (0,0)):
        self.xdim = xdim
        self.ydim = ydim
        self.mean_r = mean_r
        self.mean_aspect = mean_aspect
        self.sd_r = sd_r
        self.sd_aspect = sd_aspect
        self.mean_n = mean_n
        self.sd_n = sd_n
        self.min_offset = min_offset
        self.gutters = gutters
        self.mean_theta = mean_theta
        self.sd_theta = sd_theta
        norm = np.sum([p for n,p in n_dist])
        self.n_dist = [[n, p/norm] for n,p in n_dist]
        
    def generate_ellipse_set(self) -> typing.List[typing.Type[Ellipse]]:
        e = []
        n = int(np.random.normal(self.mean_n, self.sd_n))
        for i in range(n):
            try_to_place = 0
            while try_to_place < 20:
                try_to_place += 1
                x = self.gutters[0] + np.random.random() * (self.xdim - self.gutters[0])
                y = self.gutters[1] + np.random.random() * (self.ydim - self.gutters[1])
                
                if self.min_offset > 0:
                    place = True
                    for j in e:
                        if abs(x - j.x) <= self.min_offset and abs(y - j.y) <= self.min_offset:
                            place = False
                            break
                else:
                    place = True
                    
                if place:
                    asp = np.random.normal(self.mean_aspect, self.sd_aspect)
                    a = np.random.normal(self.mean_r, self.sd_r)
                    b = a * asp
                    args = {'xcenter': x,
                            'ycenter': y,
                            'a': a,
                            'b': b,
                            'rotation': np.random.random() * np.pi * 2,
                            'angle_range': self.generate_filter()
                    }
                    El = Ellipse(**args)
                    e.append(El)
                    break
                elif try_to_place == 20:
                    print('Error: Failed to place particle {i}')
        return e
    
    def generate_filter(self) -> typing.List[typing.Tuple[float, float]]:
        if self.mean_theta == 0 or self.n_dist == []:
            return [(0, np.pi*2)]
        n_seed = np.random.random()
        c = 0
        n = 0
        for bucket in self.n_dist:
            c += bucket[1]
            if n_seed <= c:
                n = bucket[0]
                break
        if n == 0:
            raise ValueError('Failed to generate number of occlusions, check n_dist format')
        
        occ_thetas = [np.random.normal(self.mean_theta, self.sd_theta) for i in range(n)]
        remaining_theta = np.pi * 2 - np.sum(occ_thetas)

        if remaining_theta < 0:
            raise ValueError('Total occluded angle exceeds 2pi, lower mean_theta')
        
        gaps = []
        for i in range(n):
            g = np.random.normal(.5, .2) * np.random.random() * remaining_theta
            gaps.append(g)
            remaining_theta -= g

        start = 0
        filter = []
        for occ, gap in zip(occ_thetas, gaps):
            start += gap
            filter.append((start, start + occ))
            start += occ
        return filter