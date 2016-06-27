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

By now (April 2016) the first two steps are implemented but under heavy development. Use with care.

### Calibration of the calibrator

The first step is the calibration of the calibrator target to get the phase offsets between polarizations, the amplitude bandpass and the clock corrections.

Launch the instance:
```
ansible-playbook launch_cal.yml
```

Setup the instance to install some additional packages needed and the credentials:
```
ansible-playbook setup_cal.yml
```

Launch the steps needed before the calibation:
```
ansible-playbook run_cal.yml
```

At this point the pipeline have to be manually run from within the instance:
```
cd ~/astrocompute/pipeline/generic_pipeline/
genericpipeline.py -c pipeline.cfg pre_facet_cal_rawdata.parset
```
If there were problems with the first round or a subband was clearly bad, it is possible to edit the pipeline and run only the required part using the pipeline ```pre_facet_cal_rawdata_2ndround.parset```. This will be automated in the future.


Move the final results to S3:
```
ansible-playbook finish_cal.yml
```

The instance has to be shutdown now.

TODO:
* Automatic removal of bad subbands
* Alerts when the computing is finished
* Automatic shutdown of instances

### Pre-processing of the target

This is the second step of the calibration. It is composed of two main steps. The pre-processing and the self-calibration. If the processing fails at some point after the first step is finished, the calibration can be continued from this point using an adapted alternative pipeline (```pre-facet-pretarget_resume2.parset```).

Launch the instance:
```
ansible-playbook launch_pretarget.yml
```

Setup the instance to install some additional packages needed and the credentials:
```
ansible-playbook setup_pretarget.yml
```

Launch the steps needed before the calibation:
```
ansible-playbook run_pretarget.yml
```

After the data is downladed the pipeline can be run.

### Subtraction of model

The third step of the calibration create a low and a high resolution model of the field which are subtracted. The output is a merged model and the residual data. It also outputs a high and a low resolution image of the field.

There are two main yml: subtract_all.yml and subtract_one.yml. The first is used to run the subtraction of several bands in parallel and the second to run the subtraction in just one band. 

The configuration of this step, including the names of the bands to run is saved in subtract_config.yml

After modifying ```subtract_config.yml```, launch the subtract step with:
```
ansible-playbook subtract_all.yml
```


TODO
----

* Remove dependency on s3cmd and use directly awscli