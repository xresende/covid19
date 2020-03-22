#!/usr/bin/env python3

"""."""
import random
from matplotlib import pyplot as plt

from model import COVID19
from data import DATA_BRAZIL


random.seed(13)


def covid19_summary(covid):
    """."""
    print('nr. dias duplicação : {:.6f}'.format(covid.doublingdays))
    print('nr. dias doença     : {:.6f}'.format(covid.halvingdays))
    print('final de infectados : {:.2f} %'.format(covid.infected_max))
    print('número de mortes    : {:d}'.format(covid.death_toll))
    print('dia de pico         : {:d}'.format(covid.peak_day))
    print('')


def covid19_calibrate(covid):
    """."""
    print('--- calibração ---')
    covid.calibrate(100000)
    # covid.calibrate(0)
    print()
    return covid


def covid19_sceneries1(covid, nr_days):
    """."""
    doublingdays = covid.doublingdays

    print('--- cenário ---')
    covid.doublingdays = doublingdays * 1
    covid.evolve(init=True, nr_days=nr_days)
    covid19_summary(covid)
    fmts = 'taxa de duplicação: {:.2f} dias, # mortes: {}'
    label = fmts.format(covid.doublingdays, covid.death_toll)
    plt.plot(100*covid.infected, label=label)
    print()

    print('--- cenário ---')
    covid.doublingdays = doublingdays * 2
    covid.evolve(init=True, nr_days=nr_days)
    covid19_summary(covid)
    fmts = 'fator de redução: {:.1f}, # mortes: {}'
    label = fmts.format(covid.doublingdays/doublingdays, covid.death_toll)
    plt.plot(100*covid.infected, label=label)
    print()

    print('--- cenário ---')
    covid.doublingdays = doublingdays * 3
    covid.evolve(init=True, nr_days=nr_days)
    covid19_summary(covid)
    fmts = 'fator de redução: {:.1f}, # mortes: {}'
    label = fmts.format(covid.doublingdays/doublingdays, covid.death_toll)
    plt.plot(100*covid.infected, label=label)
    print()

    print('--- cenário ---')
    covid.doublingdays = doublingdays * 4
    covid.evolve(init=True, nr_days=nr_days)
    covid19_summary(covid)
    fmts = 'fator de redução: {:.1f}, # mortes: {}'
    label = fmts.format(covid.doublingdays/doublingdays, covid.death_toll)
    plt.plot(100*covid.infected, label=label)
    print()

    print('--- cenário ---')
    covid.doublingdays = doublingdays * 5
    covid.evolve(init=True, nr_days=nr_days)
    covid19_summary(covid)
    fmts = 'fator de redução: {:.1f}, # mortes: {}'
    label = fmts.format(covid.doublingdays/doublingdays, covid.death_toll)
    plt.plot(100*covid.infected, label=label)
    print()

    plt.xlabel('Número de dias desde o primeiro caso')
    plt.ylabel('População infectada [%]')
    plt.grid()
    plt.legend()
    # plt.yscale('log')
    tfmt = 'COVID19 - Cenários de Evolução\n (taxa de mortalidade {:.1f} % - {})'
    plt.title(tfmt.format(covid.death_percentage*100, covid.country))
    plt.show()


def covid19_compare_model_data(covid):
    """."""
    _, infected, history = covid.calc_residue()
    plt.plot(infected, label='modelo')
    plt.plot(history, 'o', label='dados')
    plt.xlabel('Número de dias desde o primeiro caso')
    plt.ylabel('Número de indivíduos infectados')
    plt.grid()
    plt.legend()
    tfmt = 'COVID19 - Comparação entre modelo e dados.'
    plt.title(tfmt.format())
    plt.show()


def run(country):
    """."""
    # country = copy.deepcopy(country)
    # country['history'] = DATA_KOREA['history']

    # create model
    covid = COVID19(**country)

    # calibrate with history
    # covid = covid19_calibrate(covid)

    # compare model-data
    covid19_compare_model_data(covid)

    # set number of infected
    covid.init()

    # plot sceneries
    covid19_sceneries1(covid, nr_days=360*3)


run(DATA_BRAZIL)
