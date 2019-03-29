# Meeting Nodes

## 06 Nov 2018

Sample Rate Paper
- If a spike is missed in the signal sample then the STL checker will fail analyze that property
- If sample rate is high enough then the property check will be sufficient
- but the question is what should be the sampling rate of a signal
- How to query the signal trace

To Do list:

1) Future time chek should yield a ```Not Definitive``` answer for a check
If an formula requires signal values that are beyond the time scope then the answer shoudl be neither true or false since we have no way of knowing that at the present time
Add a feature so that the future time checks are handled by the interpreter

2) Plot the Signals
Have the data signals in a csv file
Plot them to easily visualize the trace
Vertical plots stacked together

3) Debug the Formula result
Just getting a true false result from the check is not helpful to find out where the check failed
Look into how to add markers to traces to show where the functions were invoked, figure out a strategy and test its feasibility

4) Signal Time Length
The code uses the max time of the signal for formulas such as Globally without a time range provided
Calculate that max time and provide it to interperter class for use

### Trace Understanding

Understanding a time series data is the most important aspect before devising a stategy for analysis.
What should be the sample rate
What plots should be made to visualize the behaviour