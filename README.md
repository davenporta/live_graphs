# live_graphs
Live graph dashboard for MASA testing

-----------------------

### Plot Configuration
Easily configurable with graph_settings.csv file
Each row is a separate plots
Add as many as you'd like

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
seconds | seconds of data to plot (up to `seconds_to_store`)

### Required Python Libraries
* PyQt5
* PyQtGraph
* Pandas
* NumPy

### Task List
- [ ] proper data stream to dataframe (networking)
- [ ] add numerical fields (not just graphs)
- [ ] mathematical operations on datasets (for calculating total thrust or pressure drop or what not)
- [ ] figure out window sizing
- [ ] pretty things up
- [ ] settings menu
