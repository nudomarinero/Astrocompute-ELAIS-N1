Calibration pipeline
====================

Implementation of the facet calibration pipeline (https://ui.adsabs.harvard.edu/#abs/2016ApJS..223....2V/abstract) in AWS using Ansible playbooks.


Usage
-----

The pipeline is run in several steps:
* Calibration of the calibrator
* Pre-processing of the target
* Subtraction of the self-cal model
* Facet calibration

By now (March 2017) the first three steps are implemented (although there are some upcoming modifications) and the last is under development. Use with care.

### Calibration of the calibrator

The first step is the calibration of the calibrator target to get the phase offsets between polarizations, the amplitude bandpass and the clock corrections.

Configure the calibrators to use by editing ```cal_config.yml```

Run the calibration with:
```
ansible-playbook cal.yml
```

The final results will be stored in S3. However, the disks used (EBS) have to be manually removed.

TODO:
* Automatic removal of bad subbands
* Automatically unmount and remove disks

### Pre-processing of the target

This is the second step of the calibration. It is composed of two main steps. The pre-processing and the self-calibration. 

Copy and edit ```prefactor_config.yml```

Launch the instance:
```
ansible-playbook prefactor.yml
```

The data is uploaded to S3 but the disks have to be manually deleted.

This step still has some problems with irregular datasets. In those cases the frequencies of the measurement sets have to be manually edited.

TODO:
* Sove problem with frequencies
* Automatically unmount and remove disks

### Subtraction of model

The third step of the calibration create a low and a high resolution model of the field which are subtracted. The output is a merged model and the residual data. It also outputs a high and a low resolution image of the field.

The configuration of this step, including the names of the bands to run is saved in subtract_config.yml

After modifying ```subtract_config.yml```, launch the subtract step with:
```
ansible-playbook subtract.yml
```

### Factor

Factor runs the facet calibration using the subtracted data. This step is still under development.

TODO
----

* Remove dependency on s3cmd and use directly awscli