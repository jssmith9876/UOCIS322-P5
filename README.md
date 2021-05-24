# UOCIS322 - Project 5 #
Brevet time calculator with MongoDB.

## Overview
Brevet control opening and closing time calculator.

This calculator calculates its times based on the RUSA ACP controle time calculator.
For more information: https://rusa.org/pages/acp-brevet-control-times-calculator

## Instructions
For a given brevet distance, the user must input values that correspond to the control distances (in either miles or kilometers) for the given brevet. 
The opening and closing time for each control point will then be calculated.

The control distances MUST:
* Be listed in ascending order.
* Have the last distance be at least the total brevet distance.
* Have all distances be less than 20% longer than the total brevet distance.

The times can now be submitted using the submit button. Once the button has been clicked, all current times will be stored in a database. The display button next to the submit button will then display the last submitted times to the user. 

To submit your times, all warnings must be dealt with beforehand. The submission will not complete unless there are no warnings with the checkpoint times. 

## Author: Jordan Smith, jsmith37@uoregon.edu ##