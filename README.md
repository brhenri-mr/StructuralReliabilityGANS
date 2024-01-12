# StructuralReliabilityGANS
A simple application of GANS in context for structural reliability


The core of ​​the project is to provide a generative neural network (GANS) that enables the design of W metal beams as a function of failure probability

![image](https://github.com/brhenri-mr/StructuralReliabilityGANS/assets/83376956/60d5b273-53a6-457a-b859-d26a8cbd6e79)

## Calculus probability of failure 

### Framework
- pystra

The calculation of the probability of failure constitutes the determination of the labels for each profile. The methodology selected for determining the probability of failure was the Monte Carlo method or simulation because it is highly generalizable. 

![equation](https://latex.codecogs.com/gif.image?\inline&space;\dpi{110}g(X)=\sigma_{R}-\sigma_{S})
