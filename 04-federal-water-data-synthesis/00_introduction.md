# Module overview

Hydrologic systems are extremely complex. Accurate information is critical for managing water resources, and this need is emphasized by the existence of multiple Federal agencies who each fill an important niche in the water data landscape. In this module, you will explore the strengths and unique capabilities of each data product, learn about their limitations, and build skills to use them together in order to build a more robust hydrologic picture.

The module has three lessons:

1. **[Comparative overview](01_comparative_overview.md):** how USGS observations, NOAA National Water Model (NWM) output and NASA SWOT observations differ in spatial coverage, temporal availability and accuracy, and what each agency recommends about using its data.
2. **[Synthesizing Federal data products](02_synthesize_river_data.md):** a case study of the **December 2025 Skagit River flood** in Washington. An atmospheric river drove the river near Mount Vernon (USGS 12200500) to a record peak. We look at the flood from the ground (USGS gage observations and field measurements), ahead in time (NWM forecasts issued as the flood approached), and from above (SWOT water surface elevation, and possibly water extent).
3. **[Additional Federal water data](03_additional_data.md):** short tours of related products (SWOT discharge, AORC precipitation and the NextGen hydrofabric) and where to go next.

:::{admonition} TODO (dev team): Match Lane B's final 04/02 SWOT section
:class: attention
Match Lane B's final 04/02 SWOT section
:::

This module builds on Module 2 (what each product is) and Module 3 (how to get it). Code examples reuse the Module 3 access patterns; see each Module 3 lesson for setup.

## Learning objectives

By the end of this module, learners should be able to:
- Compare USGS, NWM and SWOT river data by spatial coverage, temporal availability, accuracy and quality information, using the shared vocabulary (Location Identifier, Variable, Variable unit, Data Quality Flag(s)).
- Link the same river location across agencies: a USGS monitoring location, an NWM `feature_id` (NHDPlus COMID; `nwm_feature_id` in `hydrotools`) and a SWOT SWORD reach.
- Retrieve and line up observations, forecasts and satellite measurements for a single event, accounting for differences in units, vertical reference, time zone and sampling.
- Explain what each product can and cannot show during a flood, for example gage ratings at out-of-bank flows, forecast changes with lead time, and satellite overpass timing.
- Summarize each agency's recommendations for using its data, and choose the product, or combination of products, that fits a research question.
- Identify related Federal products (SWOT SoS discharge, AORC precipitation, the NextGen hydrofabric) and take a first step to access each.

## Important concepts and terminology

- **Synthesis.** Using several independent sources together, so that each one's strengths cover another's gaps, and so their agreement (or disagreement) tells you how confident to be.
- **Observation vs. model vs. remote sensing.** USGS reports measured (and rated) conditions at points; the NWM simulates and forecasts conditions everywhere on its network; SWOT observes water from space when it passes over. They carry different kinds of error, so they are complementary rather than interchangeable.
- **Crosswalking locations.** Each agency has its own Location Identifier. Connecting them (gage ↔ COMID ↔ SWORD reach) is often the first, and most error-prone, step of any synthesis.
- **Common units and references.** USGS discharge is in ft³/s and gage height is relative to a local gage datum; NWM streamflow is in m³/s; SWOT water surface elevation is in meters relative to a geoid ([Meet NASA SWOT](../02-federal-water-data-landscape/01_meet_nasa_swot.md)). Convert units, and compare _changes_ when vertical references differ.
- **Forecast lead time.** A forecast is labeled by when it was issued (its reference time) and how far ahead it looks. Comparing forecasts issued at different times before an event shows how the predicted peak evolved.
- **Data provider recommendations.** Each agency publishes guidance on appropriate use (for example, provisional vs. approved data, official forecasts vs. model guidance, and quality flags). Following it keeps analyses defensible.

:::{admonition} TODO (dev team): Cite USGS gage datum explanation
:class: attention
Cite USGS gage datum explanation
:::

:::{admonition} Partner review (NASA): Important concepts and terminology
:class: important
Confirm the module objectives and concept descriptions.
:::

:::{admonition} Partner review (NOAA): Important concepts and terminology
:class: important
Confirm the module objectives and concept descriptions.
:::

:::{admonition} Partner review (USGS): Important concepts and terminology
:class: important
Confirm the module objectives and concept descriptions.
:::