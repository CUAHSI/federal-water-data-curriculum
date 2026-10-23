# Module overview

Every dataset you use was shaped by decisions someone made about how it was collected, processed, documented and shared. This module is about making those decisions well in your own work, so that your results can be checked, rebuilt and reused. Often the person most likely to need them is **future you**.

The module has three lessons that build on each other:

- **Open science** is the umbrella. It covers the values behind how you and your team work, and why they matter.
- **Data management** is how you put those values into practice while you collect and analyze data.
- **Data publishing** is how you archive and share your final results, so they still meet those open science goals long after the project ends.

## Learning objectives

By the end of this module, learners should be able to:
- Explain open science, FAIR principles, and reproducibility best practices, and their benefits to science products and the science community.
- Outline the key elements of a data management plan and articulate the benefits of publishing scientific data in an appropriate repository.

These break down into:
- Describe open science as a spectrum that covers both research products and the processes behind them, and recognize that definitions vary.
- Explain the {term}`FAIR principles <FAIR principles>`, how FAIR differs from open, and why the {term}`CARE principles <CARE principles>` are an important check on any project's data sources.
- Explain what {term}`reproducibility <Reproducibility>` means in this course, how it relates to {term}`replicability <Replicability>`, and why it is a continuum rather than all-or-nothing.
- Apply three simple data management approaches: project organization, machine-readable data and documentation.
- Choose a suitable repository, and decide whether to publish derived data as a snapshot of the values or as a recipe for recreating them.

## The lessons

1. [Open Science](01_open_science.md): what open science is, the FAIR and CARE principles, common barriers, and practical ways to start.
2. [Data Management](02_data_management.md): {term}`data management plans <Data management plan>`, what reproducibility means, and three simple approaches you can start using today.
3. [Data Publishing](03_data_publishing.md): FAIR in action, choosing a repository (with a closer look at HydroShare), publishing derived data, and peer review of data and code.

Each lesson ends with a short "Now you try it" activity and Further reading. Module 1 is conceptual, so unlike later modules it has no code and no software environment to set up.

## Important concepts and terminology

- **Future you.** The person most likely to need to rebuild or reuse your work is you, months or years later, once the details have faded. Each lesson comes back to this idea: if your future self could pick up the work without help, others probably can too.
- **Open is not the same as FAIR.** Open is about who can get the data. {term}`FAIR <FAIR principles>` is about how easily people and machines can find, access, combine and reuse them. Restricted data can still be FAIR if the rules for access are clear.
- **Reproducibility is a continuum.** It starts with documentation and scripted steps, and grows through version control and modular code to automated pipelines. You don't need every tool to make real progress.
- **{term}`Metadata` and the {term}`README`.** Metadata describe your data: the who, what, when, where, why and how. The README is the front page that ties a project or dataset together.
- **{term}`Persistent identifiers <Persistent identifier>`.** A {term}`DOI` gives a published dataset or piece of software a permanent link that others can cite.
