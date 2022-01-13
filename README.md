# Digital Hologram Vortex Elimination
This repository has two different methods to eliminate vortices/residuals in digital holograms. One version calculates an anti-vortex to eliminate, the other one uses a least-squares phase unwrapping approach using FFTs.

## Least-Squares Two-Dimensional Phase Unwrapping Using FFTs
The basis for this approach comes from the 1994 paper Least-Squares Two-Dimensional Phase Unwrapping Using FFT's by Mark D. Pritt and Jerome S. Shipman.

The following steps from this paper were implemented:

1. Calculate ![equation](https://latex.codecogs.com/png.image?%5Cdpi%7B120%7D%20%5Cbg_white%20%5Cinline%20%5Crho_%7Bjk%7D)
2. Compute the two-dimensional FFT of ![equation](https://latex.codecogs.com/png.image?%5Cdpi%7B120%7D%20%5Cbg_white%20%5Cinline%20%5Crho_%7Bjk%7D)
3. Replace the values of the transformed array with the values ![equation](https://latex.codecogs.com/png.image?%5Cdpi%7B120%7D%20%5Cbg_white%20%5Cinline%20%5CPhi_%7Bmn%7D)
4. Compute the inverse FFT. The result is the desired solution function ![equation](https://latex.codecogs.com/png.image?%5Cdpi%7B120%7D%20%5Cbg_white%20%5Cinline%20%5Cphi_%7Bjk%7D)

## Two-Dimensional Phase Unwrapping by Direct Elimination of Rotational Vector fields
The basis for this approach comes from the 1998 paper Two-Dimensional Phase Unwrapplng by Direct Elimination of Rotational Vector Fields from Phase Gradients Obtained by Heterodyne Techniques by Takahiro Aoki, Toshihiro Sotomaru, Takeshi Ozawa, Takashi Komiyama, Yoko Miyamoto and Mitsuo Takeda.
