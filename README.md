# live_graphs
Live graph dashboard for MASA testing

-----------------------

### Configuration
Easily configurable with settings.csv file

Column | Function
------ | --------
type | not yet implemented
title | title of plot
x | pandas dataframe header for x axis data
xlabel | x axis label
y | y data set header in database (divide with " \| ")
alias | data title in legend (divide with " \| ")
pen | curve style field (divide with " \| ")
ylabel | y axis label
row, col | subplot layout position

### Required Python Libraries
* PyQt5
* PyQtGraph
* Pandas
* NumPy

### Task List
- [ ] proper data stream to dataframe
- [ ] add numerical fields (not just graphs)
- [ ] mathematical operations on datasets (for calculating total thrust or pressure drop or what not)
- [ ] figure out window sizing
- [ ] pretty things up
