# ArithmeticProgression

AP Math problem for AZsPCs, autumn 2021 http://azspcs.com/Contest/APMath.

I have made a few versions of a greedy algorithm in 1 dimension which has similar performance.

13/10-21
The basic greedy algorithm is also implemented for the hexagons in the competition. This scores about 0.7 points per n.
So after sending in results for the first 13 n I get just under 9 points. Apart from the algorithm not finding optimal
solutions it is also slow as it makes numerical computations in a nested loop. This makes it difficult to run the algorithm
on for the large hexagons. On my laptop it would likely take a few days.

25/10-21
Now I implemented the greedy algorithm that looks from the middle and out on the hexagonical grid. That was not good
itself but then I inverted it so it looks from the outside and in. This was a breakthrough. On some grids i find over 10%
more cells, but fewer on some.

The weakness of this algo is however that it stores the gridpoints as a list and goes from the list out-to-in. It does
not measure the distance from the middle centre. Which is more in tune with the idea behind the algorithm.
