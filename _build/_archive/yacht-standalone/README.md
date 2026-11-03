# Build files for yacht-rental-dubai/index.html

Only needed to change the map or the page template. Day-to-day edits (prices, boats, phone) go straight into the
`charter-data` block in `../../yacht-rental-dubai/index.html`.

```sh
python3 chart.py                                  # coastline, Palm and routes -> chart.json
python3 chart_svg.py chart.json chart.svg.html    # chart.json -> SVG markup
python3 build.py . ../../site/yacht-rental-dubai  # template.html + SVG + FAQ -> index.html
```
