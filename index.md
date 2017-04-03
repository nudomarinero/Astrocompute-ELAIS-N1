---
layout: default
title: Astrocompute ELAIS-N1
---

# Astrocompute ELAIS-N1

Information about the [SKA](https://www.skatelescope.org/)-[AWS](http://aws.amazon.com/) [Astrocompute proposal](https://www.skatelescope.org/ska-aws-astrocompute-call-for-proposals/) called: \"Calibration of LOFAR ELAIS-N1 data in the Amazon cloud\". Maintained by J. Sabater (Institute for Astronomy, University of Edinburgh).

## LOFAR AMIs
We have created an AMI with the LOFAR software pre-installed: `ami-f7d4d0e0`. It is based on the Ubuntu 14.04 LTS official AMI.

Software installed:

* casacore libraries.
* casarest libraries.
* pyrap.
* LOFAR software (release 2.19).
* [CASA](http://casa.nrao.edu/).
* [LSMTool](https://github.com/darafferty/LSMTool).
* [LoSoTo](https://github.com/revoltek/losoto).
* [factor](https://github.com/revoltek/factor).
* [WSClean](https://sourceforge.net/projects/wsclean/).
* [Montage](http://montage.ipac.caltech.edu/index.html).
* [Sagecal](http://sourceforge.net/projects/sagecal/)
* Some additional Python libraries like [astropy](http://www.astropy.org/), [Jupyter](https://jupyter.org/), etc.
* GRID certificates and tools.
* SRM tools.
* AWS tools and Python libraries.
* Postgresql 8.4.10 formerly required by some LOFAR BBS tasks.

### Legacy AMIs
We keep some old AMIs for compatibility reasons:

* LOFAR 2.18 pre-release: `ami-05144012`
* LOFAR 2.17: `ami-bfc200d2`
* LOFAR 2.17 pre-release: `ami-8be114e6`
* LOFAR 2.15 node: `ami-5c261436`
* LOFAR 2.15 head: `ami-bf3507d5`
* LOFAR 2.12 node: `ami-431b6229`
* LOFAR 2.12 head: `ami-47156c2d`
* LOFAR 2.10 node: `ami-c7a3c3a2`
* LOFAR 2.10 head: `ami-69dfab0c`

Note that the AMIs called `node` do not have the GRID, SRM, AWS or Postgresql packages installed. Since the version 2.17 all the images include the same software.

### Packaging of LOFAR
The [radio-astro Ubuntu PPA](https://launchpad.net/~radio-astro/+archive/ubuntu/main) keeps all the LOFAR dependencies packaged and updated. However, we decided to independently generate the LOFAR package for each release to maintain control of the compilation process. 
The generation of the packages is explained in: https://github.com/nudomarinero/Astrocompute-ELAIS-N1/tree/master/vagrant

## Data release
The LOFAR data of the ELAIS-N1 field is released in the S3 bucket `lofar-elais-n1`

## Calibration pipeline
The calibration of the data is performed in two steps: a) the prefacet calibration and b) the facet calibration. All the steps are already implemented in: [https://github.com/nudomarinero/Astrocompute-ELAIS-N1/tree/master/pipeline].
 

