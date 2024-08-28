# Purpose

A project that deploys the USDM package and processes study spreadsheets to create

- USDM API JSON files
- PNG of the study nodes and relationships
- Set of nodes and edges for the study
- A fltered set of nodes and edges for timelines

# Studies

The current set of mapped studies are:

- Roche NCT04320615 COVID pneumonia
- Eli Lilly NCT03421379 diabetes
- CDISC Pilot Study
- Simpe Example 1, 2 and 3 showing the basic use of the spreadsheet format
- Cycles 1 and 2 showing the ability to model cycles within studies
- Profile 1 to demonstrate the use of profiles (additional timelines)

# Issues

## Certificates

If you get a cetificate error on Mac OS 

```[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate````

then run the command 

```/Applications/Python 3.10/Install Certificates.command```