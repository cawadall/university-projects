Simple Noise Nuisance Evaluator 
---

This program computes the Corrected Equivalent Continuous Noise Index (LKeq,T) for the assessment of the noise nuisance resulting form the performance of a given activity, indicating wether the [RD1367](https://github.com/cawadall/university_projects/acoustics/BOE-A-2007-RD1367.pdf) established regulations (Spain) are complied with.


### Usage
To run this program, just select the following parameters:

#### Input Parameters:
1. **LAeq,T** (Equivalent Continuous A-weighted Sound Pressure Level [dBA]) - The noise index associated with the annoyance, or harmful effects, over a time period T. Measured in dBA.
2. **LCeq,T** (Equivalent Continuous C-weighted Sound Pressure Level [dBC]) - The noise index associated with the annoyance, or harmful effects, over a time period T. Measured in dBC.
3. **LAIeq,T** (Impulsive equivalent Continuous A-weighted Sound Pressure Level [dbA]) - Noise index with the time impulse constant (I) of the measuring equipment.
4. **LAIeq,n,T** [dBA] - LAeq,T of the backgorund noise (without the activity).
5. **LCeq,n,T** [dBC] - LCeq,T of the backgorund noise
6. **LAIeq,n,T** [dBA] - LAIeq,T of the backgorund noise
7. **Activity Type** - Acoustic emitter type [string]. Only the following values are admitted:
    - 'infraestructura_viaria': highway infrastructure.
    - 'actividad': normal activity involving noise.
    - 'actividad_colindante': activity adjacent to the measurement site.

#### Output:
1. LKeq,T - Corrected Equivalent Continuous Noise Index [dB]
2. String indicating regulation compliance or non-compliance

#### Execution:

```python
python3 evaluacion_ruido.py <'LAeq'> <'LCeq'> <'LAIeq'> <'LAeq ruido de fondo'> <'LCeq ruido de fondo'> <'LAIeq ruido de fondo'> <'Tipo de actividad: infraestructura_viaria, actividad o actividad_colindante'>
```
