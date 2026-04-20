from kpler.sdk.configuration import Configuration
from kpler.sdk import Platform,FlowsDirection, FlowsSplit, FlowsPeriod, FlowsMeasurementUnit,RefinedProducts
from kpler.sdk.resources.flows import Flows
from datetime import date

flow_dir={'Export':FlowsDirection.Export,
          'Import':FlowsDirection.Import,
          'Net Exports':FlowsDirection.NetExport,
          'Net Imports':FlowsDirection.NetImport}

flow_units={
    'kbd':FlowsMeasurementUnit.KBD,
    'bbl':FlowsMeasurementUnit.BBL,
    'kb':FlowsMeasurementUnit.KB,
    'mmbbl':FlowsMeasurementUnit.MMBBL,
    'mt':FlowsMeasurementUnit.MT,
    'kt':FlowsMeasurementUnit.KT,
    't':FlowsMeasurementUnit.T,
    'cm':FlowsMeasurementUnit.CM
}

flow_period={
    'annually': FlowsPeriod.Annually,
    'monthly':FlowsPeriod.Monthly,
    'weekly':FlowsPeriod.Weekly,
    'eia-weekly':FlowsPeriod.EiaWeekly,
    'daily': FlowsPeriod.Daily
}

