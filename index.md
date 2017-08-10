---
layout: default
title: Astrocompute ELAIS-N1
---

# Astrocompute ELAIS-N1

Information about the [SKA](https://www.skatelescope.org/)-[AWS](http://aws.amazon.com/) [Astrocompute proposal](https://www.skatelescope.org/ska-aws-astrocompute-call-for-proposals/) called: \"Calibration of LOFAR ELAIS-N1 data in the Amazon cloud\". Maintained by J. Sabater (Institute for Astronomy, University of Edinburgh).

## LOFAR AMIs
We have created an AMI with the LOFAR software pre-installed: `ami-bdab83c6`. It is based on the Ubuntu 16.04 LTS official AMI.

Software installed:

* casacore libraries.
* casarest libraries.
* pyrap.
* LOFAR software (release 2.21).
* [CASA](http://casa.nrao.edu/).
* [LSMTool](https://github.com/darafferty/LSMTool).
* [PyBDSF](https://github.com/lofar-astron/PyBDSF).
* [LoSoTo](https://github.com/revoltek/losoto).
* [factor](https://github.com/revoltek/factor).
* [WSClean](https://sourceforge.net/projects/wsclean/).
* [Montage](http://montage.ipac.caltech.edu/index.html).
* [Sagecal](http://sourceforge.net/projects/sagecal/)
* Some additional Python libraries like [astropy](http://www.astropy.org/), [Jupyter](https://jupyter.org/), etc.
* GRID certificates and tools.
* SRM tools.
* AWS tools and Python libraries.
* [ddf pipeline](https://github.com/mhardcastle/ddf-pipeline).

### Legacy AMIs
We keep some old AMIs with Ubuntu 14.04 LTS for compatibility reasons:

* LOFAR 2.19: `ami-f7d4d0e0`
* LOFAR 2.18 pre-release: `ami-05144012`
* LOFAR 2.17: `ami-bfc200d2`
* LOFAR 2.17 pre-release: `ami-8be114e6`
* LOFAR 2.15 head: `ami-bf3507d5`

### Packaging of LOFAR
The [Kern](http://kernsuite.info/) [PPA](https://launchpad.net/~kernsuite/+archive/ubuntu/kern-dev/) keeps all the LOFAR dependencies packaged and updated. However, we decided to independently generate the LOFAR package for each release to maintain control of the compilation process and to be able to quickly deploy patched versions of the LOFAR software when a bug is found. 
The generation of the packages is explained in: [Github vagrant](https://github.com/nudomarinero/Astrocompute-ELAIS-N1/tree/master/vagrant)

## Data release
The LOFAR data of the ELAIS-N1 field is released in the S3 bucket `lofar-elais-n1`. A list with the data can be found in: [data](http://www.lofarcloud.uk/data.html).

## Calibration pipeline
The calibration of the data is performed in two steps: a) the prefacet calibration and b) the facet calibration. All the steps are already implemented in: [Github pipeline](https://github.com/nudomarinero/Astrocompute-ELAIS-N1/tree/master/pipeline).

## Publications
Articles:
* Calibration of LOFAR data on the cloud (published in Astronomy & Computing): [lofar_cloud.pdf](http://www.roe.ac.uk/~jsm/lofar/lofar_cloud.pdf)


