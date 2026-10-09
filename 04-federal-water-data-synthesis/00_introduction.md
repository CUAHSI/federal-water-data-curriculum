# Module overview

Hydrologic systems are extremely complex. Accurate information is critical for managing water resources, and this need is emphasized by the existence of multiple Federal agencies who each fill an important niche in the water data landscape. In this module, you will explore the strengths and unique capabilities of each data product, learn about their limitations, and build skills to use them together in order to build a more robust hydrologic picture.

The module has three lessons:

1. **[Comparative overview](01_comparative_overview.md):** how NASA Surface Water and Ocean Topography (SWOT) observations, NOAA National Water Model (NWM) output and USGS Water Data for the Nation (WDFN) observations differ in spatial coverage, temporal availability and accuracy, and what each agency recommends about using its data.
2. **[Synthesizing Federal data products](02_synthesize_river_data.md):** a case study of the **December 2025 Skagit River flood** in Washington. An atmospheric river drove the river near Mount Vernon (USGS 12200500) to a record crest (the highest stage on record). We look at the flood from the ground (USGS gage observations and field measurements), ahead in time (NWM forecasts issued as the flood approached), and from above (SWOT water surface elevation and water extent). This lesson tells the story in the order you would meet the flood, so unlike the rest of the course it starts with USGS.

3. **[Additional Federal water data](03_additional_data.md):** a pointer to SWOTViz, a CUAHSI browser viewer for SWOT data, then short tours of related products (SWOT discharge, AORC precipitation and the NextGen hydrofabric) and where to go next.

This module builds on Module 2 (what each product is) and Module 3 (how to get it). Code examples reuse the Module 3 access patterns, in one Module 4 {term}`conda environment <Conda environment>`, `m04-synthesis` (`environments/m04-synthesis.yml`); the case study shows how to create it.

## Learning objectives

By the end of this module, learners should be able to:
- Compare and describe the capabilities and limitations of NASA SWOT, NOAA NWM, and USGS WDFN data for a single flood event at the appropriate scales and resolutions.

These break down into:
- Compare SWOT, NWM and WDFN river data by spatial coverage, temporal availability, accuracy and quality information, using the course's shared concepts ({term}`location identifier <Location identifier>`, {term}`variable <Variable>`, {term}`variable unit <Variable unit>`, {term}`time <Time>`, {term}`data quality flag(s) <Data quality flag(s)>`, {term}`version / provenance <Version / provenance>` and {term}`data unit <Data unit>`).
- Link the same river location across agencies: a SWOT {term}`SWORD` reach, an NWM {term}`feature_id` (NHDPlus {term}`COMID`; `nwm_feature_id` in `hydrotools`) and a USGS monitoring location.
- Retrieve and line up observations, forecasts and satellite measurements for a single event, accounting for differences in units, vertical reference, time zone and sampling.
- Explain what each product can and cannot show during a flood, for example gage ratings at out-of-bank flows, forecast changes with lead time, and satellite overpass timing.
- Summarize each agency's recommendations for using its data, and choose the product, or combination of products, that fits a research question.
- Identify related Federal products (SWOT SoS discharge, AORC precipitation, the NextGen hydrofabric) and take a first step to access each.

## Important concepts and terminology

- **Synthesis.** Using several independent sources together, so that each one's strengths cover another's gaps, and so their agreement (or disagreement) tells you how confident to be.
- **Remote sensing vs. model vs. observation.** SWOT observes water from space when it passes over; the NWM simulates and forecasts conditions everywhere on its network; USGS reports measured (and rated) conditions at points. They carry different kinds of error, so they are complementary rather than interchangeable.
- **Crosswalking locations.** Each agency has its own location identifier. Connecting them (SWORD reach ↔ COMID ↔ gage) is often the first, and most error-prone, step of any synthesis.
- **Common units and references.** SWOT {term}`water surface elevation <Water surface elevation>` is in meters relative to a geoid ([Meet NASA SWOT](../02-federal-water-data-landscape/01_meet_nasa_swot.md)); NWM streamflow is in m³/s; USGS discharge is in ft³/s and {term}`gage height <Gage height>` is relative to a local gage datum. Convert units, and compare _changes_ when vertical references differ.

  :::{admonition} TODO (dev team): Gage datum citation
  :class: attention
  Cite USGS gage datum explanation. (Refers to: “**Common units and references.** USGS discharge is in ft³/s and gage height is relative to a local gage datum”)
  :::

- **Forecast lead time.** A forecast is labeled by when it was issued (its {term}`forecast reference time <Forecast reference time>`) and how far ahead it looks. Comparing forecasts issued at different times before an event shows how the predicted peak evolved.
- **Data provider recommendations.** Each agency publishes guidance on appropriate use (for example, quality flags, official forecasts vs. model guidance, and provisional vs. approved data). Following it keeps analyses defensible.
- **Reproducible synthesis.** Combining three products multiplies what you need to record: each product's version (SWOT product version, NWM model version, USGS approval status), your query (identifiers, dates, product names) and your access dates. Module 1 covers why ([reproducibility techniques](../01-data-best-practices/02_data_management.md#reproducibility-techniques), [publishing derivative data](../01-data-best-practices/03_data_publishing.md#publishing-derivative-data)); the case study shows one way to do it.

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

:::{admonition} TODO (dev team): Learner-review friction items (P6.5.4)
:class: attention
From the integration-pass learner review (2026-10-09). Not yet fixed:
- The objective "take a first step to access each" can't be met for the hydrofabric (no anonymous access now); reword if the objective isn't fixed by issue #36.
- Link {term}`Lead time`, {term}`Gage datum` and say "EGM2008 geoid" to match Modules 2–3.
:::
