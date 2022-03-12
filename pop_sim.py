import matplotlib.pyplot as plt
from pandas import Series
from numpy.random import normal
import scipy.stats as st

pop_sizes = {'Ashkenazi': 0.02}
trait_name = "IQ"

TRAIT_VALUES = {"IQ": {'pop_mean': 100, 'pop_sd': 15}}

class Population():

    pop_num = 300_000_000

    def __init__(self, sub_name, sub_prop, sd_diff, sd_thresh=4, trait_name="IQ") -> None:
        self.sub_prop = sub_prop
        self.sd_diff = sd_diff
        self.sd_thresh = sd_thresh
        self.sub_name = sub_name
        self.most_pop, self.most_pop_sub = None, None

        self.trait_name = trait_name
        self.pop_mean = TRAIT_VALUES[trait_name]['pop_mean']
        self.pop_sd = TRAIT_VALUES[trait_name]['pop_sd']

    def __call__(self):
        self.pop = normal(self.pop_mean, self.pop_sd, size=self.pop_num)
        self.pop_sub = normal(self.pop_sub_mean, self.pop_sd, size=self.pop_sub_num)


    @property
    def pop_sub_num(self):
        return int(self.pop_num * self.sub_prop)


    @property
    def pop_name(self):
        return f"Non-{self.sub_name}"

    @property
    def pop_sub_mean(self):
        return int(self.pop_mean + self.sd_diff * self.pop_sd)


    def plot_frequency(self, density=False):
        plt.hist(self.pop, bins=50, alpha=0.5, label=self.pop_name,
                    density=density)
        plt.hist(self.pop_sub, bins=50, alpha=0.5, color='red', label=self.sub_name,
                    density=density)
        abs_or_rel = "Relative" if density else "Absolute"
        plt.title(f"{abs_or_rel} Frequency")
        plt.yticks([])
        plt.legend()
        plt.show()


    def pop_most(self, n=5):
        return [int(val) for val in Series(self.pop).nlargest(n)]

    def pop_sub_most(self, n=5):
        return [int(val) for val in Series(self.pop_sub).nlargest(n)]


    def get_thresh(self):
        thresh_value = self.pop_mean + self.pop_sd * self.sd_thresh
        self.most_pop = [m for m in self.pop if m > thresh_value]
        self.most_pop_sub = [a for a in self.pop_sub if a > thresh_value]


    def prop_most(self):
        prop = len(self.most_pop_sub) / (len(self.most_pop) + len(self.most_pop_sub))
        return "{:.0%}".format(prop)


    def plot_thresh(self):
        density = False
        plt.hist(self.most_pop, bins=50, alpha=0.5, label=self.sub_name,
                    density=density)
        plt.hist(self.most_pop_sub, bins=50, alpha=0.5, color='red', label=self.pop_name,
                    density=density)
        abs_or_rel = "Relative" if density else "Absolute"
        plt.title(f"{abs_or_rel} Frequency")
        plt.ylabel("Frequency")
        plt.xlabel(self.trait_name)
        plt.legend()
        plt.show()

    def one_of(self, sub=False):
        """Those above 4 SDs or 160 IQ are one out of this many people (rarity):"""
        loc = self.sd_diff if sub else 0
        percentile = st.norm.cdf(self.sd_thresh, loc=loc)
        one_of_n = 1 / (1 - percentile)
        one_of_n = f"{one_of_n:,.0f}"
        return one_of_n

