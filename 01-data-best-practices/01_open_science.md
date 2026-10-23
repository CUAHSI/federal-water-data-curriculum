# Open Science

"Open science" is the umbrella value system for data best practices, which at their core help facilitate collaborative science. There is no single agreed definition. The U.S. federal government uses this one, from the White House Office of Science and Technology Policy (OSTP) and the National Science and Technology Council ([OSTP, 2023](https://bidenwhitehouse.archives.gov/ostp/news-updates/2023/01/11/fact-sheet-biden-harris-administration-announces-new-actions-to-advance-open-and-equitable-research)):

> "The principle and practice of making research products and processes available to all, while respecting diverse cultures, maintaining security and privacy, and fostering collaborations, reproducibility, and equity."

Other organizations word it differently, so you may meet other definitions elsewhere. Notice that this one covers *processes* as well as products: open science is about how you and your team work, not only about what you share at the end. It treats other scientists and disciplines as collaborators. We all benefit from transparent and {term}`reproducible <Reproducibility>` research, as it helps ensure the integrity and usability of scientific findings going into the future. This is especially true for water science and common complications water scientists have to navigate: fragmented community, data-intensive problems, and funder mandates.

Open science exists on a spectrum made up of open data, open code, open access publications, open methods/protocols, and open processes, such as developing code in a public repository and sharing work in progress. This module focuses mostly on open data, open code, and open processes.

Many groups support researchers who want to work this way. [The Turing Way](https://book.the-turing-way.org) is a community-written handbook on reproducible, ethical and collaborative data science. [Openscapes](https://openscapes.org) is a movement that helps researchers connect and build confidence in open, data-intensive science. NASA's Transform to Open Science (TOPS) initiative offers [Open Science 101](https://science.data.nasa.gov/features-events/open-science-training), a free online course. For Indigenous data governance, the [Global Indigenous Data Alliance (GIDA)](https://www.gida-global.org/careprinciples) maintains the CARE principles described below.

## Open science in practice

Open science is no longer an optional "nice to have" aspect of research. Funders and journals increasingly require shared data and metadata as part of the publication process.

Some requirements from [NSF's Public Access Policy](https://www.nsf.gov/policies/document/faq-public-access#qa-group-1) include {term}`data management plans <Data management plan>`, machine-readable {term}`metadata <Metadata>`, and for publications to be available free of charge. For awards made on or after 22 January 2026, NSF also requires recipients to share all data supporting NSF-funded publications at the time of publication, removes the 12-month embargo (a waiting period before a paper must be made public), and moves the data management and sharing plan to a tool on Research.gov ([NSF 26-202](https://www.nsf.gov/policies/document/pappg24-1-supplement-2)). These changes follow the [2022 OSTP memo](https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/08/08-2022-OSTP-Public-Access-Memo.pdf) on free, immediate, and equitable access to federally funded research.

[AGU's Position Statement on Data](https://www.agu.org/science-policy/position-statements/open-data) emphasizes "Preserving Open Data as a World Heritage to Secure our Future", including topics like ensuring equitable access to trusted and reusable data, implementing metadata standards across disciplines and domains, and taking collective responsibility in maintaining data infrastructure.

## FAIR and CARE

The {term}`FAIR principles <FAIR principles>` ([Wilkinson et al., 2016](https://doi.org/10.1038/sdata.2016.18); [GO FAIR](https://www.go-fair.org/fair-principles/)) describe how easily people *and machines* can find, access, combine, and reuse data. FAIR is related to openness, but it isn't the same thing. The principles allow for authentication and authorization where necessary, so restricted data can still be FAIR as long as the rules for getting access are clear. FAIR is also something you build throughout a project, as you'll see in [Data Management](02_data_management.md), and cash in when you publish, which we cover in [FAIR in action](03_data_publishing.md#fair-in-action). Here is a quick overview:

- F: Findable - Metadata and data should be easy to find for both humans and computers
- A: Accessible - Once the user finds the required data, they need to know how they can be accessed
- I: Interoperable - The data usually need to be integrated with other data and interoperate with workflows for analysis, storage, and processing
- R: Reusable - Data should be well-described so they can be reused or combined in different settings

It's important to note that "open" doesn't always mean completely accessible to everyone, all the time. It usually entails having clear and persistent ways to access the data, publication, code, etc. Sometimes, there are necessary restrictions around sharing different types of data, whether that's because of laws, ethics, or data sovereignty. The {term}`CARE principles <CARE principles>` for Indigenous Data Governance ([GIDA](https://www.gida-global.org/careprinciples)) are a very important example. GIDA describes them as complementing the existing FAIR principles, asking those who work with data to consider both people and purpose. In GIDA's words:

- C: Collective benefit - data ecosystems shall be designed and function in ways that enable Indigenous Peoples to derive benefit from the data.
- A: Authority to Control - Indigenous Peoples’ rights and interests in Indigenous data must be recognised and their authority to control such data be empowered.
- R: Responsibility - Those working with Indigenous data have a responsibility to share how those data are used to support Indigenous Peoples’ self-determination and collective benefit.
- E: Ethics - Indigenous Peoples’ rights and wellbeing should be the primary concern at all stages of the data life cycle and across the data ecosystem.

CARE is an important check on any project. Before you use or share data, ask whether they relate to Indigenous Peoples, lands, or waters, and so should follow the CARE principles. If they might, check the terms attached to the data and GIDA's guidance before you go further. Understanding where your data come from, and the terms attached to them, is each researcher's responsibility.

## Barriers to open science

Now that we have covered some of the reasons behind open science and adopting data best practices, we should cover some common barriers that come up in conversation. These apply to open science in general, including the reproducibility practices in [Data Management](02_data_management.md). For more information on these barriers and others we aren't going to cover, we highly recommend taking a look at [The Turing Way](https://book.the-turing-way.org/reproducible-research/overview/overview-barriers/).

Putting your code and data online can be revealing and intimidating. Sharing possible errors in your work is a real fear, but that is far outweighed by the feedback you may receive, and how you may help other scientists in their research. It is also a motivator to hold your work to a higher standard which benefits all who are involved and all who may learn from your work.

Working openly also takes additional time and effort, especially at the start of a project: setting up version control, writing tests for your code, and agreeing with collaborators on what will be shared, when, and how. That time pays off later. When a reviewer requests a change, version-controlled data and code make it much quicker to integrate, and because others can see how the work was done, they can check it and build on it.

Some barriers are bigger than any one person. Journals tend to favor novel results, reproducible practices are often not valued for promotion, and the skills involved take time to learn ([Whitaker, 2019](https://doi.org/10.5281/zenodo.2669547)). You can't fix these alone. That is a good reason to start with the steps you can control, and to support change in your team and institution where you can.

## Putting open science into practice

We know it is easy to talk about open science, and more difficult to pull these practices into your own work. There is a wider push towards adopting these open science workflows, and here are some tangible ways to work towards them:

- **Opt for constructive peer code reviews during the development phase.** We are human and it is important to foster an environment where everyone is comfortable sharing in-progress work for constructive feedback. It is often the best way to ensure quality and build confidence in your work.
- **Share work early and often with peers and collaborators.** This is related to our point about peer code reviews. In every phase of the scientific process, it is important to get other people's perspectives. They may think of an issue you've run into from another angle and help you find a solution that you may never have thought of.
- **Publish data and code as their own citable products.** This makes your data, code, and findings accessible to the wider water science community. It may add an extra step to the process, but it will in turn lower the barrier of entry for someone that is building off of concepts related to your work. It also ensures that if someone does use your data or code, you will be properly credited. It is through collaboration that we can move the scientific community forward, together.

Open science sets the values: work that others, including your future self, can find, check, and build on. The next two lessons put those values into practice. [Data Management](02_data_management.md) covers what you do during a project, and [Data Publishing](03_data_publishing.md) covers how you share the results so they last.

## Now you try it

Practice telling FAIR and open apart, using five datasets a water researcher might come across.

**Your task:** For each dataset below, mark which FAIR letters it meets (F, A, I, R) and whether it is *open*, meaning anyone can get the files without asking or being approved.

1. A stream gage's discharge record, served by a public web service, with a permanent site ID and documented formats.
2. Satellite water-surface data from a national archive, with a dataset DOI. Downloads are free but need a free account.
3. A repository record whose metadata anyone can read, but whose files are released on request because the sites are on private land.
4. A CSV on a lab's shared drive ("anyone with the link can view"), with no README.
5. Discharge values printed as a table in the PDF supplement of a journal article.

**What you should see:** Open and FAIR don't always go together. Two of the datasets are largely FAIR without being fully open, one is open but barely FAIR, and one is easy to get but hard for a machine to read.

:::{dropdown} Example answer
| # | F | A | I | R | Open? |
|---|---|---|---|---|---|
| 1 | ✓ permanent site ID, catalogued | ✓ standard web service | ✓ documented formats | ✓ if the metadata describe units and quality | Yes |
| 2 | ✓ DOI | ✓ standard protocol, with a free login | ✓ | ✓ | Free, but behind a login |
| 3 | ✓ metadata can be found | ✓ access rules are stated | Depends on the files | Depends on the metadata | No |
| 4 | ✗ no permanent ID or metadata | Partly: only while the link works | Maybe | ✗ no README | Yes, by link |
| 5 | Partly, through the article | ✓ | ✗ a PDF table isn't machine-readable | Partly | Only if the article is open access |

Datasets 2 and 3 are not fully open, but they are largely FAIR: you can find them, and the rules for getting the files are clear. Dataset 4 is open to anyone with the link, but with no persistent identifier and no metadata it is barely FAIR, and it can disappear at any time. Dataset 5 is easy to get but hard to reuse, because the values have to be copied out of a PDF by hand.
:::

*Optional:* where would your own data sit in this table today?

## Further reading

- [NSF's Public Access Policy](https://www.nsf.gov/policies/document/faq-public-access#qa-group-1)
- [AGU's Position Statement on Data](https://www.agu.org/science-policy/position-statements/open-data)
- [FAIR data principles](https://www.go-fair.org/fair-principles/)
- [CARE principles for Indigenous Data Governance](https://www.gida-global.org/careprinciples)
- [The Turing Way](https://book.the-turing-way.org/reproducible-research/overview/overview-barriers/)
- [Openscapes](https://openscapes.org)
- [NASA TOPS Open Science 101](https://science.data.nasa.gov/features-events/open-science-training)
