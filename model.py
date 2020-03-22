"""Cornova Virus COVID19 Mode.

Ref.:
https://en.wikipedia.org/wiki/Mathematical_modelling_of_infectious_disease

Copyright © 2010 Ximenes R. Resende (xresende@gmail.com) - All Rights Reserved

"""

import random
import numpy as np


class COVID19:
    """."""

    def __init__(self,
                 country, population,
                 infected,
                 doublingdays, halvingdays,
                 death_percentage,
                 beds, history, tol):
        """."""
        self.country = country
        self.population = population
        self.doublingdays = doublingdays
        self.halvingdays = halvingdays
        self.susceptible = None
        self._infected = infected
        self.infected = None
        self.imune = None
        self.death_percentage = death_percentage
        self.beds = beds  # number of hospital beds per thousand people
        self.history = history
        self.tol = tol  # tolerance on affected people

        # init vectors
        self.init()

    def init(self):
        """."""
        self.infected = np.array([self._infected/self.population])
        self.susceptible = 1 - self.infected
        self.imune = 0 * self.susceptible

    def evolve(self, init=False, nr_days=None):
        """Evolve epidemy."""
        if init:
            self.init()
        beta = 1.0 / self.doublingdays
        gamma = 1.0 / self.halvingdays
        day = 0
        vecs, veci, vecr = \
            list(self.susceptible), list(self.infected), list(self.imune)
        while True:
            ps1, pi1, pr1 = vecs[-1], veci[-1], vecr[-1]
            rate = beta * ps1 * pi1
            ps2 = ps1 - rate
            pi2 = pi1 + rate - gamma * pi1
            pr2 = pr1 + gamma * pi1
            total = ps2 + pi2 + pr2
            correction = 1.0 / total
            vecs.append(correction * ps2)
            veci.append(correction * pi2)
            vecr.append(correction * pr2)
            day += 1
            if nr_days is not None:
                if day > nr_days:
                    break
            else:
                affected1 = veci[-1] + vecr[-1]
                affected2 = veci[-2] + vecr[-2]
                if (affected1 - affected2)*self.population < self.tol:
                    break
        self.susceptible = np.array(vecs)
        self.infected = np.array(veci)
        self.imune = np.array(vecr)

    def calibrate(self, niter=100000):
        """."""
        def select_cloud(trials):
            """."""
            trials = np.array(trials)
            r, p1, p2 = trials.T
            minr = min(r)
            diff = (r - minr)/minr
            sel = (diff >= -0.05) & (diff <= 0.05)
            self.cloud_doublingdays = p1[sel]
            self.cloud_halvingdays = p2[sel]
            # print(len(p1[sel]))

        residue, *_ = self.calc_residue()
        trials = []
        for _ in range(niter):
            parms = self.doublingdays, self.halvingdays
            self.doublingdays *= random.uniform(0.95, 1.05)
            self.halvingdays *= random.uniform(0.95, 1.05)
            new_residue, *_ = self.calc_residue()
            rdiff = (new_residue - residue)/residue
            if -0.05 <= rdiff <= +0.05:
                trial = new_residue, self.doublingdays, self.halvingdays
                trials.append([trial])
            if new_residue > residue:
                self.doublingdays, self.halvingdays = parms
            else:
                residue = new_residue
                print('{:11.6f} : {:.4f} {:.4f}'.format(
                    residue, self.doublingdays, self.halvingdays))

        # select_cloud(trials)
        self.init()

    def calc_residue(self):
        """."""
        self.init()
        self.evolve(nr_days=len(self.history)-2)
        infected = self.population * self.infected
        residue = np.sqrt(sum((infected - self.history)**2))
        return residue, infected, self.history

    @property
    def death_toll(self):
        """."""
        return int(round(self.infected_max / 100 * self.population * self.death_percentage))

    @property
    def affected(self):
        """."""
        return self.infected + self.imune

    @property
    def infected_max(self):
        """."""
        return 100*max(self.infected)

    @property
    def infected_max_nr(self):
        """."""
        return int(round(self.infected_max * self.population))

    @property
    def peak_day(self):
        """."""
        return np.argmax(self.infected)
