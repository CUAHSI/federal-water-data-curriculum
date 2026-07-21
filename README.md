![Static Badge](https://img.shields.io/badge/course_status-under_development-%23fcc200?style=for-the-badge)

# federal-water-data-curriculum
Course curriculum behind the CUAHSI program, Federal Open Water Data for Researchers (name still under development; repo name may change).

## Locally building the site

This is built as a [MyST](https://mystmd.org/) Markdown-based site to fit with [CUAHSI's Water Content Portal](https://water-content-portal.cuahsi.io/) and ease the integration into that website. To build locally, you will need Node.js, npm, and MyST.

Once you have `npm`, you can install `MyST` with:
```
npm install -g mystmd
```

To build locally and then view on the local host (http://localhost:3000):
```
myst start
```
