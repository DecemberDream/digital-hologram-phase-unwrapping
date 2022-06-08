# Digital Hologram Vortex Elimination
This repository has two different methods to eliminate vortices/residuals in digital holograms. One version calculates an anti-vortex to eliminate, the other one uses a least-squares phase unwrapping approach using FFTs.

## Least-Squares Two-Dimensional Phase Unwrapping Using FFTs
The basis for this approach comes from the 1994 paper Least-Squares Two-Dimensional Phase Unwrapping Using FFT's by Mark D. Pritt and Jerome S. Shipman.

The following steps from this paper were implemented:

1. Calculate $\rho_{jk}$
2. Compute the two-dimensional FFT of $\rho_{jk}$
3. Replace the values of the transformed array $\rho_{jk}$ with the values $\Phi_{mn}$
4. Compute the inverse FFT. The result is the desired solution function $\phi_{jk}$

## Two-Dimensional Phase Unwrapping by Direct Elimination of Rotational Vector fields
The basis for this approach comes from the 1998 paper Two-Dimensional Phase Unwrapplng by Direct Elimination of Rotational Vector Fields from Phase Gradients Obtained by Heterodyne Techniques by Takahiro Aoki, Toshihiro Sotomaru, Takeshi Ozawa, Takashi Komiyama, Yoko Miyamoto and Mitsuo Takeda.

The gist of this approach is to create anti-vortices and add them exactly onto the origins of the vortices. If it's a positive vortex, add the negative and vice versa. This eliminates the vortices and cleans up the image.

## Performance
The code was benchmarked in a non-rigorous manner using the `time`-library. A Intel i5-4690 was used and the lowest time of 3 runs is presented. The [test-image](input/test.bmp) is the `1024x1024` pixels image provided in the input-folder.

| Test (Algorithm/Function) | Time (in seconds) |
| --- | --- |
| Anti-Vortices (iterative) | 14.2 s |
| Iterative Function (laplace) | 17.2 s |
| Kernel (laplace) | 8 s |

So I would recommend using the Kernel approach used in the `laplace`-file.
