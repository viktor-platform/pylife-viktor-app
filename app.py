import pylife.materialdata.woehler as woehler
from pylife.materiallaws import WoehlerCurve
import plotly.graph_objects as go
from pathlib import Path
import pandas as pd
import numpy as np

from viktor import ViktorController
from viktor.views import (
    PlotlyResult,
    PlotlyView,
    WebResult,
    WebView,
)
from viktor.result import(
    SetParamsResult,
)

from viktor.parametrization import (
    ViktorParametrization,
    MultiSelectField,
    SetParamsButton,
    BooleanField,
    NumberField,
    OptionField,
    FileField,
    LineBreak,
    TextField,
    IsFalse,
    IsTrue,
    Lookup,
    Table,
    Text,
    Tab,
)

def useFileForData(params, **kwargs):
    if params.tab1.useSampleData is True:
        parentFolder = Path(__file__).parent #pylife-viktor-app
        filePath = parentFolder/'fatigue-data-plain.csv'
    else:
        filePath = params.FileUpload
    with filePath.open() as f:
        df = pd.read_csv(filePath, sep='\t')
    df.columns = ['load', 'cycles']
    load_cycle_limit = None # or for example 1e7
    df = woehler.determine_fractures(df, load_cycle_limit)
    fatigue_data = df.fatigue_data
    fatigue_data.fatigue_limit
    return df

def generateData(woehlerCurve, params, **kwargs):
    cycles = np.logspace(1., 8., 70)
    df = pd.DataFrame(index=cycles)
    for fp in params.failureProbs:
        new_data = woehlerCurve.basquin_load(cycles, failure_probability=fp)
        df.insert(len(df.columns), f"{fp}", new_data)
    return df

def addWoehlerCurves(woehlerCurve, name, params, **kwargs):
    pd.options.plotting.backend = "plotly"
    df = useFileForData(params)
    fatigue_data = df.fatigue_data
    fatigue_data.fatigue_limit
    fractures = fatigue_data.fractures
    runouts = fatigue_data.runouts
    cycles = np.logspace(np.log10(df.cycles.min()), np.log10(df.cycles.max()), 100)
    fig = go.Figure([go.Scatter(x=fractures.cycles, y=fractures.load, mode='markers', name='fractures'),
        go.Scatter(x=runouts.cycles, y=runouts.load, mode='markers', name='runouts'),
        go.Scatter(x=[df.cycles.min(), df.cycles.max()], y=[fatigue_data.fatigue_limit]*2, mode='lines', name='fatigue limit')]).update_xaxes(type='log').update_yaxes(type='log').update_layout(xaxis_title='Cycles', yaxis_title='Load')
    for prob in np.sort(params.tab1.failureProbs):
        fig.add_scatter(x= cycles, y=woehlerCurve.basquin_load(cycles, failure_probability=prob), mode='lines', name=f"{name} {prob*100}%")
    return fig

class Parametrization(ViktorParametrization):
    """Viktor Parametrization"""

    tab1 = Tab('Data Analysis')

    tab1.text1 = Text(
        """
# Welcome to the PyLife demonstration app!

This is a sample app demonstrating how PyLife, a package designed by BOSCH Research and made 
open-source, makes stress and fatigue calculations.

        """
    )

    tab1.fileUpload = FileField('Upload Fatigue Data', 
        visible=IsFalse(Lookup('tab1.useSampleData')),
        file_types=['.csv'], 
        max_size=5_000_000
    )
    tab1.useSampleData = BooleanField("Use sample data",
        default=True,
        flex=40,
    )

    tab1.lb0 = LineBreak()
    tab1.failureProbs = MultiSelectField("failure probabilities",
        visible=IsTrue(Lookup("tab1.useFailureProb")),
        options=[0.1,
                 0.2,
                 0.3,
                 0.4,
                 0.5,
                 0.6,
                 0.7,
                 0.8,
                 0.9],
        default=[0.1, 0.5, 0.9],
    )

    tab1.useFailureProb = BooleanField("Use set failure probabilities",
        default=False,
        flex=40,
    )

    tab1.lb1 = LineBreak()
    tab1.maxLikelihoodOption = OptionField("Infinite or Full",
        options=['Infinite', 
                 'Full'],
        default='Infinite',
    )

    tab2 = Tab('Fix Parameters')
    tab2.text2 = Text(
        """
Here you can choose to overwrite the parameters should you be 
unhappy with the wöhler curves from the data. The Choices can 
be modified below. Note this only holds for Maximum Likelihood 
Full.
        """

    )

    tab2.modifyWoehler = BooleanField("Fix Parameters",
        default=False,
        flex=40,
    )
    
    tab2.lbx = LineBreak()
    tab2.tableOutput = Table(
        "Table of parameters",
        visible=IsTrue(Lookup('tab2.modifyWoehler'))
    )
    tab2.tableOutput.name = TextField('Name')
    tab2.tableOutput.woehlerParams = NumberField("Parameter Value", num_decimals=1)

    tab2.lbx = LineBreak()
    tab2.setParameters = SetParamsButton(
        "Call/Reset parameters", 
        method="updateParams",
        visible=IsTrue(Lookup('tab2.modifyWoehler')),
        flex=100,
    )


class Controller(ViktorController):
    viktor_enforce_field_constraints = True  # Resolves upgrade instruction https://docs.viktor.ai/sdk/upgrades#U83

    label = 'My Entity Type'
    parametrization = Parametrization

    @PlotlyView("Elementary Analysis", duration_guess=3)
    def elementaryAnalysisPlotly(self, params, **kwargs):
        pd.options.plotting.backend = "plotly"
        df = useFileForData(params)
        fatigue_data = df.fatigue_data
        fatigue_data.fatigue_limit
        elementary_result = woehler.Elementary(fatigue_data).analyze()
        wc = elementary_result.woehler
        elementaryFig = addWoehlerCurves(wc, 'Elementary', params)  
        return PlotlyResult(elementaryFig.to_json())
    
    @PlotlyView("Probit", duration_guess=2)
    def probitPlotly(self, params, **kwargs):
        pd.options.plotting.backend = "plotly"
        df = useFileForData(params)
        fatigue_data = df.fatigue_data
        fatigue_data.fatigue_limit
        probitResult = woehler.Probit(fatigue_data).analyze()
        wc = probitResult.woehler
        probitFig = addWoehlerCurves(wc, 'Probit', params)  
        return PlotlyResult(probitFig.to_json())
    
    @PlotlyView("Maximum Likelihood", duration_guess=2)
    def maxLikelihoodPlotly(self, params, **kwargs):
        pd.options.plotting.backend = "plotly"
        df = useFileForData(params)
        fatigue_data = df.fatigue_data
        fatigue_data.fatigue_limit
        if params.tab1.maxLikelihoodOption == 'Infinite':
            maxLikelihoodResult = woehler.MaxLikeInf(fatigue_data).analyze()
        else:
            if params.tab2.modifyWoehler is True and len(params.tab2.tableOutput)>1:
                fixedParams = {
                'k_1': params.tab2.tableOutput[0].woehlerParams,
                'ND': params.tab2.tableOutput[1].woehlerParams,
                'SD': params.tab2.tableOutput[2].woehlerParams,
            }
            else:
                fixedParams = {}
            maxLikelihoodResult = woehler.MaxLikeFull(fatigue_data).analyze(fixed_parameters=fixedParams)
        wc = maxLikelihoodResult.woehler
        probitFig = addWoehlerCurves(wc, f"MaxLikelihood {params.tab1.maxLikelihoodOption}", params)  
        return PlotlyResult(probitFig.to_json())
    
    @WebView("What's next?", duration_guess=1)
    def whats_next(self, **kwargs):
        """Initiates the process of rendering the "What's next?" tab."""
        html_path = Path(__file__).parent / "final_step.html"
        with html_path.open() as f:
            html_string = f.read()
        return WebResult(html=html_string)

    @staticmethod
    def updateParams(params, **kwargs):
        df = useFileForData(params)
        fatigue_data = df.fatigue_data
        fatigue_data.fatigue_limit  
        maxLikelihoodResult = woehler.MaxLikeFull(fatigue_data).analyze()

        return SetParamsResult({
            "tab2": {
            "tableOutput": [
        {'name': 'K_1', 'woehlerParams': maxLikelihoodResult[0]},
        {'name': 'ND', 'woehlerParams': maxLikelihoodResult[1]},
        {'name': 'SD', 'woehlerParams': maxLikelihoodResult[2]},
        ]
        }
        }
        )
