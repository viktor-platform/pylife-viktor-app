import pylife.materialdata.woehler as woehler
from pylife.materiallaws import WoehlerCurve
import plotly.graph_objects as go
from pathlib import Path
import pandas as pd
import numpy as np

from viktor import (
    ViktorController,
    File,
)
from viktor.views import (
    PlotlyAndDataResult,
    PlotlyAndDataView,
    DataGroup,
    WebResult,
    DataItem,
    WebView,
)
from viktor.result import (
    DownloadResult,
)

from viktor.parametrization import (
    ViktorParametrization,
    MultiSelectField,
    DownloadButton,
    BooleanField,
    NumberField,
    OptionField,
    UserError,
    FileField,
    LineBreak,
    IsFalse,
    IsTrue,
    Lookup,
    Text,
    Tab,
)


def useFileForData(params, **kwargs):
    if params.tab2.useSampleData is True:
        parentFolder = Path(__file__).parent  # pylife-viktor-app
        filePath = parentFolder / "fatigue-data-plain.csv"
        with filePath.open() as f:
            df = pd.read_csv(filePath, sep="\t")
    else:
        filePath = params.tab2.fileUpload.file.copy().source
        df = pd.read_csv(filePath, sep="\t")
    df.columns = ["load", "cycles"]
    if params.tab2.useSetCycleLimit:
        load_cycle_limit = params.tab2.cycleLimit * 1000000
    else:
        load_cycle_limit = None
    df = woehler.determine_fractures(df, load_cycle_limit)
    return df

def useWohlerFile(params, **kwargs):
    if not params.tab2.wohlerDataUpload and not params.tab2.useSampleWohler:
            raise UserError("Please upload/select which wöhler data to use")
    filePath = params.tab2.wohlerDataUpload.file.copy().source
    wohlerParameters = pd.read_csv(filePath, sep="\t")
    wohlerParameters.index = ['k_1', 'ND', 'SD', 'TN', 'TS', 'failure_probability']
    del wohlerParameters[wohlerParameters.columns[0]]
    wohlerParameters = wohlerParameters.iloc[:,0]
    return wohlerParameters

def generateData(woehlerCurve, params, **kwargs):
    cycles = np.logspace(1.0, 8.0, 70)
    df = pd.DataFrame(index=cycles)
    for fp in params.failureProbs:
        new_data = woehlerCurve.basquin_load(cycles, failure_probability=fp)
        df.insert(len(df.columns), f"{fp}", new_data)
    return df

def wohlerGenerateData(type, params, **kwargs): 
    df = useFileForData(params)
    fatigue_data = df.fatigue_data
    fatigue_data.fatigue_limit
    if not params.tab2.useSampleWohler:
        wohlerData = useWohlerFile(params)
    elif type=='probit':
        wohlerData = woehler.Probit(fatigue_data).analyze()
    elif type=='MaxLike':
        if params.tab2.maxLikelihoodOption == "Infinite":
            wohlerData = woehler.MaxLikeInf(fatigue_data).analyze()
        else:
            if params.tab3.changeSlope and params.tab3.changeCycleEnduranceLimit and params.tab3.changeLoadEnduranceLimit and params.tab3.changeScatterTN and params.tab3.changeScatterTS:
                raise UserError("Please leave one of the parameters unfixed for calculations")
            fixedParams = {}
            if params.tab3.changeSlope:
                fixedParams["k_1"] = params.tab3.slopeValue
            if params.tab3.changeCycleEnduranceLimit:
                fixedParams["ND"] = params.tab3.cycleEnduranceLimit
            if params.tab3.changeLoadEnduranceLimit:
                fixedParams["SD"] = params.tab3.loadEnduranceLimit
            if params.tab3.changeScatterTN:
                fixedParams["TN"] = params.tab3.scatterTN
            if params.tab3.changeScatterTS:
                fixedParams["TS"] = params.tab3.scatterTS
            wohlerData = woehler.MaxLikeFull(fatigue_data).analyze(fixed_parameters=fixedParams)
    return wohlerData

def addWoehlerCurves(woehlerCurve, name, params, **kwargs):
    pd.options.plotting.backend = "plotly"
    df = useFileForData(params)
    fatigue_data = df.fatigue_data
    fatigue_data.fatigue_limit
    fractures = fatigue_data.fractures
    runouts = fatigue_data.runouts
    cycles = np.logspace(np.log10(df.cycles.min()), np.log10(df.cycles.max()), 100)
    fig = (
        go.Figure(
            [
                go.Scatter(
                    x=fractures.cycles,
                    y=fractures.load,
                    mode="markers",
                    name="fractures",
                ),
                go.Scatter(
                    x=runouts.cycles, y=runouts.load, mode="markers", name="runouts"
                ),
            ]
        )
        .update_xaxes(type="log")
        .update_yaxes(type="log")
        .update_layout(xaxis_title="Cycles", yaxis_title="Load")
    )
    for prob in np.sort(params.tab2.failureProbs):
        fig.add_scatter(
            x=cycles,
            y=woehlerCurve.basquin_load(cycles, failure_probability=prob),
            mode="lines",
            name=f"{name} {prob*100}%",
        )
    return fig

def makeDataGroup(wc):
    dataGroup = DataGroup(
        DataItem("k_1", wc[0]),
        DataItem("ND", wc[1]),
        DataItem("SD", wc[2]),
        DataItem("TN", wc[3]),
        DataItem("TS", wc[4])
    )
    return dataGroup


class Parametrization(ViktorParametrization):
    """Viktor Parametrization"""

    tab1 = Tab("Introduction")

    tab1.text1 = Text(
        """
# BOSCH Research: pyLife Fatigue Calculator

pyLife is an Open Source Python library for state of the art algorithms used in lifetime assessment
 of mechanical components subject to fatigue load.

## Purpose of the project

This library was originally compiled at Bosch Research to collect algorithms needed by different in
 house software projects, that deal with lifetime prediction and material fatigue on a component level.
 In order to allow for collaboration it was decided to release it as Open Source. Read this article about 
 [pyLife’s origin](https://www.bosch.com/stories/bringing-open-source-to-mechanical-engineering/) and 
 how it has become a tool used daily at BOSCH Research.

Not only is collaboration from science and education encouraged, but also from other commercial 
companies dealing with the topic of fatigue analysis. We commend this library to university teachers to use it 
for education purposes.

 pyLife is designed and programmed by [Johannes Mueller](https://github.com/johannes-mueller) 
 (Johannes.Mueller4@de.bosch.com) and [Daniel Kreuter](https://github.com/DKreuter) 
 (danielchristopher.kreuter@de.bosch.com) at BOSCH Research, the content of this app is based
 on the Master Thesis of Mustapha Kassem at TU Müchen. You may find more information on the content and what 
 functions are used in the [pyLife Cookbook](https://pylife.readthedocs.io/en/stable/demos/woehler_analyzer.html#).
        """
    )

    tab2 = Tab("Data upload")

    tab2.text2 = Text(
        """
## Data Upload and Wöhler Selection
In this section the data can be uploaded and the user may choose to generate
a wöhler curve based on the data or upload their own. Both files need to be .csv
and follow the basic structure of the pyLife sample data. Feel free to download
the sample data in order to have a template for your own data. Same can be done 
for the wöhler curve in the next section.
        """
    )

    tab2.fileUpload = FileField(
        "Upload Fatigue Data",
        visible=IsFalse(Lookup("tab2.useSampleData")),
        file_types=[".csv"],
        max_size=5_000_000,
    )
    tab2.useSampleData = BooleanField(
        "Use sample data",
        default=True,
        flex=30,
    )
    tab2.lb1 = LineBreak()
    tab2.downloadSampleData = DownloadButton(
        "Download sample data/template",
        method="downloadSampleFile",
        flex=100,
        longpoll=True,
    )

    tab2.lb2 = LineBreak()
    tab2.wohlerDataUpload = FileField(
        "Upload wohler Data",
        visible=IsFalse(Lookup("tab2.useSampleWohler")),
        file_types=[".csv"],
        max_size=5_000_000,
        flex=50
    )
    tab2.useSampleWohler = BooleanField(
        "Use Wöhler curves from data",
        default=True,
        flex=50,
    )

    tab2.lb3 = LineBreak()
    tab2.cycleLimit = NumberField(
        "Cycle limit (E6)",
        default=10,
        flex=50,
        visible=IsTrue(Lookup("tab2.useSetCycleLimit"))
    )
    tab2.useSetCycleLimit = BooleanField(
        "Set cycle limit",
        default=False,
        flex=30,
    )



    tab2.lb4 = LineBreak()
    tab2.failureProbs = MultiSelectField(
        "failure probabilities",
        visible=IsTrue(Lookup("tab2.useFailureProb")),
        options=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
        default=[0.1, 0.5, 0.9],
    )

    tab2.useFailureProb = BooleanField(
        "Set failure probabilities",
        default=False,
        flex=40,
    )

    tab2.lb5 = LineBreak()
    tab2.maxLikelihoodOption = OptionField(
        "Infinite or Full",
        options=["Infinite", "Full"],
        default="Infinite",
    )

    tab3 = Tab("Fix Parameters")
    tab3.text2 = Text(
        """
## Adjust Wöhler Curve Parameters 
Here you can choose to overwrite the parameters should you be 
unhappy with the wöhler curves from the data. You may choose to upload
or to overwrite the values in the table below.
        """
    )

    tab3.lb6 = LineBreak()
    tab3.slopeValue = NumberField(
        'New value for Slope k_1',
        visible=IsTrue(Lookup("tab3.changeSlope")),
        flex=60,
        )
    tab3.changeSlope = BooleanField(
        "Change Slope k_1",
        default=False,
        flex=40,
    )

    tab3.lb7 = LineBreak()
    tab3.cycleEnduranceLimit = NumberField(
        'New value for cycle endurance limit ND',
        visible=IsTrue(Lookup("tab3.changeCycleEnduranceLimit")),
        flex=60,
    )
    tab3.changeCycleEnduranceLimit = BooleanField(
        "Change ND",
        default=False,
        flex=30,
    )

    tab3.lb8 = LineBreak()
    tab3.loadEnduranceLimit = NumberField(
        'New value for load endurance limit SD',
        visible=IsTrue(Lookup("tab3.changeLoadEnduranceLimit")),
        flex=60,
        )
    tab3.changeLoadEnduranceLimit = BooleanField(
        "Change SD",
        default=False,
        flex=30,
    )

    tab3.lb9 = LineBreak()
    tab3.scatterTN = NumberField(
        'New value for scatter value TN',
        visible=IsTrue(Lookup("tab3.changeScatterTN")),
        flex=60,
        )
    tab3.changeScatterTN = BooleanField(
        "Change Scatter value TN",
        default=False,
        flex=40,
    )

    tab3.lb10 = LineBreak()
    tab3.scatterTS = NumberField(
        'New value for scatter value TS',
        visible=IsTrue(Lookup("tab3.changeScatterTS")),
        flex=60,
        )
    tab3.changeScatterTS = BooleanField(
        "Change Scatter value TS",
        default=False,
        flex=40,
    )

    tab3.lb11 = LineBreak()
    tab3.downloadWohlerData = DownloadButton(
        "Download Modified Wöhler Curve Data",
        method="performDownload",
        flex=100,
        longpoll=True,
    )




class Controller(ViktorController):
    viktor_enforce_field_constraints = (
        True  # Resolves upgrade instruction https://docs.viktor.ai/sdk/upgrades#U83
    )

    label = "My Entity Type"
    parametrization = Parametrization

    @PlotlyAndDataView("Probit", duration_guess=2)
    def probitPlotly(self, params, **kwargs):
        if not params.tab2.fileUpload and not params.tab2.useSampleData:
            raise UserError("Please upload/select data to use")
        pd.options.plotting.backend = "plotly"
        wc = wohlerGenerateData('probit', params)
        probitFig = addWoehlerCurves(wc.woehler, "Probit", params)
        return PlotlyAndDataResult(probitFig.to_json(), makeDataGroup(wc))

    @PlotlyAndDataView("Maximum Likelihood", duration_guess=2)
    def maxLikelihoodPlotly(self, params, **kwargs):
        if not params.tab2.fileUpload and not params.tab2.useSampleData:
            raise UserError("Please upload/select data to use")
        pd.options.plotting.backend = "plotly"
        wc = wohlerGenerateData('MaxLike', params)
        MaxLikeFig = addWoehlerCurves(
            wc.woehler, f"MaxLikelihood {params.tab2.maxLikelihoodOption}", params
        )
        return PlotlyAndDataResult(MaxLikeFig.to_json(), makeDataGroup(wc))

    @WebView("What's next?", duration_guess=1)
    def whats_next(self, **kwargs):
        """Initiates the process of rendering the "What's next?" tab."""
        html_path = Path(__file__).parent / "final_step.html"
        with html_path.open() as f:
            html_string = f.read()
        return WebResult(html=html_string)

    def performDownload(self, params, **kwargs):
        maxLikelihoodResult = wohlerGenerateData('MaxLike', params)
        df = pd.DataFrame(maxLikelihoodResult.values, maxLikelihoodResult.index, columns=['value'])
        download = df.to_csv(sep='\t')
        return DownloadResult(download, file_name="woehler_data.csv")

    def downloadSampleFile(self, **kwargs): 
        filePath = Path(__file__).parent/"fatigue-data-plain.csv"
        sampleData = File.from_path(filePath)
        return DownloadResult(sampleData, "fatigue-sample-data.csv")
    