from kpler.sdk.configuration import Configuration
from kpler.sdk import Platform,FlowsDirection, FlowsSplit, FlowsPeriod, FlowsMeasurementUnit,RefinedProducts
from kpler.sdk.resources.flows import Flows
from datetime import date

flow_dir={'Exports':FlowsDirection.Export,
          'Imports':FlowsDirection.Import,
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


flow_split={
    'origin countries': FlowsSplit.OriginCountries,
    'destination countries':FlowsSplit.DestinationCountries,
    'buyers':FlowsSplit.Buyers,
    'charterers':FlowsSplit.Charterers,
    'crude quality':FlowsSplit.CrudeQuality, 
    'destination continents':FlowsSplit.DestinationContinents,
    'destination installations':FlowsSplit.DestinationInstallations,
    'destination padds':FlowsSplit.DestinationPadds,
    'destination subcontinents':FlowsSplit.DestinationSubcontinents,
    'destination trading regions':FlowsSplit.DestinationTradingRegions, 
    'grades':FlowsSplit.Grades,
    'long haul vessel type':FlowsSplit.VesselType,
    'long haul vessel type cpp':FlowsSplit.VesselTypeCpp,
    'long haul vessel type oil':FlowsSplit.VesselTypeOil,
    'origin continents':FlowsSplit.OriginContinents, 
    'origin installations':FlowsSplit.OriginInstallations, 
    'origin padds':FlowsSplit.OriginPadds,
    'origin subcontinent':FlowsSplit.OriginSubcontinents,
     'origin trading region':FlowsSplit.OriginTradingRegions,
     'products':FlowsSplit.Products, 
    'routes':FlowsSplit.Routes, 
    'sellers':FlowsSplit.Sellers,
    'source':FlowsSplit.Sources, 
    'total':FlowsSplit.Total,
    'trade status':FlowsSplit.TradeStatus,
    'vessel type':FlowsSplit.VesselType, 
    'vessel type cpp':FlowsSplit.VesselTypeCpp,
    'vessel type oil': FlowsSplit.VesselTypeOil
}