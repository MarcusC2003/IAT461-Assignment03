# IAT 461 — Assignment 3 Report

## A1 — Data acquisition and cleaning

### Missing Employees

- There are no missing values
- Some businesses have 0 employees so I did not change impute or remove any of the rows

### Coordinates (lat, lon)

Although a significant amount (49.8%) of the location data is missing, later steps require the precise spatial data for clustering and mapping. Therefore the coordinates were dropped rather than imputed.

### Feepaid

Based on the City of Vancouver website, the business licensing fee based on the category/type. To verify I checked the mean, median, and mode which were all very close or identical. With this knowlege, I filled the missing fee values with the median fee of their respective types.

### Issue dates

Some `issueddate`/`expireddate` were not parsable or had negative times. Because the missing dates are not imputable i dropped them from the set. Additionally, the negative times could have been inaccurate and because there were only 66 negative times I chose to drop those as well instead of swapping the issue and expired dates.

### Businesstype consolidation + relabelling

To create new labels using `businesstype` and `businesssubtype`, I first identified the categories that made up around 80% of the data, then merged the remaining types into 1 group to reduce the number of new labels.

---

## A2 — Location-only clustering: K-means vs. DBSCAN

Based on elbow I have chosen K=6

_How do the K-means clusters map onto actual Vancouver geography — do they correspond to anything you'd recognize (downtown core, west side, etc.)?_

The K-Means section off Vancouver's regions fairly accurately. For example, downtown region is correctly sectioned off from the Mount Pleasent / Fairview group and the Kitsilano group.

_How do the DBSCAN clusters compare? Where do the two methods agree or disagree, and why — think about what each algorithm assumes about cluster shape and density, and what DBSCAN's "noise" points represent._

The DBScan clusters have much more variety in size and numbers. It targets the clusters buisnesses rather than geographic locations therefore we can use DBSCAN to identify groups of active buisnesses.

---

## A3 — Feature-based clustering: Size, Industry, Lifecycle

_What do the resulting clusters seem to represent? Does this differ from the purely geographic clustering in A2?_

The 6 clusters seem to represent the following industries

- Restaurant
- Long-term Rental + Other(approx. 1.2%)
- Health Care
- Legal Services
- Parking Areas / Garages
- Misc (a large chunk of the data / the rest)

Yes the purely geographic clustering sectioned off tightly compacted areas whereas this clustering can be used to identify industries.

---

## B4 — Cluster membership and interpretation

_Does the grouping seem meaningful given what you know (or can look up) about these areas?_

Yes the groupings are meaningful. It was expected that downtown would be the largest point plotted but it is helpful to visually see the amount of active businesses compared to other areas. The grouped locations themselves are also split into very well known areas/neighbourhoods in vancouver which are often used to casually identify where a store/restaurant is.

_Any surprising groupings?Explain using the actual cluster membership, not just the general shape of the plot._

I was surprised to see that Oakridge, Kensington, Victoria-Fraserview, and Killarney were all grouped together as they are quite far from each other. One thing i did find interesting was how the clusters differed based on the K.

#### B5 — Suggested reflection questions (optional, not required)

_Do business-similar areas also tend to be geographically close, or does similarity cut across geography?_

Mostly cuts across geography. At (K=6) a couple of clusters are geographically close (Downtown is its own cluster; Grandview-Woodland and Strathcona pair up), but most clusters mix west-side and east-side areas (e.g. Arbutus-Ridge and Kerrisdale group with Renfrew-Collingwood and Hastings-Sunrise).

_How does this compare to your Part A "Industry" clustering — consistent story, or different?_

Consistent. Part A's business-level clusters (Restaurant, Long-term Rental, Health Care, Legal Services, Parking/Garage, Misc) are the same categories separating the Part B area clusters. For example the residential east-side cluster (Oakridge, Kensington, Victoria-Fraserview, Killarney) is elevated in Health Care and Long-term Rental.

_Pick one area you didn't expect to see grouped with another — what do they have in common?_

As mentioned before I was surprised to see that Oakridge, Kensington, Victoria-Fraserview, and Killarney were all grouped together. Oakridge reads as an affluent mall/condo area, Killarney as a quieter suburb. However, all four areas lean heavily toward Health Care Professionals and Services and Long-term Rental, with little Legal Services or Restaurant presence.
