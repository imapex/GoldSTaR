# GoldSTaR
Support Tips and Registration Engine

## Overview
GoldSTaR is an application designed to simplify the support of Cisco equipment.  The application will collect an inventory of a customer's equipment from multiple sources.  Intially this will come from APIC-EM.  

The details about the collected inventory, including running image, will be compared to the suggested values from the Cisco Support API.  The results will be presented back and ordered by priorirty.

***Stretch Goals***

The application will injest the current field notices and present any current field notices for a given product and allow the user to sign up for future field notices. 

Prime Infrastructure included as a source to injest inventory.

## Prerequisites
APIC-EM must be up and running and managing equpment.

## To Do
* [ ] Implement Support API to query suggested software releases
* [ ] Add web front end for simplified navigation
* [ ] Get FN information for the list of PlatformIDs
* [ ] Allow the user to subscribe to associated FNs
